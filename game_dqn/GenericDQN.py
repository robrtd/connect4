import statistics
import numpy as np
from sklearn.model_selection import train_test_split
import logging
import ExperienceReplay as er
from keras.callbacks import TensorBoard, ReduceLROnPlateau
from time import time
import keras.backend as K

class GenericDQN(object):
    def __init__(self, num_actions, single_actions=False, q_learning_epochs=2, fixed_learning_epochs=2, batch_size=50):
        self.num_actions = num_actions
        self.single_actions = single_actions
        self.q_learning_epochs = q_learning_epochs
        self.fixed_learning_epochs = fixed_learning_epochs
        self.batch_size = batch_size
        self.experience_list = []


    def load_games(self, game_list, input_shape = None):
        for game in game_list:
            max_memory = len(game.get_screens())-1
            # Initialize experience replay object
            exp_replay = er.ExperienceReplay(model_shape=input_shape, num_actions=self.num_actions, max_memory=max_memory)
            game.load_experience(exp_replay, max_memory, input_shape = input_shape)
            self.experience_list.append(exp_replay)


    def learn(self, model, model_file = None, start_from_scratch=False, reference_states=None, input_shape=None):
        q_progress = {'q_values': [], 'epochs': []}
        tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

        if model_file is not None and not start_from_scratch:
            model.load_weights(model_file)

        # TODO: find alternative way for calculating reference-q-values
        if reference_states is not None:
            q_progress['q_values'].append(self.get_avg_max_q(model, reference_states=reference_states, shape=input_shape));
            q_progress['epochs'].append(0)

        # Train
        for e in range(self.q_learning_epochs):

            all_inputs = None
            all_targets = None
            all_q_deltas = []

            for el in self.experience_list:
                # the Q-learning magic happens here...
                inputs, targets, q_delta = el.get_batch(model, single_actions=self.single_actions, p=0.25)

                if input_shape is not None:
                    inputs.reshape((inputs.shape[0],) + input_shape)

                if (all_inputs is None):
                    all_inputs = inputs
                    all_targets = targets
                else:
                    all_inputs = np.concatenate( (all_inputs, inputs), axis=0)
                    all_targets = np.concatenate( (all_targets, targets), axis=0)

                all_q_deltas += q_delta

            logging.debug("q_deltas: N: %d, min %f, max %f, avg %f" % (len(all_q_deltas), min(all_q_deltas), max(all_q_deltas), statistics.mean(all_q_deltas)))
            # adapt model
            X_train, X_test, y_train, y_test = train_test_split(all_inputs, all_targets, test_size=0.2) #Xrandom_state=42)
            _lr = K.get_value(model.optimizer.lr)
            logging.debug(" Current learning rate (before fit):" + str(_lr))
            #K.set_value(model.optimizer.lr, _lr/10.)
            reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=1, verbose=1)
            #model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=self.fixed_learning_epochs, batch_size=self.batch_size, callbacks=[tensorboard, reduce_lr])
            model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=self.fixed_learning_epochs,
                      batch_size=self.batch_size, callbacks=[tensorboard])
            _lr = K.get_value(model.optimizer.lr)
            logging.debug(" Current learning rate  (after fit):" + str(_lr))
            scores = model.evaluate(X_test, y_test, verbose=0)

            print(e, scores)
            print("Baseline Error: %.2f%%" % (100-scores*100))
            loss = scores

            print("Epoch {:03d}/{:03d} | Loss {:.4f}".format(e, self.q_learning_epochs, loss))

            if reference_states is not None:
                q_progress['q_values'].append(self.get_avg_max_q(model, reference_states=reference_states, shape=input_shape));
                prev_epochs = q_progress['epochs'][len(q_progress['epochs'])-1]
                q_progress['epochs'].append(prev_epochs + len(self.experience_list))

            # Save trained model weights and architecture, this will be used by the visualization code
            if model_file is not None:
                model.save_weights(model_file, overwrite=True)

        return q_progress

    @staticmethod
    def get_avg_max_q(model, reference_states, shape=None):
        cnt = reference_states.shape[0]
        ref = reference_states
        if shape is not None:
            ref = reference_states.reshape((cnt,) + shape)
        q_matrix = model.predict(ref)
        print("Q-Matrix: ", q_matrix[0])
        q_sum = 0
        for id in range(0, cnt):
            q_sum += q_matrix[id].max()

        # print "Q-average: ", q_sum / 1. / cnt
        return q_sum / 1. / cnt