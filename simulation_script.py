from AMM import BettingMarket
from BaseTrader import Trader
from simulation import Simulation
import numpy as np
from matplotlib import pyplot as plt
import random

# 1. Run perfect traders simulation
s = Simulation()
ground_truth = s.draw_unif_ground_truth(0.3, 0.7)
markets = s.create_market_comp([100, 100], 'LMSR', 'LSLMSR', 150.27, 0.03, ground_truth)
s.perfect_trader_sim(5, 10000000, markets, verbose=True)
