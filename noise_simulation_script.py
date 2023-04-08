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
markets = s.create_market_comp(init_quant, 'LMSR', 'LSLMSR', s.compute_b(
    alpha, init_quant)[0], alpha, ground_truth)
# b1_prob, b2_prob, b1_exprev, b2_exprev = s.noisyinfo_sim(10, 10000000, markets, silence=False, verbose=False)
b1_prob, b2_prob, b1_exprev, b2_exprev = s.simple_noise_sim(
    10, 10000000, markets, verbose=True)
print()
print("LMSR price probabilities:", b1_prob)
print("LS-LMSR price probabilities:", b2_prob)
print("LMSR expected revenue:", b1_exprev)
print("LS-LMSR expected revenue:", b2_exprev)

##########################################################################
##########################################################################

# 2. Run noisy information simulation: indep variable =  alpha
vigs = np.arange(0.02, 0.4, 0.01)
alphas = vigs/(2*np.log(2))
print(len(alphas))
alphas = [0.03]

init_quant = [100, 100]
N_TRIALS = 100
N_TRADERS = 10

# acc_LS = []
# acc_LMSR = []
# # rev_LS = []
# # rev_LMSR = []
# # rev_stdevs_LMSR = []
# # rev_stdevs_LS = []

# exprev_LMSR = []
# exprev_LS = []
# exprev_stdevs_LMSR = []
# exprev_stdevs_LS = []

wcls = []

acc_LS_temp = []
acc_LMSR_temp = []
rev_LS_temp = []
rev_LMSR_temp = []
exprev_LMSR_temp = []
exprev_LS_temp = []
o1, o2 = [], []

for alpha in alphas:
    # s = Simulation()

    # b, worst_case_loss = s.compute_b(alpha, init_quant)
    # print(b, worst_case_loss)
    # wcls.append(-worst_case_loss)

    for i in range(N_TRIALS):
        # SET HYPERPARAM
        # alpha = 0.03
        s = Simulation()
        b, worst_case_loss = s.compute_b(alpha, init_quant)
        # b = 150.27
        ground_truth = s.draw_unif_ground_truth(0.1, 0.2)
        ####
        markets = s.create_market_comp(
            [100, 100], 'LMSR', 'LSLMSR', b, alpha, ground_truth)
        b1, b2 = markets[0], markets[1]
        b1_prob, b2_prob, b1_exprev, b2_exprev, b1_rev, b2_rev, out1, out2 = s.noisyinfo_sim(
            10, 10000000, markets, p_signal_low=0.2, p_signal_high=1, silence=True, verbose=False)

        acc_LS_temp.append(1-abs(b2_prob[0]-ground_truth[0]))
        acc_LMSR_temp.append(1-abs(b1_prob[0]-ground_truth[0]))
        rev_LS_temp.append(b2_rev)
        rev_LMSR_temp.append(b1_rev)
        exprev_LS_temp.append(b2_exprev)
        exprev_LMSR_temp.append(b1_exprev)
        o1.append(out1)
        o2.append(out2)

    # acc_LS.append(np.mean(acc_LS_temp))
    # acc_LMSR.append(np.mean(acc_LMSR_temp))
    # # rev_LS.append(np.mean(rev_LS_temp))
    # # rev_stdevs_LS.append(np.std(rev_LS_temp))
    # # rev_LMSR.append(np.mean(rev_LMSR_temp))
    # # rev_stdevs_LMSR.append(np.std(rev_LMSR_temp))

    # exprev_LMSR.append(np.mean(exprev_LMSR_temp))
    # exprev_stdevs_LMSR.append(np.std(exprev_LMSR_temp))
    # exprev_LS.append(np.mean(exprev_LS_temp))
    # exprev_stdevs_LS.append(np.std(exprev_LS_temp))


# EXP REV vs ALPHA
# plt.plot(alphas, wcls, marker='o',markersize=5, label='worst-case-losses')
# plt.errorbar(alphas, exprev_LMSR, yerr=exprev_stdevs_LMSR, marker='o',markersize=5, label='LMSR')
# plt.errorbar(alphas, exprev_LS, yerr=exprev_stdevs_LS, marker='o',markersize=5, label='LS_LMSR')
# plt.ylabel('Expected MM revenue')
# plt.title(r'Expected revenue vs. $\alpha$ (N=20 traders in noise model)')
# plt.xlabel(r'$\alpha$')
# plt.legend()
# plt.savefig('figs/noise2_exprevenuevsalpha.png')
# plt.show()

# # ACCURACY vs ALPHA
# plt.plot(alphas, acc_LS, marker='o',label='LS_LMSR')
# plt.plot(alphas, acc_LMSR, marker='o', label='LMSR')
# plt.xlabel(r'$\alpha$')
# plt.ylabel(r'Final market prediction accuracy')
# plt.title(r'Market accuracy vs. $\alpha$ (N=10 traders in noise model)')
# plt.legend()
# # plt.savefig('figs/noise_accuracyvsalpha.png')
# # plt.close()
# plt.show()

