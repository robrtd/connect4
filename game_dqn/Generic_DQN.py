import numpy as np
import sys, json, os
from sklearn.model_selection import train_test_split

class ExperienceReplay(object):
    def __init__(self, size=(84,84), layers=3, num_actions = 13, max_memory=1000, discount=.9):
        self.max_memory = max_memory
        self.size = size
        self.num_actions = num_actions
        shape = (max_memory,) + size + (layers,)
        self.state_t = np.zeros(shape).astype('float32')
        self.action_t = np.zeros((max_memory,num_actions)).astype('float32')
        self.reward_t = np.zeros(max_memory).astype('float32')
        self.game_over = np.zeros(max_memory).astype('bool')
        self.discount = discount

    def remember(self, index, state, action, reward, game_over = False):
        assert index < self.max_memory

        self.state_t[index] = state
        self.action_t[index] = action
        self.reward_t[index] = reward
        self.game_over[index] = game_over

    def get_batch(self, model, single_actions = False):
        inputs = self.state_t
        targets = model.predict(inputs)

        # ignore targets for actions already taken
        if single_actions:
            for i in range(self.action_t.shape[0]):
                action_index = np.argmax(self.action_t[i])
                for j in range(i+1, targets.shape[0]):
                    targets[j][action_index] = -1

        # Q-values are the predictions of the next state, i.e. we simply shift target by one
        Q_sa = targets[1:]

        for i in range(0,self.max_memory):
            # reward_t + gamma * max_a' Q(s', a')
            reward_value = self.reward_t[i]
            if not self.game_over[i]: # same as: i < self.max_memory - 1
                # targets in next screen are possible oppponents rewards
                # therefore, we subtract them
                reward_value -= self.discount * np.max(Q_sa[i])

            targets[i, np.argmax(self.action_t[i])] = reward_value

        return inputs, targets


class DQN_Learn(object):
    def __init__(self, num_actions, grid_size, q_learning_epochs = 2, fixed_learning_epochs = 2, batch_size = 50):
        self.num_actions = num_actions
        self.q_learning_epochs = q_learning_epochs
        self.fixed_learning_epochs = fixed_learning_epochs
        self.batch_size = batch_size
        self.grid_size = grid_size
        self.experience_list = []

    @staticmethod
    def get_datafiles(dir):
        filelist = []
        for fn in os.listdir(dir):
            print (dir + fn)
            filelist.append(dir + fn)
        return filelist

    def load_games(self, game_list, size=(84,84), layers = 3, num_actions = 13, input_shape = None):
        for game in game_list:
            max_memory = len(game.get_screens())-1
            # Initialize experience replay object
            exp_replay = ExperienceReplay(max_memory=max_memory, size=size, layers=layers, num_actions=num_actions)
            game.load_experience(exp_replay, max_memory, input_shape = input_shape)
            self.experience_list.append(exp_replay)


    def learn(self, model, model_file = None, start_from_scratch=False, reference_states=None, input_shape=None, single_actions = False):
        q_progress = {'q_values': [], 'epochs': []}

        if model_file is not None and not start_from_scratch:
            model.load_weights(model_file)

        if reference_states is not None:
            q_progress['q_values'].append(self.get_avg_max_q(model, reference_states=reference_states, shape=input_shape));
            q_progress['epochs'].append(0)

        # Train
        for e in range(self.q_learning_epochs):

            all_inputs = None
            all_targets = None

            for el in self.experience_list:
                # the Q-learning magic happens here...
                inputs, targets = el.get_batch(model, single_actions=single_actions)

                if input_shape is not None:
                    inputs.reshape((inputs.shape[0],) + input_shape)

                if (all_inputs is None):
                    all_inputs = inputs
                    all_targets = targets
                else:
                    all_inputs = np.concatenate( (all_inputs, inputs), axis=0)
                    all_targets = np.concatenate( (all_targets, targets), axis=0)

            # adapt model
            X_train, X_test, y_train, y_test = train_test_split(all_inputs, all_targets, test_size=0.01) #Xrandom_state=42)
            model.fit(X_train, y_train, validation_data=(X_test, y_test), nb_epoch=self.fixed_learning_epochs, batch_size=self.batch_size)
            scores = model.evaluate(X_test, y_test, verbose=0)

            print e, scores
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
        print "Q-Matrix: ", q_matrix[0]
        q_sum = 0
        for id in range(0, cnt):
            q_sum += q_matrix[id].max()

        # print "Q-average: ", q_sum / 1. / cnt
        return q_sum / 1. / cnt