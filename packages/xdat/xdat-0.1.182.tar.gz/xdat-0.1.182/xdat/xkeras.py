import tensorflow as tf
from keras.layers import Conv2D
from keras.layers import Layer, Dense, GlobalAveragePooling2D, GlobalMaxPooling2D, Reshape, Activation, add, multiply

from keras.models import clone_model
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.utils import Sequence


def clone_keras_model(model):
    # Clone the model's architecture
    cloned_model = clone_model(model)

    # Compile the cloned model (use the same parameters as the original model)
    cloned_model.compile(optimizer=model.optimizer,
                         loss=model.loss,
                         metrics=model.metrics)

    return cloned_model


class ImageDataGenerator(Sequence):
    """
    batch_size=32
    target_size=(224,224)

    generator = ImageDataGenerator(df, batch_size, target_size)
    model.fit(generator, epochs=epochs)

    generator_for_prediction = ImageDataGenerator(df, batch_size, target_size, target_col=None, shuffle=False)
    predictions = model.predict(generator_for_prediction)
    """

    def __init__(self, dataframe, batch_size, target_size, shuffle=True, image_path_col='image_path', target_col='target', process_image=None):
        self.dataframe = dataframe
        self.batch_size = batch_size
        self.target_size = target_size
        self.shuffle = shuffle
        self.image_path_col = image_path_col
        self.target_col = target_col
        self.indices = np.arange(len(dataframe))
        if process_image is not None:
            self.process_image = process_image

        if self.shuffle:
            np.random.shuffle(self.indices)

    def __len__(self):
        return int(np.ceil(len(self.dataframe) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch = [self.dataframe.iloc[i] for i in batch_indices]

        images = np.array([self.load_and_preprocess_image(row[self.image_path_col], self.target_size) for row in batch])

        if self.target_col is None:
            return images

        labels = np.array([row[self.target_col] for row in batch])
        return images, labels

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

    def load_and_preprocess_image(self, image_path, target_size):
        img = load_img(image_path, target_size=target_size)
        img_array = np.array(img.convert('RGB'))
        img_array = self.process_image(img_array)
        return img_array

    def process_image(self, img):
        return img


class SpatialAttentionLayer(Layer):
    def __init__(self, **kwargs):
        super(SpatialAttentionLayer, self).__init__(**kwargs)
        # Initialize the Conv2D layer with a single filter for spatial attention
        self.conv2d = Conv2D(1, (3, 3), activation='sigmoid', padding='same')

    def call(self, input_feature):
        # Apply the Conv2D layer to learn spatial attention
        attention = self.conv2d(input_feature)
        return attention * input_feature

    def get_config(self):
        return super(SpatialAttentionLayer, self).get_config()


class ChannelAttentionLayer(Layer):
    def __init__(self, ratio=8, **kwargs):
        super(ChannelAttentionLayer, self).__init__(**kwargs)
        self.ratio = ratio
        self.shared_layer_one = None
        self.shared_layer_two = None

    def build(self, input_shape):
        channel = input_shape[-1]
        # Initialize shared layers in the build method to ensure the channel dimension is known
        self.shared_layer_one = Dense(channel // self.ratio, activation='relu', kernel_initializer='he_normal', use_bias=True, bias_initializer='zeros')
        self.shared_layer_two = Dense(channel, kernel_initializer='he_normal', use_bias=True, bias_initializer='zeros')
        super(ChannelAttentionLayer, self).build(input_shape)

    def call(self, input_feature):
        channel = input_feature.shape[-1]
        avg_pool = GlobalAveragePooling2D()(input_feature)
        avg_pool = Reshape((1, 1, channel))(avg_pool)
        avg_pool = self.shared_layer_one(avg_pool)
        avg_pool = self.shared_layer_two(avg_pool)

        max_pool = GlobalMaxPooling2D()(input_feature)
        max_pool = Reshape((1, 1, channel))(max_pool)
        max_pool = self.shared_layer_one(max_pool)
        max_pool = self.shared_layer_two(max_pool)

        attention = add([avg_pool, max_pool])
        attention = Activation('sigmoid')(attention)

        return multiply([input_feature, attention])

    def get_config(self):
        config = super(ChannelAttentionLayer, self).get_config()
        config.update({"ratio": self.ratio})
        return config


class ShuffleLayer(Layer):
    def __init__(self, **kwargs):
        super(ShuffleLayer, self).__init__(**kwargs)

    def call(self, inputs, training=None):
        if training:
            # Shuffle along the batch dimension
            return tf.random.shuffle(inputs)
        else:
            return inputs


class RGBtoHSVLayer(Layer):
    def __init__(self, **kwargs):
        super(RGBtoHSVLayer, self).__init__(**kwargs)

    def call(self, inputs):
        return tf.image.rgb_to_hsv(inputs)


def mape_loss(y_true, y_pred):
    return tf.reduce_mean(tf.abs((y_true - y_pred) / y_true)) * 100


