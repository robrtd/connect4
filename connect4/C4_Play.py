import C4_Game as C4G
import random
from TeachDQN import TeachDQN
from C4_DQN_Model import C4_DQN_Model

def get_computer_player_id():
    p = 0
    while p == 0:
        p = random.randint(-1,1)
    return p


def ask_pos():
    moves = range(1,8)
    print("Which pos (1-7)? ")
    inp = ''
    while inp not in moves:
        try:
            inp = int(input())
        except ValueError:
            inp = ''
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

COMPUTERPLAYERID=get_computer_player_id()
game = C4G.C4_Game()

computer_player = TeachDQN()
computer_player.load_model(model_class=C4_DQN_Model, model_file='game_dqn/c4_model_deep.h5')

while not game.is_over():
    if COMPUTERPLAYERID == 1:
        computer_player.do_best_move(game, 1)
        if game.is_over():
            break
    game.show()
    while not game.set(ask_pos()):
        pass
    if game.is_over():
        break
    #while not game.set(get_computer_move(game.copy_board(), -1*STARTPLAYER)):
    if COMPUTERPLAYERID == -1:
        computer_player.do_best_move(game, -1)
game.show()
print(game.get_winner())

