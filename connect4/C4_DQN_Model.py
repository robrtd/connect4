from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import sgd, RMSprop
import logging

class C4_DQN_Model(object):
    model_shape = (6, 7, 2)

    @staticmethod
    def get_model_shape():
        return C4_DQN_Model.model_shape

    @staticmethod
    def get_channels():
        return C4_DQN_Model.model_shape[2]

    @staticmethod
    def create_model():
        #return C4_DQN_Model.create_model_conv()
        return C4_DQN_Model.create_model_deep()

    @staticmethod
    def create_model_conv():
        model = Sequential()

        model.add(Conv2D(6 * 7, 2, 2, input_shape=C4_DQN_Model.model_shape, subsample=(1, 1), dim_ordering='tf', activation='relu'))
        model.add(Flatten())
        model.add(Dense(42*42, activation='relu'))
        model.add(Dense(7, init='normal', activation='linear'))
        # linear output so we can have range of real-valued outputs -- stolen from http://outlace.com/Reinforcement-Learning-Part-3/
        rms = RMSprop()
        model.compile(loss="mse", optimizer=rms)

        return model

    @staticmethod
    def create_model_deep():
        model = Sequential()

        model.add(Conv2D(filters=81, kernel_size=(2,2), strides=(1,1), use_bias=True, data_format='channels_last', input_shape=C4_DQN_Model.model_shape, activation='relu'))
        logging.debug('Layer-1 output-shape: ' + str(model.output_shape))
        model.add(Conv2D(filters=3*81, kernel_size=(2,2), strides=(1,1), use_bias=True, data_format='channels_last', activation='relu'))
        logging.debug('Layer-2 output-shape: ' + str(model.output_shape))
        model.add(Conv2D(filters=9*81, kernel_size=(2,2), strides=(1,1), use_bias=True, data_format='channels_last', activation='relu'))
        logging.debug('Layer-3 output-shape: ' + str(model.output_shape))
        #model.add(MaxPooling2D(pool_size=(2,2), data_format='channels_last'))
        model.add(Dropout(rate=0.2))
        logging.debug('Layer-4 output-shape: ' + str(model.output_shape))
        model.add(Flatten())
        logging.debug('Layer-5 output-shape: ' + str(model.output_shape))
        model.add(Dense(9*81, activation='relu'))
        logging.debug('Layer-6 output-shape: ' + str(model.output_shape))
        model.add(Dropout(rate=0.4))
        logging.debug('Layer-7 output-shape: ' + str(model.output_shape))
        model.add(Dense(7, activation='linear'))
        logging.debug('Layer-8 output-shape: ' + str(model.output_shape))
        # linear output so we can have range of real-valued outputs -- stolen from http://outlace.com/Reinforcement-Learning-Part-3/
        rms = RMSprop()
        model.compile(loss="mse", optimizer=rms)

        return model


    @staticmethod
    def create_model_fcn():
        model = Sequential()

        model.add(Dense(6*7*4, activation='relu', input_dim=6*7, init='normal'))
        model.add(Dense(6*7*4, activation='relu', init='normal'))
        model.add(Dropout(0.2))
        model.add(Dense(6*7*4, activation='relu', init='normal'))
        model.add(Dense(7, init='normal', activation='linear'))
        rms = RMSprop()
        model.compile(loss="mse", optimizer=rms)

        return model
