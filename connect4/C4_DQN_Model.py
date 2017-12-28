from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Convolution2D
from keras.optimizers import sgd, RMSprop

class C4_DQN_Model(object):
    model_shape = (6, 7, 1)

    @staticmethod
    def get_model_shape():
        return C4_DQN_Model.model_shape

    @staticmethod
    def create_model():
        return C4_DQN_Model.create_model_conv()

    @staticmethod
    def create_model_conv():
        model = Sequential()

        model.add(Convolution2D(6 * 7, 2, 2, input_shape=C4_DQN_Model.model_shape, subsample=(1, 1), dim_ordering='tf', activation='relu'))
        model.add(Flatten())
        model.add(Dense(42*42, activation='relu'))
        model.add(Dense(7, init='normal', activation='linear'))
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
