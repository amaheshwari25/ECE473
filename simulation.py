from AMM import BettingMarket
from BaseTrader import Trader
import numpy as np
from matplotlib import pyplot as plt
import random

class Simulation:

    def __init__(self, markets):
        self.markets = markets
        self.betters = []
    
    def add_better(self, trader: Trader):
        self.betters.append(trader)
    

# 1 ROUND OF SIMULATION 
p0 = 0.4*random.random()+0.3
true_belief = [p0, 1-p0]
print('GROUND TRUTH:', true_belief)
# using same parameters from CMU paper Figure 7: uses alpha = 0.03 for LS-LMSR, beta = 150.27, q0 = [100, 100]
b1 = BettingMarket(2, [100, 100], 'LMSR', None, 150.27, true_belief)
b2 = BettingMarket(2, [100, 100], 'LSLMSR', 0.03, None, true_belief)

s = Simulation([b1, b2])

trader1 = Trader(1, 2, 10000000)
trader_p0 = min(max(np.random.normal(loc=p0, scale=0.2), 0), 1)
trader1.set_belief([trader_p0, 1-trader_p0])

trader2 = Trader(2, 2, 10000000)
trader2.set_belief([trader_p0, 1-trader_p0])
print()
bet1, cost1 = trader1.play(b1, verbose=True)
print("LMSR market trader: bet", bet1, "; cost", cost1)
print()
print('------')
print()
bet2, cost2 = trader2.play(b2, verbose=True)
print("LMSR market trader: bet", bet2, "; cost", cost2)


