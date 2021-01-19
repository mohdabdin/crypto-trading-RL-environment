import numpy as np
from binanceEnv import binanceEnv
import random

env = binanceEnv()
 
for _ in range(0,100):
    random_action = np.random.choice(np.arange(0, 3), p=[0.1, 0.1, 0.8])
    random_coin = random.randint(0,3)
    amount = 2
    action_w = np.array([int(random_coin), int(random_action), amount])
    env.step(action_w)
    env.render()