from AMM import BettingMarket
from BaseTrader import Trader
from simulation import Simulation
import numpy as np
from matplotlib import pyplot as plt
import random


# 1. Run a simple noisy information simulation
s = Simulation()
ground_truth = s.draw_unif_ground_truth(0.6, 0.8)
init_quant = [100, 100]
alpha = 0.03
markets = s.create_market_comp(init_quant, 'LMSR', 'LSLMSR', s.compute_b(alpha, init_quant)[0], alpha, ground_truth)
print(s.noisyinfo_sim(10, 10000000, markets, silence=False, verbose=True))