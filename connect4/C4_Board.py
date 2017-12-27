import numpy as np

class C4_Board:
    def __init__(self):
        self.board = np.zeros((6,7))
        self.last_move_player = None


    def copy(self):
        new_board = C4_Board()
        new_board.board = self.board.copy()
        new_board.last_move_player = self.last_move_player
        return new_board

    def show(self):
        # NOTE: accessing stone[-1] returns the last element
        stone = [' ','X','O']
        print('_________________')
        for x in range(5,-1,-1):
            a = ['.' for _ in range(7)]
            str = '| '
            for i in range(7):
                a[i] = stone[int(self.board[x,i])]
                str += stone[int(self.board[x,i])] + ' '
            str += '|'
            print(str)
        print('--1-2-3-4-5-6-7--')

    def set(self, pos, player):
        for x in range(6):
            if self.board[x,pos] == 0:
                self.board[x,pos] = player
                self.last_move_player = player
                return True
        return False

    def _is_move_possible(self):
        b = self.copy()
        b.board = b.board*b.board
        return np.min(b.board) == 0

    def is_over(self):
        return self.get_winner() != 0 or not self._is_move_possible()

    def get_winner(self):
        winner = self._check_4_in_col_()
        if winner != 0:
            return winner

        winner = self._check_4_in_row_()
        if winner != 0:
            return winner

        winner = self._check_4_in_diag_()
        return winner

    def get_status(self, player_to_play=None, shape=None):
        # display board, as if it was $player_to_play's move
        if player_to_play is None or player_to_play != self.last_move_player:
            b = self.board
        else:
            b = np.multiply(-1, self.board)

        #if shape is None:
        #    shape = (self.sizeX, self.sizeY, 1)
        #return b.reshape(shape)
        return b


    def _check_4_in_diag_(self):
        for r0 in range(3):
            for c0 in range(4):
                stone = self.board[r0,c0]
                if stone == 0:
                    continue
                four = True
                for d in range(4):
                    if self.board[r0+d,c0+d] != stone:
                        four = False
                        break
                if four:
                    return stone
        for r0 in range(3):
            for c0 in range(3,7):
                stone = self.board[r0, c0]
                if stone == 0:
                    continue
                four = True
                for d in range(4):
                    if self.board[r0 + d, c0 - d] != stone:
                        four = False
                        break
                if four:
                    return stone
        return 0

    def _check_4_in_col_(self):
        for row in range(6):
            for x in range(4):
                stone = self.board[row,x]
                if stone == 0:
                    continue
                four = True
                for col in range(x, x+4):
                    if self.board[row, col] != stone:
                        four = False
                        break
                if four:
                    return stone
        return 0

    def _check_4_in_row_(self):
        for col in range(7):
            for x in range(3):
                stone = self.board[x, col]
                if stone == 0:
                    continue
                four = True
                for row in range(x, x + 4):
                    if self.board[row, col] != stone:
                        four = False
                        break
                if four:
                    return stone
        return 0
