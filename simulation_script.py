from AMM import BettingMarket
from BaseTrader import Trader
from simulation import Simulation
import numpy as np
from matplotlib import pyplot as plt
import random

# 1. Run perfect traders simulation
NTRADERS = 10
a1, r1, o1, a2, r2, o2 = [], [], [], [], [], []


def normalize_price(price):
    tot = price[0]+price[1]
    return [price[0] / tot, price[1] / tot]


noise_delta = 0.05
noise = 0.
for i in range(150):
    s = Simulation()
    ground_truth = s.draw_unif_ground_truth(0.1, 0.2)
    # ground_truth = [0.1, 0.9]
    markets = s.create_market_comp(
        [100, 100], 'LMSR', 'LSLMSR', 150.27, 0.03, ground_truth)
    trader_beliefs = []
    noise = i * 0.1
    for i in range(NTRADERS):
        trader_beliefs.append(s.draw_unif_ground_truth(
            max(ground_truth[0]-noise, 0.), min(ground_truth[0]+noise, 1.)))
        # noise -= noise_delta
    rev1, price1, out1, rev2, price2, out2 = s.perfect_trader_sim(
        NTRADERS, 10000000, markets, trader_beliefs, verbose=False)

    # print('------------------------')
    # print(ground_truth)
    # for t in s.getLMSRtraders():
    #     print("trader {} has belief {}".format(t.id, t.belief[0]))
    # print("Revenue: ", rev1)
    # for t in s.getLSLMSRtraders():
    #     print("trader {} has belief {}".format(t.id, t.belief[0]))
    # print("Revenue: ", rev2)

    price1 = normalize_price(price1)
    price2 = normalize_price(price2)
    LMSR_accuracy = 1-abs(price1[0]-ground_truth[0])
    LSLMSR_accuracy = 1-abs(price2[0]-ground_truth[0])
    a1.append(LMSR_accuracy)
    a2.append(LSLMSR_accuracy)
    r1.append(rev1)
    r2.append(rev2)
    o1.append(out1)
    o2.append(out2)

    print("LMSR accuracy is ", LMSR_accuracy)
    print("LS-LMSR accuracy is ", LSLMSR_accuracy)
    # print("LMSR revenue is ", rev1)
    # print("LS-LMSR revenue is ", rev2)

plt.title("Price vs. Accuracy Tradeoff (LMSR)")
plt.xlabel("Price accuracy")
plt.ylabel("Revenues")
colors = ['red' if o == 0 else 'blue' for o in o1]
# print(o1, colors)
c2 = ['yellow' if o == 0 else 'green' for o in o2]

# plt.figure(1)
plt.scatter(a1, r1, c=colors)
# plt.figure(2)
plt.scatter(a2, r2, c=c2)
plt.show()
