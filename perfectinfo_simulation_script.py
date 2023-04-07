from AMM import BettingMarket
from BaseTrader import Trader
from simulation import Simulation
import numpy as np
from matplotlib import pyplot as plt
import random

# 1. Run single perfect traders simulation
# s = Simulation()
# ground_truth = s.draw_unif_ground_truth(0.3, 0.7)
# markets = s.create_market_comp([100, 100], 'LMSR', 'LSLMSR', 150.27, 0.03, ground_truth)
# s.perfect_trader_sim(5, 10000000, markets, silence=True)


# 2. Compute "perfect-traders" simulation plots: how does revenue vary against alpha (/corresponding b)
vigs = np.arange(0.02, 0.2, 0.01)
alphas = vigs/(2*np.log(2))

init_quant = [100, 100]
N_TRIALS = 100
N_TRADERS = 10

acc_LS = []
acc_LMSR = []
rev_LS = []
rev_LMSR = []
rev_stdevs_LMSR = []
rev_stdevs_LS = []

exprev_LMSR = []
exprev_LS = []
exprev_stdevs_LMSR = []
exprev_stdevs_LS = []

wcls= []

for alpha in alphas:
    s = Simulation()
    acc_LS_temp = []
    acc_LMSR_temp = []
    rev_LS_temp = []
    rev_LMSR_temp = []
    exprev_LMSR_temp = []
    exprev_LS_temp = []

    b, worst_case_loss = s.compute_b(alpha, init_quant)
    # print(b, worst_case_loss)
    wcls.append(-worst_case_loss)

    for i in range(N_TRIALS):
        ground_truth = s.draw_unif_ground_truth(0.7, 0.9)
        markets = s.create_market_comp([100, 100], 'LMSR', 'LSLMSR', b, alpha, ground_truth)
        b1, b2 = markets[0], markets[1]
        b1_price, b2_price, b1_rev, b2_rev = s.perfect_trader_sim(N_TRADERS, 100000000, markets, silence=True)
        # print(b1.init_cost, b1.cost(b1.q), b1.q[b1.outcome], worst_case_loss)

        # normalize prices (specifically for b2)
        b1_price = np.array(b1_price)/np.sum(b1_price)
        b2_price = np.array(b2_price)/np.sum(b2_price)

        acc_LS_temp.append(1-abs(b2_price[0]-ground_truth[0]))
        acc_LMSR_temp.append(1-abs(b1_price[0]-ground_truth[0]))
        rev_LS_temp.append(b2_rev)
        rev_LMSR_temp.append(b1_rev)
        exprev_LS_temp.append(b2.get_expected_revenue())
        exprev_LMSR_temp.append(b1.get_expected_revenue())
    
    acc_LS.append(np.mean(acc_LS_temp))
    acc_LMSR.append(np.mean(acc_LMSR_temp))
    rev_LS.append(np.mean(rev_LS_temp))
    rev_stdevs_LS.append(np.std(rev_LS_temp))
    rev_LMSR.append(np.mean(rev_LMSR_temp))
    rev_stdevs_LMSR.append(np.std(rev_LMSR_temp))

    exprev_LMSR.append(np.mean(exprev_LMSR_temp))
    exprev_stdevs_LMSR.append(np.std(exprev_LMSR_temp))
    exprev_LS.append(np.mean(exprev_LS_temp))
    exprev_stdevs_LS.append(np.std(exprev_LS_temp))



plt.plot(alphas, wcls, marker='o',markersize=5, label='worst-case-losses')
plt.errorbar(alphas, exprev_LMSR, yerr=exprev_stdevs_LMSR, marker='o',markersize=5, label='LMSR')
plt.errorbar(alphas, exprev_LS, yerr=exprev_stdevs_LS, marker='o',markersize=5, label='LS_LMSR')
plt.ylabel('Expected MM revenue')
plt.title(r'Expected revenue vs. $\alpha$ (N=10 perfect-information traders)')
plt.xlabel(r'$\alpha$')
plt.legend()
plt.savefig('figs/exprevenuevsalpha.png')
plt.show()


# plt.errorbar(alphas, rev_LS, yerr=rev_stdevs_LS, marker='o',markersize=5, label='LS_LMSR')
# plt.errorbar(alphas, rev_LMSR, yerr=rev_stdevs_LMSR, marker='o',markersize=5, label='LMSR')
# plt.plot(alphas, wcls, marker='o',markersize=5, label='worst-case-losses')
# plt.xlabel(r'$\alpha$')
# plt.ylabel(r'Final MM revenue')
# plt.title(r'Revenue vs. $\alpha$ (N=10 perfect-information traders)')
# plt.legend()
# plt.savefig('figs/revenuevsalpha.png')
# plt.close()

# plt.scatter(acc_LS, rev_LS, label='LS-LMSR')
# plt.scatter(acc_LMSR, rev_LMSR, label='LMSR')

# plt.plot(alphas, acc_LS, marker='o',label='LS_LMSR')
# plt.plot(alphas, acc_LMSR, marker='o', label='LMSR')
# plt.xlabel(r'$\alpha$')
# plt.ylabel(r'Final market prediction accuracy')
# plt.title(r'Market accuracy vs. $\alpha$ (N=10 perfect-information traders)')
# plt.legend()
# plt.savefig('figs/accuracyvsalpha.png')
# plt.close()

# print(alpha)
