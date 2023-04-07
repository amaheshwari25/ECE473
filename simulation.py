from AMM import BettingMarket
from BaseTrader import Trader
import numpy as np
from matplotlib import pyplot as plt
import random

class Simulation:

    def __init__(self):
        self.betters = []
    
    # def add_better(self, trader: Trader):
    #     self.betters.append(trader)

    def draw_unif_ground_truth(self, low, high):
        p0 = low+(high-low)*random.random()
        return [p0, 1-p0]

    def create_market_comp(self, init_quant, msr1, msr2, msr1_const, msr2_const, ground_truth):
        b1 = BettingMarket(2, init_quant, msr1, (None if msr1 == "LMSR" else msr1_const), (None if msr1 == "LS-LMSR" else msr1_const), ground_truth)
        b2 = BettingMarket(2, init_quant, msr2, (None if msr2 == "LMSR" else msr2_const), (None if msr2 == "LS-LMSR" else msr2_const), ground_truth)
        return [b1, b2]

    def perfect_trader_sim(self, ntraders, trader_money, markets, verbose=False):
        print()
        print()
        b1, b2 = markets[0], markets[1]
        assert(b1.true_dist == b2.true_dist)
        print('GROUND TRUTH:', b1.true_dist)
        print('INITIAL PRICE: LMSR', [b1.get_price(0, b1.q), b1.get_price(1, b1.q)])
        print('INITIAL PRICE: LS-LMSR', [b2.get_price(0, b2.q), b2.get_price(1, b2.q)])
        print()

        traders_b1 = []
        bets_b1 = []
        costs_b1 = []
        traders_b2 = []
        bets_b2 = []
        costs_b2 = []

        for i in range(ntraders):
            traderv1 = Trader(i, 2, trader_money)
            traderv1.set_belief(b1.true_dist)
            traders_b1.append(traderv1)
            traderv2 = Trader(i, 2, trader_money)
            traderv2.set_belief(b1.true_dist)
            traders_b2.append(traderv2)

            print("LMSR market trader", i, ":")
            bet1, cost1 = traderv1.play(b1, verbose=verbose)
            bets_b1.append(bet1)
            costs_b1.append(cost1)
            print("Final: bet:", bet1, "cost:", cost1)
            print('------')

            print("LS-LMSR market trader", i, ":")
            bet2, cost2 = traderv2.play(b2, verbose=verbose)
            bets_b2.append(bet2)
            costs_b2.append(cost2)
            print("Final: bet:", bet2, "cost:", cost2)
            print()
        print('==========')
        print('LMSR market: ')
        b1.get_market_state()
        print()
        print('LS-LMSR market')
        b2.get_market_state()
    









# TBD: more strategic simulation
#   - update the quantities to get to a reasonable "level" first so 1 trader does not extract all value? or fine for 1 trader to extract all?
#   - make belief a function of current state + noisy signal (counteracts possible max value extraction from first player): weighted

# print()
# print()
# # 1. Draw ground truth uniformly from [0.3, 0.7] 
# p0 = 0.4*random.random()+0.3
# true_belief = [p0, 1-p0]
# print('GROUND TRUTH:', true_belief)

# # 2. Establish 2 betting markets (LMSR, LS-LMSR)
# # using same parameters from CMU paper Figure 7: uses alpha = 0.03 for LS-LMSR, beta = 150.27, q0 = [100, 100]
# # b1 = BettingMarket(2, [100, 100], 'LMSR', None, 150.27, true_belief)
# b1 = BettingMarket(2, [100, 100], 'LMSR', None, 150.27, true_belief)
# b2 = BettingMarket(2, [100, 100], 'LSLMSR', 0.03, None, true_belief)
# print('INITIAL PRICE: LMSR', [b1.get_price(0, b1.q), b1.get_price(1, b1.q)])
# print('INITIAL PRICE: LS-LMSR', [b2.get_price(0, b2.q), b2.get_price(1, b2.q)])
# print()


# s = Simulation([b1, b2])

# ntraders = 5
# traders_v1 = []
# bets_v1 = []
# costs_v1 = []
# traders_v2 = []
# bets_v2 = []
# costs_v2 = []

# STDEV = 0
# for i in range(ntraders):
#     # draw this trader's belief
#     trad_p0 = min(max(np.random.normal(loc=p0, scale=STDEV), 0), 1)

#     traderv1 = Trader(i, 2, 10000000)
#     traderv1.set_belief([trad_p0, 1-trad_p0])
#     traderv2 = Trader(i, 2, 10000000)
#     traderv2.set_belief([trad_p0, 1-trad_p0])

#     bet1, cost1 = traderv1.play(b1, verbose=False)
#     bets_v1.append(bet1)
#     costs_v1.append(cost1)
#     print("LMSR market trader", i, " bet:", bet1, "cost:", cost1)
#     print('------')
#     bet2, cost2 = traderv2.play(b2, verbose=True)
#     bets_v2.append(bet2)
#     costs_v2.append(cost2)
#     print("LS-LMSR market trader", i, " bet:", bet2, "cost:", cost2)
#     print()

# print('==========')
# print('LMSR market: ')
# b1.get_market_state()
# print()
# print('LS-LMSR market')
# b2.get_market_state()




# 1 ROUND OF SIMULATION 
# trader1 = Trader(1, 2, 10000000)
# trader1.set_belief([trader_p0, 1-trader_p0])
# trad_p0 = min(max(np.random.normal(loc=p0, scale=0.2), 0), 1)

# trader2 = Trader(2, 2, 10000000)
# trader2.set_belief([trader_p0, 1-trader_p0])
# print()
# bet1, cost1 = trader1.play(b1, verbose=True)
# print("LMSR market trader: bet", bet1, "; cost", cost1)
# b1.get_market_state()
# print()
# print('------')
# print()
# bet2, cost2 = trader2.play(b2, verbose=True)
# print("LS-LMSR market trader: bet", bet2, "; cost", cost2)
# b2.get_market_state()


