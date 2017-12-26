import C4_Board as C4B

class C4_Game:

    def __init__(self, startPlayer = 1):
        self.board = []
        self.board.append(C4B.C4_Board())
        self.move = 0
        self.player = startPlayer

    def show(self, move = None):
        if not move:
            move = self.move

        print(self.player, self.move)
        self.board[move].show()

    def copy_board(self, move = None):
        if not move:
            move = self.move
        return self.board[move].copy()

    def set(self, pos):
        if self.is_over() or not self.board[self.move].set(pos - 1, self.player):
            return False

        if self.is_over():
            return True

        self.board.append(self.board[self.move].copy())
        self.player *= -1
        self.move += 1
        return True

    def get_winner(self):
        return self.board[self.move].get_winner()

    def is_over(self):
        return self.board[self.move].is_over()





