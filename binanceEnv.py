import tensorflow as tf
import numpy as np
import pandas as pd

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts

from Visualization import TradingGraph as tg

tf.compat.v1.enable_v2_behavior()

    
class binanceEnv(py_environment.PyEnvironment):
    def __init__(self, fee = 0.001, starting_date = "2018-05-29", initial_balance = 10000, look_back_window = 40):
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(4,3,10), dtype=np.int32, minimum=0, maximum=10, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(4,5,40), dtype=np.float32, minimum=0, name='observation')
        self._state = np.zeros((4,5,40), dtype=np.float32)
        self._episode_ended = False
        self.initial_balance = initial_balance
        self.wallet = [self.initial_balance]
        self.look_back_window = look_back_window
        self.fee = fee
        self.starting_date = starting_date
        self.visual = None
        
        self.current_step = self.look_back_window
        self.moves = []
        ef = pd.ExcelFile("priceData.xls")
        self.dfs = []
        for sn in ef.sheet_names:
            print("loading sheet: "+sn)
            self.dfs.append(pd.read_excel('priceData.xls', sheet_name = sn))
            print("loaded: "+sn)
            self.moves.append([])
            self.wallet.append(0.0)
            
            
    def reset(self):
        """Return initial_time_step."""
        self.initial_time_step = ts.restart(self._state)
        self.wallet = [self.initial_balance]
        ef = pd.ExcelFile("priceData.xls")
        for sn in ef.sheet_names:
            self.wallet.append(0.0)
        self.current_step = self.look_back_window
        return ts.restart(self._state)

    def step(self, action):
        """Apply action and return new time_step."""
        data = []
        for df in self.dfs:
            data.append(np.array([df['volume'].values[range(self.current_step-self.look_back_window, self.current_step)],
                                  df['open'].values[range(self.current_step-self.look_back_window, self.current_step)],
                                  df['high'].values[range(self.current_step-self.look_back_window, self.current_step)],
                                  df['low'].values[range(self.current_step-self.look_back_window, self.current_step)],
                                  df['close'].values[range(self.current_step-self.look_back_window, self.current_step)]]))
        
        self._state = np.array(data)
        
        
        coin = action[0]
        action_type = action[1]
        amount = action[2]/10.0
            
        reward = 0
        
        if self.wallet[0]<0.01*self.initial_balance:
            self._episode_ended = True
            return ts.termination(self._state, reward)
        
        if action_type==0:
            #Buy coin
            current_price = data[coin][1, self.look_back_window-1]
            usd_val = amount*self.wallet[0]
            self.wallet[0] -= usd_val
            self.wallet[coin+1] += usd_val/current_price
            self.moves[coin].append(['buy', self.current_step, current_price])
            
        
        if action_type==1:
            #Sell coin
            current_price = data[coin][1, self.look_back_window-1]
            coin_val = amount*self.wallet[coin+1]
            self.wallet[coin+1] -= coin_val
            self.wallet[0] += coin_val*current_price
            self.moves[coin].append(['sell', self.current_step, current_price])
        
        
        self.current_step+=1
        return ts.transition(self._state, reward, 1.0)
    
    def render(self):
        if self.visual == None:
            self.visual = tg(self.dfs)
        else:
            self.visual.render(self.current_step, self.look_back_window, self.moves)
        
    def current_time_step(self):
        return self._current_time_step


    def observation_spec(self):
        """Return observation_spec."""
        return self._observation_spec

    def action_spec(self):
        return self._action_spec
   

    def _reset(self):
        return self.initial_time_step
 

    def _step(self, action):
        return self.step(action)
   

        
