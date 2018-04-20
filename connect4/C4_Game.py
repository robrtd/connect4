import C4_Board as C4B
import numpy as np
import random

class C4_Game:
    numActions = 7

    def __init__(self, startPlayer=1, win_reward=1, channels=1):
        self.channels = channels
        self.board = []
        self.board.append(C4B.C4_Board(channels=self.channels))
        self.actions = [None]
        self.rewards = [0]
        self.move = 0
        self.player = startPlayer
        self.win_reward = win_reward

    def show(self, move = None):
        if not move:
            move = self.move

        print(self.player, self.move)
        self.board[move].show()

    def copy(self):
        g2 = C4_Game(channels=self.channels, win_reward=self.win_reward)
        for b in self.board[1:]:
            g2.board.append(b.copy())
        g2.actions = list(self.actions)
        g2.rewards = list(self.rewards)
        g2.move = self.move
        g2.player = self.player
        return g2


    def copy_board(self, move = None):
        if not move:
            move = self.move
        return self.board[move].copy()

    def perform_random_move(self, player = None):
        if not player:
            player = self.player

        if self.is_over():
            return False

        is_valid = False
        while not is_valid:
            b = self.board[self.move].copy()
            move = random.randint(0, 6)
            is_valid = b.set(move, player)

        return self.set_stone_by_index(move)

    def set_stone_by_index(self, index, player=None):
        if not player:
            player = self.player
        assert(player == self.player)
        if self.is_over():
            return False
        next_board = self.board[self.move].copy()
        if not next_board.set(index, self.player):
            return False

        self.actions[self.move] = index
        self.rewards[self.move] = next_board.get_winner()*self.win_reward

        self.actions.append(None)
        if next_board.is_over():
            self.rewards.append(self.rewards[self.move])
        else:
            self.rewards.append(0)
        self.board.append(next_board)
        self.player *= -1
        self.move += 1
        return True

    def get_reward(self, screen=None, player=None):
        if screen is None:
            screen = self.move
        f = 1
        if player is not None:
            f = player
        return f * self.rewards[screen]


    def get_action_vector(self, screen):
        vec = np.zeros(self.numActions)
        vec[self.actions[screen]] = 1
        return vec

    def get_gameover(self, screen):
        return screen >= len(self.board)-2

    def load_experience(self, experience, max_memory, input_shape=None):
        n = 0
        player = 1
        for screen in self.board:
            experience.remember(n
                                , state=screen.get_status(player_to_play=1, shape=input_shape)
                                , action=self.get_action_vector(n)
                                , reward=self.get_reward(n, player=player)
                                , game_over=self.get_gameover(n))

            if self.get_gameover(n):
                return

            player *= -1
            n += 1
            if n >= max_memory:
                return


    def get_screens(self):
        return range(len(self.board))


    def get_screen(self, move_index = None):
        if move_index is None:
            move_index = self.move
        return self.board[move_index]


    def set(self, pos):
        return self.set_stone_by_index(pos - 1)


    def get_winner(self):
        return self.board[self.move].get_winner()

    def is_over(self):
        return self.board[self.move].is_over()

    @staticmethod
    def get_numActions():
        return 1*C4_Game.numActions

    #@staticmethod
    #def get_size():
    #    return (6,C4_Game.numActions)
