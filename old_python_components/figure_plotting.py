from AMM import BettingMarket
from BaseTrader import Trader
import numpy as np
from matplotlib import pyplot as plt
import random

# CMU FIGURE 1
# bm_y250 = BettingMarket(2, [0, 250], "LSLMSR", alpha=0.05, beta=None, true_dist=[0.8, 0.2])
# bm_y500 = BettingMarket(2, [0, 500], "LSLMSR", alpha=0.05, beta=None, true_dist=[0.8, 0.2])
# bm_y750 = BettingMarket(2, [0, 750], "LSLMSR", alpha=0.05, beta=None, true_dist=[0.8, 0.2])
# bm = [bm_y250, bm_y500, bm_y750]

# x_vals = np.arange(0, 1000, 5)
# traders = [Trader(x, 2, 10000000000) for x in range(3)]
# prices = [[], [], []]

# for i in range(3):
#     for x in x_vals:
#         bm[i].submit_bet(traders[i], [x-bm[i].q[0], 0])
#         prices[i].append(bm[i].get_price(0, bm[i].q))

# plt.plot(x_vals, prices[0], label='q_y = 250')
# plt.plot(x_vals, prices[1], label='q_y = 500')
# plt.plot(x_vals, prices[2], label='q_y= 750')

# plt.xlabel(r'$q_x$')
# plt.ylabel(r'$p_x(q)$')
# plt.title(r'Price variation as a function of complement quantity, $\alpha=0.05$')
# plt.legend()
# plt.savefig('cmu_fig1.png')
# plt.close()

# CMU FIGURE 2/3
# x_vals = np.arange(1, 1000)
# bm_1 = BettingMarket(2, [1, 1], "LSLMSR", alpha=0.05, beta=None, true_dist=[0.8, 0.2])
# inf_trader = Trader(999, 2, 10000000000000)
# costs_1 = []
# for x in x_vals:
#     costs_1.append(bm_1.submit_bet(inf_trader, [1, 0]))
#     bm_1.submit_bet(inf_trader, [0, 1])
# plt.plot(x_vals, costs_1)
# plt.xlim(1, 1000)
# plt.xlabel('Quantity outstanding (for both items)')
# plt.ylabel('Cost of unit bet (of 1st item)')
# plt.xscale('log')
# plt.title(r'Cost of unit bet vs quantity outstanding, $q_1 = q_2$')
# plt.savefig('cmu_fig2.png')
# plt.close()

# bm_2 = BettingMarket(2, [1.5, 1], "LSLMSR", alpha=0.05, beta=None, true_dist=[0.8, 0.2])
# inf_trader = Trader(999, 2, 10000000000000)
# costs_2 = []
# for x in x_vals:
#     costs_2.append(bm_2.submit_bet(inf_trader, [1, 0]))
#     bm_2.submit_bet(inf_trader, [0.5, 1])
# plt.plot(x_vals, costs_2)
# plt.xlim(1, 1000)
# plt.xlabel('Quantity outstanding (of 2nd item)')
# plt.ylabel('Cost of unit bet (of 1st item)')
# plt.xscale('log')
# plt.title(r'Cost of unit bet vs quantity outstanding, $q_1 = 1.5q_2$')
# plt.savefig('cmu_fig3-based.png')
# plt.close()


# FIGURE: variance with alpha 
# alphas = [0.01, 0.05, 0.1, 0.2, 0.5]
# x_vals = np.arange(1, 1000)

# for alph in alphas:
#     bm = BettingMarket(2, [1, 1], "LSLMSR", alpha=alph, beta=None, true_dist=[0.8, 0.2])
#     inf_trader = BaseTrader(999, 2, 10000000000000)
#     costs = []
#     for x in x_vals:
#         costs.append(bm.submit_bet(inf_trader, [1, 0]))
#         bm.submit_bet(inf_trader, [0, 1])
#     plt.plot(x_vals, costs, label=(r'$\alpha=$'+str(alph)))

# plt.xlim(1, 1000)
# plt.xlabel('Quantity outstanding (for both items)')
# plt.ylabel('Cost of unit bet (of 1st item)')
# plt.xscale('log')
# plt.title(r'Cost of unit bet vs quantity outstanding, $q_1 = q_2$')
# plt.legend()
# plt.savefig('alpha_fig.png')
# plt.close()