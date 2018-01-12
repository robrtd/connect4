== generic DQN solution for board games

|T| <-- GameX <-- Screens/Boards
|e|
|a|
|c|
|h|
|D|
|Q| <-- GenericDQN <-- ExperienceReplay
|N|


== Evaluations

| Model | Reward | Epsilon | 1k-Iterations | Score |
| Deep  | 1      | 0.5     | 220           | 70%   |
| Deep  | 10     | 0.5     |   0           |  0%   |
| Deep  | 10     | 0.5     | 220           | 80%   |
| Deep  | 10     | 0.5     | 420           | 80%   |
| Deep  | 10     | 0.5     | 820           | 70%   | 
| Deep  | 10     | 0.1     | 820           | < 50% |


(1) The model does improve signifiantly. I.e. it is not all wrong ;)

(2) As the Score does not improve beyond a certain point: the model may be limited. 