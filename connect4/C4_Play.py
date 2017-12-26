import C4_Game as C4G
import random

STARTPLAYER=-1

def ask_pos():
    moves = range(1,8)
    print("Which pos (1-7)? ")
    inp = ''
    while inp not in moves:
        inp = input()
    return inp

def get_computer_move(board, player):
    for run in range(2):
        for move in range(7):
            b = board.copy()
            b.set(move, player)
            if b.get_winner() != 0:
                return move + 1
        player *= -1

    return random.randint(1, 7)

game = C4G.C4_Game()
if STARTPLAYER == -1:
    game.set(4)
game.show()
while not game.is_over():
    while not game.set(ask_pos()):
        pass
    if game.is_over():
        break
    while not game.set(get_computer_move(game.copy_board(), -1*STARTPLAYER)):
        pass
    game.show()
game.show()
print(game.get_winner())

