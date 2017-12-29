from GenericDQN import GenericDQN
import time, random
import numpy as np
import logging

REF_STATI_FILE = 'GAME_ref_stati.npy'

class TeachDQN:

    def __init__(self, gameClass=None, do_learn=False, do_start_from_scratch=False, win_reward=1):
        self.gameClass = gameClass
        self.win_reward = win_reward

        self.do_learn = do_learn
        self.do_start_from_scratch = do_start_from_scratch

        self.model = None
        self.model_shape = None

    def get_model_action(self, game):
        shape = (1,) + self.model_shape
        move = self.model.predict(game.get_screen().get_status(player_to_play=1, shape=shape))
        return move[0]


    def do_monte_carlo_chosen_move(self, action, game, player):
        # norm the action vector to represent probabilities
        action = np.add(-action.min() + 1. / action.shape[0], action)
        action = np.multiply(1. / np.sum(action), action)

        # random choice with monte-carlo weights
        # until a valid move is found
        action_index = -1
        skipFirst = True
        while skipFirst or not game.set_stone_by_index(action_index, player):
            skipFirst = False
            dice = random.random()
            x = 0
            for i in range(action.shape[0]):
                x += action[i]
                if dice <= x:
                    action_index = i
                    break
        return action_index


    def do_best_move(self, game, player):
        action = self.get_model_action(game)

        valid_move = False
        action_index = -1
        while not valid_move:
            action_index = np.argmax(action)
            valid_move = game.set_stone_by_index(action_index, player)

            # invalidate this action for argmax
            action[action_index] = action.min() - 1
        return action_index


    def play_game(self, game, epsilon = 0.0, verbose = 0):
        player = 1
        while not game.is_over():
            move_index = -1
            # with chance epsilon: play a random move
            if random.random() < 1 - epsilon:
                # norm action vector
                action = self.get_model_action(game)
                move_index = self.do_monte_carlo_chosen_move(action, game, player)
                if verbose > 0:
                    print('Played move: ', game.index_to_action(move_index))
            else:
                game.perform_random_move(player=player)
            player *= -1

    def load_model(self, model_class, model_file='generic_model.h5', single_actions=False):
        #self.model = DQN_TTT_Model.DQN_TTT_Model.create_model_fcn()
        self.model = model_class.create_model()
        self.MODEL_FILE = model_file
        self.model_shape = model_class.get_model_shape()
        self.single_actions = single_actions
        logging.debug("model_shape: " + str(self.model_shape))

        if not self.do_start_from_scratch:
            self.model.load_weights(self.MODEL_FILE)


        #if self.do_learn and self.do_start_from_scratch:
        #    # play_random_game_as_reference
        #    NO_REF_STATES=100
        #    shape = (NO_REF_STATES,) + self.model_shape
        #    self.reference_stati = np.zeros(shape)
        #    for id in range(NO_REF_STATES):
        #        game = self.gameClass()
        #        self.play_game(game, epsilon=1.0)
        #        for a in range(0,2):
        #            x = random.randint(0, len(game.get_screens())-1)
        #            reference_screen = game.get_screen(x)
        #            self.reference_stati[id] = reference_screen.get_status(player_to_play=1)
        #
        #    np.save(REF_STATI_FILE, self.reference_stati)
        #else:
        #    self.reference_stati = np.load(REF_STATI_FILE)

    def learn(self):
        ITERATIONS=2

        id = 0
        if self.do_learn:
            q_progress_list = []
            for iteration in range(ITERATIONS):
                logging.info("  Starting iteration %s / %s" % (iteration, ITERATIONS-1))
                games = []
                for id in range(1000):
                    # Start testing the game
                    game = self.gameClass(win_reward=self.win_reward)
                    games.append(game)

                    self.play_game(game, epsilon = 0.5 - 0.5*iteration/(ITERATIONS-1.))

                num_actions = self.gameClass.get_numActions()
                #size = self.gameClass.get_size()
                dqn_learner = GenericDQN(num_actions = num_actions, single_actions=self.single_actions, q_learning_epochs=3, fixed_learning_epochs=1)
                dqn_learner.load_games(games, input_shape=self.model_shape)

                q_progress = dqn_learner.learn(model=self.model, model_file=self.MODEL_FILE, start_from_scratch=self.do_start_from_scratch, input_shape=None)
                print(q_progress)
                q_progress_list.append(q_progress)

            print(q_progress_list)

    def play(self):
        n = 0
        won = 0
        lost = 0
        while n < 15:
            n += 1

            game = self.gameClass(win_reward=self.win_reward)
            self.play_game(game, verbose=0, epsilon=0.0)

            winner = game.get_winner()
            if winner == 1:
                won += 1
            if winner == -1:
                lost += 1
            #print 'Game over. Winner: ', winner
            #print game.get_screen().board

        if n>0:
            win_quotient = won/1./n
            print('Won: ', won, 'Lost: ', lost, win_quotient)

