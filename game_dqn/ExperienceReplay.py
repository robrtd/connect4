import numpy as np
import logging

class ExperienceReplay(object):
    def __init__(self, model_shape=(84,84,1), num_actions = 13, max_memory=1000, discount=.9):
        self.max_memory = max_memory
        self.num_actions = num_actions
        shape = (max_memory,) + model_shape
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
