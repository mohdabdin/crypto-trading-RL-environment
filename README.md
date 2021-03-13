This is a crypto trading RL project that's still in progress, The aim of the project is to apply reinforcement learning
in a complex trading environment, as most of the RL trading environments I've seen simplify the problem to one trading pair
I decide to try and do 4 different pairs based on the intuition that assets from within the same market price changes are
correlated in a certain way which this project aims to explore.

Currently, the environment hold the following observation and action specs:
  Action spec: (3,) to represent the coin chosen, the action(buy/sell/hold), and amount
  Observation space: (4, 5, 40) where 4 is the number of trading pairs, 5 is the OHCLV values, and 40 is the look back period
  
  
You can find the full implementation of this project where I go through each detail in this article:
https://levelup.gitconnected.com/a-complex-reinforcement-learning-crypto-trading-environment-in-python-134f3faf0d7a
  
