import C4_Game as C4G
import random
from TeachDQN import TeachDQN
from C4_DQN_Model import C4_DQN_Model
import logging

logging.basicConfig(level=logging.DEBUG,format='%(levelname)s:%(asctime)s %(message)s')

EXECUTE_TESTS=False

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


def get_computer_move(game, player):
    # Stupid KI that plays random moves
    # unless it could win directly
    # or lose directly (i.e. places the 4-th stone correctly)
    for run in range(2):
        for move in range(7):
            b = game.copy_board()
            b.set(move, player)
            if b.get_winner() != 0:
                return move
        player *= -1

    b = game.copy_board()
    move = -1
    while True:
        move = random.randint(0, 6)
        if b.set(move, player):
            break
    return move

def perform_moves(white, black):
    game = C4G.C4_Game(channels=C4_DQN_Model.get_channels())
    for i in range(len(white)):
        game.set_stone_by_index(white[i], player=1)
        if i < len(black):
            game.set_stone_by_index(black[i], player=-1)
    for i in range(len(white), len(black)):
        game.set_stone_by_index(black[i], player=-1)
    return game


computer_player = TeachDQN()
#computer_player.load_model(model_class=C4_DQN_Model, model_file='../game_dqn/c4_model_deep_9-81_channel2_testr10.h5')
computer_player.load_model(model_class=C4_DQN_Model, model_file='../game_dqn/c4_model_deep_channel2_r10-i220.h5')
#computer_player.load_model(model_class=C4_DQN_Model, model_file=None)

if EXECUTE_TESTS:
    # 1
    game = perform_moves(white=[3,2,4,4], black=[3,2,5])
    model_action = computer_player.get_model_action(game=game)
    print("Should play 1 and estimates: ", model_action)
    print("Should play 1 and played: ", computer_player.do_best_move(game, -1))

    # 2
    game = perform_moves(white=[3, 3, 3], black=[4, 4])
    print("Should play 3 and played: ", computer_player.do_best_move(game, -1))

    #3 play some games against an easy half-random KI
    win_cnt = 0
    draw_cnt = 0
    lost_cnt = 0
    for g in range(500):
        game = C4G.C4_Game(channels=C4_DQN_Model.get_channels())
        model_player = get_computer_player_id()
        current_player = 1
        while not game.is_over():
            if model_player==current_player:
                computer_player.do_best_move(game, model_player)
            else:
                move = get_computer_move(game, current_player)
                success = game.set_stone_by_index(move, current_player)
            current_player *= -1
        if game.get_winner() == model_player:
            win_cnt += 1
        elif game.get_winner() == 0:
            draw_cnt += 1
        else:
            lost_cnt += 1
    print("Model performance (wins/draw/lost): ", win_cnt, draw_cnt, lost_cnt)


game = C4G.C4_Game(channels=C4_DQN_Model.get_channels(), win_reward=10)
#COMPUTERPLAYERID=get_computer_player_id()
COMPUTERPLAYERID=1

while not game.is_over():
    if COMPUTERPLAYERID == 1:
        #computer_player.do_best_move(game, 1)
        move, q_val = computer_player.find_best_move(game, player=1, depth=3, search_width=2)
        print("Computermove: %d; q_val: %f" % (move, q_val))
        game.set_stone_by_index(move, COMPUTERPLAYERID)
        if game.is_over():
            break
    game.show()
    while not game.set(ask_pos()):
        pass
    if game.is_over():
        break
    #while not game.set(get_computer_move(game.copy_board(), -1*STARTPLAYER)):
    if COMPUTERPLAYERID == -1:
        move = computer_player.do_best_move(game, -1)
        print("Computermove: %d" % move)
game.show()
print(game.get_winner())

