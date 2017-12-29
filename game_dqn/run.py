import TeachDQN
from C4_Game import C4_Game
from C4_DQN_Model import C4_DQN_Model
import logging

logging.basicConfig(level=logging.DEBUG,format='%(levelname)s:%(asctime)s %(message)s')

do_learn=True
do_start_from_scratch=True

teacher = TeachDQN.TeachDQN(gameClass=C4_Game, do_learn=do_learn, do_start_from_scratch=do_start_from_scratch, win_reward=10)

teacher.load_model(model_class=C4_DQN_Model, model_file='c4_model_deep.h5', single_actions=False)

if do_learn:
    logging.info("Starting to learn...")
    teacher.learn()
    logging.info("Learning is done.")
else:
    teacher.play()