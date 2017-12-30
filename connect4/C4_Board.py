import numpy as np

class C4_Board:
    def __init__(self, channels=1):
        self.channels = channels
        self.board = np.zeros((6,7, self.channels))
        self.last_move_player = None


    def copy(self):
        new_board = C4_Board(channels=self.channels)
        new_board.board = self.board.copy()
        new_board.last_move_player = self.last_move_player
        return new_board

    def get_stone_type(self, row, col):
        if self.channels == 1:
            return int(self.board[row, col, 0])
        elif self.channels == 2:
            if self.board[row,col,0] > 0:
                return 1
            if self.board[row,col,1] > 0:
                return -1
            return 0
        return 0

    def _set_stone_type(self, row, col, player):
        if self.channels == 1:
            self.board[row, col, 0] = player
        elif self.channels == 2:
            if player == 1:
                self.board[row, col, 0] = 1
            elif player == -1:
                self.board[row, col, 1] = 1

    def show(self):
        # NOTE: accessing stone[-1] returns the last element
        stone = [' ','X','O']
        print('_________________')
        for x in range(5,-1,-1):
            str = '| '
            for i in range(7):
                str += stone[self.get_stone_type(x,i)] + ' '
            str += '|'
            print(str)
        print('--1-2-3-4-5-6-7--')

    def set(self, pos, player):
        assert(pos >= 0 and pos < 7)
        for x in range(6):
            if np.sum(self.board[x,pos,:]) == 0:
                #self.board[x,pos] = player
                self._set_stone_type(x, pos, player)
                self.last_move_player = player
                return True
        return False

    def _is_move_possible(self):
        board = self.board.copy()
        if self.channels == 1:
            board = board*board
            return np.min(board) == 0
        if self.channels == 2:
            moves = np.sum(board)
            return moves < 6*7

    def is_over(self):
        return not self._is_move_possible() or self.get_winner() != 0

    def get_winner(self):
        winner = self._check_4_in_col_()
        if winner != 0:
            return winner

        winner = self._check_4_in_row_()
        if winner != 0:
            return winner

        winner = self._check_4_in_diag_()
        return winner

    def get_status(self, player_to_play=None, shape=(6, 7, 1)):
        # display board, as if it was $player_to_play's move
        if self.channels == 1:
            if player_to_play is None or player_to_play != self.last_move_player:
                b = self.board
            else:
                b = np.multiply(-1, self.board)
            # TODO: remove reshape, as we now have a separate channel anyway
            return b.reshape(shape)

        if self.channels == 2:
            if player_to_play is None or player_to_play != self.last_move_player:
                b = self.board
            else:
                b = np.zeros((6,7,2))
                b[:,:,0] = self.board[:,:,1]
                b[:,:,1] = self.board[:,:,0]
            return b.reshape(shape)

        return None

    def _check_4_in_diag_(self):
        for r0 in range(3):
            for c0 in range(4):
                stone = self.get_stone_type(r0,c0)
                if stone == 0:
                    continue
                four = True
                for d in range(4):
                    if self.get_stone_type(r0+d,c0+d) != stone:
                        four = False
                        break
                if four:
                    return stone
        for r0 in range(3):
            for c0 in range(3,7):
                stone = self.get_stone_type(r0, c0)
                if stone == 0:
                    continue
                four = True
                for d in range(4):
                    if self.get_stone_type(r0 + d, c0 - d) != stone:
                        four = False
                        break
                if four:
                    return stone
        return 0

    def _check_4_in_col_(self):
        for row in range(6):
            for x in range(4):
                stone = self.get_stone_type(row,x)
                if stone == 0:
                    continue
                four = True
                for col in range(x, x+4):
                    if self.get_stone_type(row, col) != stone:
                        four = False
                        break
                if four:
                    return stone
        return 0

    def _check_4_in_row_(self):
        for col in range(7):
            for x in range(3):
                stone = self.get_stone_type(x, col)
                if stone == 0:
                    continue
                four = True
                for row in range(x, x+4):
                    if self.get_stone_type(row, col) != stone:
                        four = False
                        break
                if four:
                    return stone
        return 0