# # EXP REV vs ACCURACY
# plt.plot(acc_LS, wcls, marker='o',markersize=5, label='worst-case-losses')
# plt.errorbar(acc_LMSR, exprev_LMSR, yerr=exprev_stdevs_LMSR, marker='o',markersize=5, label='LMSR')
# plt.errorbar(acc_LS, exprev_LS, yerr=exprev_stdevs_LS, marker='o',markersize=5, label='LS_LMSR')
# plt.ylabel('Expected MM revenue')
# plt.title(r'Expected revenue vs. price accuracy (N=20 traders in noise model)')
# plt.xlabel(r'Price accuracy')
# plt.legend()
# plt.savefig('figs/noise2_exprev_accuracy.png')
# # plt.show()


##########################################################################
##########################################################################
# # 2. Run noisy information simulation: indep variable =  number of traders
# n_traders_arr = np.arange(1, 15, 1)
# init_quant = [100, 100]
# alpha = 0.03
# N_TRIALS = 15

# acc_LS = []
# acc_stdevs_LS = []
# acc_LMSR = []
# acc_stdevs_LMSR = []

# # rev_LS = []
# # rev_stdevs_LS = []
# exprev_LS = []
# exprev_stdevs_LS = []

# for nt in n_traders_arr:
#     s = Simulation()
#     b, worst_case_loss = s.compute_b(alpha, init_quant)
#     acc_LS_temp = []
#     acc_LMSR_temp = []
#     exprev_LS_temp = []

#     for i in range(N_TRIALS):
#         #### SET HYPERPARAM
#         ground_truth = s.draw_unif_ground_truth(0.5, 0.7)
#         ####
#         markets = s.create_market_comp([100, 100], 'LMSR', 'LSLMSR', b, alpha, ground_truth)
#         b1, b2 = markets[0], markets[1]

#         b1_prob, b2_prob, b1_exprev, b2_exprev = s.simple_noise_sim(10, 10000000, markets, priv_info_noise=0.3,look_back=50,k=0.5, silence=True, verbose=False)

#         b1_prob, b2_prob, b1_exprev, b2_exprev = s.noisyinfo_sim(nt, 10000000, markets, priv_info_noise=0.3, p_signal_low=0.1, p_signal_high=0.9, silence=True, verbose=False)

#         acc_LS_temp.append(1-abs(b2_prob[0]-ground_truth[0]))
#         acc_LMSR_temp.append(1-abs(b1_prob[0]-ground_truth[0]))
#         # rev_LS_temp.append(b2_rev)
#         exprev_LS_temp.append(b2_exprev)

#     acc_LS.append(np.mean(acc_LS_temp))
#     acc_stdevs_LS.append(np.std(acc_LS_temp))
#     acc_LMSR.append(np.mean(acc_LMSR_temp))
#     acc_stdevs_LMSR.append(np.std(acc_LMSR_temp))

#     # rev_LS.append(np.mean(rev_LS_temp))
#     # rev_stdevs_LS.append(np.std(rev_LS_temp))
#     exprev_LS.append(np.mean(exprev_LS_temp))
#     exprev_stdevs_LS.append(np.std(exprev_LS_temp))

# # EXP REV vs NT
# # plt.errorbar(n_traders_arr, exprev_LS, yerr=exprev_stdevs_LS, marker='o',markersize=5, label='LS_LMSR')
# # plt.ylabel('Expected MM revenue')
# # plt.title(r'Expected revenue vs. number of traders ($\alpha$=0.03)')
# # plt.xlabel(r'number of traders')
# # plt.legend()
# # plt.savefig('figs/noise2_nt_exprev.png')
# # plt.show()

# plt.errorbar(n_traders_arr, acc_LS, yerr=acc_stdevs_LS, marker='o',markersize=5, label='LS_LMSR')
# plt.errorbar(n_traders_arr, acc_LMSR, yerr=acc_stdevs_LMSR, marker='o',markersize=5, label='LMSR')
# plt.ylabel('Final market prediction accuracy')
# plt.title(r'Market accuracy vs. number of traders ($\alpha$=0.03)')
# plt.xlabel(r'number of traders')
# plt.legend()
# # plt.savefig('figs/noise2_nt_acc.png')
# plt.show()

# REV vs ACCURACY
# plt.plot(acc_LS, wcls, marker='o',markersize=5, label='worst-case-losses')
# plt.errorbar(acc_LMSR, exprev_LMSR, yerr=exprev_stdevs_LMSR, marker='o',markersize=5, label='LMSR')
# plt.errorbar(acc_LS, exprev_LS, yerr=exprev_stdevs_LS, marker='o',markersize=5, label='LS_LMSR')
colors = ['red' if o == 0 else 'blue' for o in o1]
plt.scatter(acc_LMSR_temp, rev_LMSR_temp, c=colors)
plt.ylabel('Actual MM revenue')
plt.title(r'Revenue vs. price accuracy (N=10 traders in noise model)')
plt.xlabel(r'Price accuracy')
# plt.legend()
# plt.savefig('figs/noise_exprev_accuracy.png')
plt.show()
