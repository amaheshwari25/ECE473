from AMM import BettingMarket
from BaseTrader import Trader
from simulation import Simulation
import numpy as np
from matplotlib import pyplot as plt
import random


# 1. Run a simple noisy information simulation
# s = Simulation()
# ground_truth = s.draw_unif_ground_truth(0.6, 0.8)
# init_quant = [100, 100]
# alpha = 0.03
# markets = s.create_market_comp(init_quant, 'LMSR', 'LSLMSR', s.compute_b(alpha, init_quant)[0], alpha, ground_truth)
# # b1_prob, b2_prob, b1_exprev, b2_exprev = s.noisyinfo_sim(10, 10000000, markets, silence=False, verbose=False)
# b1_prob, b2_prob, b1_exprev, b2_exprev = s.simple_noise_sim(10, 10000000, markets, verbose=True)
# print()
# print("LMSR price probabilities:", b1_prob)
# print("LS-LMSR price probabilities:", b2_prob)
# print("LMSR expected revenue:", b1_exprev)
# print("LS-LMSR expected revenue:", b2_exprev)

##########################################################################
##########################################################################

# # # 2. Run noisy information simulation: indep variable =  alpha 
# vigs = np.arange(0.02, 0.4, 0.02)
# alphas = vigs/(2*np.log(2))

# N_TRADERS = 20
# init_quant = [100, 100]
# N_TRIALS = 40
# LOOK_BACK = int(N_TRADERS/4)
# K = 0.3
# K_MIN = 0.2
# K_MAX = 0.6
# PRIV_NOISE = 0.2

# acc_LS = []
# acc_quartiles_LS = []
# acc_LMSR = []
# acc_quartiles_LMSR = []
# # rev_LS = []
# # rev_LMSR = []
# # rev_stdevs_LMSR = []
# # rev_stdevs_LS = []

# exprev_LMSR = []
# exprev_quartiles_LMSR = []
# exprev_LS = []
# exprev_quartiles_LS = []


# # exprev_stdevs_LMSR = []
# # exprev_stdevs_LS = []

# wcls= []

# for alpha in alphas:
#     s = Simulation()
#     acc_LS_temp = []
#     acc_LMSR_temp = []
#     exprev_LMSR_temp = []
#     exprev_LS_temp = []

#     b, worst_case_loss = s.compute_b(alpha, init_quant)
#     # print(b, worst_case_loss)
#     wcls.append(-worst_case_loss)

#     for i in range(N_TRIALS):
#         #### SET HYPERPARAM
#         ground_truth = s.draw_unif_ground_truth(0.6, 0.8)
#         #### 
#         markets = s.create_market_comp([100, 100], 'LMSR', 'LSLMSR', b, alpha, ground_truth)
#         b1, b2 = markets[0], markets[1]
#         b1_prob, b2_prob, b1_exprev, b2_exprev = s.simple_noise_sim(N_TRADERS, 10000000, markets, priv_info_noise=PRIV_NOISE,look_back=LOOK_BACK, k_min=K_MIN, k_max=K_MAX, silence=True, verbose=False)
#         # b1_prob, b2_prob, b1_exprev, b2_exprev = s.noisyinfo_sim(N_TRADERS, 10000000, markets, p_signal_low=0.2, p_signal_high=0.8, silence=True, verbose=False)

#         acc_LS_temp.append(1-abs(b2_prob[0]-ground_truth[0]))
#         acc_LMSR_temp.append(1-abs(b1_prob[0]-ground_truth[0]))
#         exprev_LS_temp.append(b2_exprev)
#         exprev_LMSR_temp.append(b1_exprev)
    
#     acc_LMSR.append(np.median(acc_LMSR_temp))
#     acc_LS.append(np.median(acc_LS_temp))
#     exprev_LMSR.append(np.median(exprev_LMSR_temp))
#     exprev_LS.append(np.median(exprev_LS_temp))

#     acc_quartiles_LMSR.append([np.median(acc_LMSR_temp)-np.quantile(acc_LMSR_temp, 0.25), np.quantile(acc_LMSR_temp, 0.75)-np.median(acc_LMSR_temp)])
#     acc_quartiles_LS.append([np.median(acc_LS_temp)-np.quantile(acc_LS_temp, 0.25), np.quantile(acc_LS_temp, 0.75)-np.median(acc_LS_temp)])
#     exprev_quartiles_LMSR.append([np.median(exprev_LMSR_temp)-np.quantile(exprev_LMSR_temp, 0.25), np.quantile(exprev_LMSR_temp, 0.75)-np.median(exprev_LMSR_temp)])
#     exprev_quartiles_LS.append([np.median(exprev_LS_temp)-np.quantile(exprev_LS_temp, 0.25), np.quantile(exprev_LS_temp, 0.75)-np.median(exprev_LS_temp)])



#     # acc_LS.append(np.mean(acc_LS_temp))
#     # acc_LMSR.append(np.mean(acc_LMSR_temp))
#     # exprev_LMSR.append(np.mean(exprev_LMSR_temp))
#     # exprev_stdevs_LMSR.append(np.std(exprev_LMSR_temp))
#     # exprev_LS.append(np.mean(exprev_LS_temp))
#     # exprev_stdevs_LS.append(np.std(exprev_LS_temp))

# exprev_quartiles_LMSR = [[exprev_quartiles_LMSR[i][0] for i in range(len(alphas))], [exprev_quartiles_LMSR[i][1] for i in range(len(alphas))]] 
# exprev_quartiles_LS = [[exprev_quartiles_LS[i][0] for i in range(len(alphas))], [exprev_quartiles_LS[i][1] for i in range(len(alphas))]] 
# acc_quartiles_LMSR = [[acc_quartiles_LMSR[i][0] for i in range(len(alphas))], [acc_quartiles_LMSR[i][1] for i in range(len(alphas))]] 
# acc_quartiles_LS = [[acc_quartiles_LS[i][0] for i in range(len(alphas))], [acc_quartiles_LS[i][1] for i in range(len(alphas))]] 


# # EXP REV vs ALPHA 
# # plt.errorbar(alphas, exprev_LMSR, yerr=exprev_stdevs_LMSR, marker='o',markersize=5, label='LMSR')
# # plt.errorbar(alphas, exprev_LS, yerr=exprev_stdevs_LS, marker='o',markersize=5, label='LS_LMSR')

# # # note: this plots MEDIANS and 1st / 3rd quartile
# plt.errorbar(alphas, exprev_LMSR, yerr=exprev_quartiles_LMSR, marker='o',markersize=5, capsize=3, label='LMSR')
# plt.errorbar(alphas, exprev_LS, yerr=exprev_quartiles_LS, marker='o',markersize=5, capsize=3, label='LS_LMSR')
# plt.plot(alphas, wcls, marker='o',markersize=5, label='worst-case-losses')
# plt.ylabel('Expected MM revenue')
# plt.title(r'Expected revenue vs. $\alpha$ (N=20 traders, $k: 0.6 \rightarrow 0.2$)')
# plt.xlabel(r'$\alpha$')
# plt.legend()
# plt.savefig('figs/simple_noise_exprev_alpha.png')
# plt.show()

# # # ACCURACY vs ALPHA 
# # plt.plot(alphas, acc_LS, marker='o',label='LS_LMSR')
# # plt.plot(alphas, acc_LMSR, marker='o', label='LMSR')

# # note: this plots MEDIANS and 1st / 3rd quartile
# plt.errorbar(alphas, acc_LMSR, yerr=acc_quartiles_LMSR, marker='o',markersize=5, capsize=3, label='LMSR')
# plt.errorbar(alphas, acc_LS, yerr=acc_quartiles_LS, marker='o',markersize=5, capsize=3, label='LS_LMSR')
# plt.xlabel(r'$\alpha$')
# plt.ylabel(r'Final market prediction accuracy')
# plt.title(r'Market accuracy vs. $\alpha$ (N=20 traders, $k: 0.6 \rightarrow 0.2$)')
# plt.legend()
# plt.savefig('figs/simple_noise_acc_alpha.png')
# plt.close()
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
# 2. Run noisy information simulation: indep variable =  number of traders 
N_TRAD_MAX = 30
n_traders_arr = np.arange(1, N_TRAD_MAX)
init_quant = [100, 100]
alpha = 0.03
N_TRIALS = 40
LOOK_BACK = int(N_TRAD_MAX/4)
K = 0.3
K_MIN = 0.2
K_MAX = 0.6
PRIV_NOISE = 0.2

acc_LS = []
acc_LS_med = []
acc_quartiles_LS = []
acc_stdevs_LS = []

acc_LMSR = []
acc_LMSR_med = []
acc_quartiles_LMSR = []
acc_stdevs_LMSR = []

exprev_LS = []
exprev_LS_med = []
exprev_stdevs_LS = []

for nt in n_traders_arr:
    s = Simulation()
    b, worst_case_loss = s.compute_b(alpha, init_quant)
    acc_LS_temp = []
    acc_LMSR_temp = []
    exprev_LS_temp = []

    for i in range(N_TRIALS):
        #### SET HYPERPARAM
        ground_truth = s.draw_unif_ground_truth(0.6, 0.8)
        #### 
        markets = s.create_market_comp([100, 100], 'LMSR', 'LSLMSR', b, alpha, ground_truth)
        b1, b2 = markets[0], markets[1]
        b1_prob, b2_prob, b1_exprev, b2_exprev = s.simple_noise_sim(nt, 10000000, markets, priv_info_noise=PRIV_NOISE,look_back=LOOK_BACK, k_min=K_MIN, k_max=K_MAX, silence=True, verbose=False)
        # b1_prob, b2_prob, b1_exprev, b2_exprev = s.simple_noise_sim(nt, 10000000, markets, priv_info_noise=0.2,look_back=LOOK_BACK,k=K, silence=True, verbose=False)
        # b1_prob, b2_prob, b1_exprev, b2_exprev = s.noisyinfo_sim(nt, 10000000, markets, priv_info_noise=0.3, p_signal_low=0.1, p_signal_high=0.9, silence=True, verbose=False)

        acc_LS_temp.append(1-abs(b2_prob[0]-ground_truth[0]))
        acc_LMSR_temp.append(1-abs(b1_prob[0]-ground_truth[0]))
        exprev_LS_temp.append(b2_exprev)

    acc_LS.append(np.mean(acc_LS_temp))
    acc_LS_med.append(np.median(acc_LS_temp))
    acc_stdevs_LS.append(np.std(acc_LS_temp))
    acc_quartiles_LS.append([np.median(acc_LS_temp)-np.quantile(acc_LS_temp, 0.25), np.quantile(acc_LS_temp, 0.75)-np.median(acc_LS_temp)])

    acc_LMSR.append(np.mean(acc_LMSR_temp))
    acc_LMSR_med.append(np.median(acc_LMSR_temp))
    acc_stdevs_LMSR.append(np.std(acc_LMSR_temp))
    acc_quartiles_LMSR.append([np.median(acc_LMSR_temp)-np.quantile(acc_LMSR_temp, 0.25), np.quantile(acc_LMSR_temp, 0.75)-np.median(acc_LMSR_temp)])

    exprev_LS.append(np.mean(exprev_LS_temp))
    exprev_LS_med.append(np.median(exprev_LS_temp))
    exprev_stdevs_LS.append(np.std(exprev_LS_temp))

# EXP REV vs NT 
plt.errorbar(n_traders_arr, exprev_LS, yerr=exprev_stdevs_LS, marker='o',markersize=5, label='LS_LMSR')
plt.ylabel('Expected MM revenue')
plt.title(r'Exp. revenue vs num. traders ($\alpha=0.03,k: 0.6 \rightarrow 0.2$)')
plt.xlabel(r'Number of traders')
plt.legend()
plt.savefig('figs/simple_noise_nt_exprev.png')
plt.show()

# ACC vs NT
acc_quartiles_LMSR = [[acc_quartiles_LMSR[i][0] for i in range(len(n_traders_arr))], [acc_quartiles_LMSR[i][1] for i in range(len(n_traders_arr))]] 
acc_quartiles_LS = [[acc_quartiles_LS[i][0] for i in range(len(n_traders_arr))], [acc_quartiles_LS[i][1] for i in range(len(n_traders_arr))]] 

# plt.errorbar(n_traders_arr, acc_LS, yerr=acc_stdevs_LS, marker='o',markersize=5, label='LS_LMSR')
# plt.errorbar(n_traders_arr, acc_LMSR, yerr=acc_stdevs_LMSR, marker='o',markersize=5, label='LMSR')

# note: this plots MEDIANS and QUANTILES
plt.errorbar(n_traders_arr, acc_LMSR_med, yerr=acc_quartiles_LMSR, marker='o', markersize=5, capsize=3, label='LMSR')
plt.errorbar(n_traders_arr, acc_LS_med, yerr=acc_quartiles_LS, marker='o', markersize=5, capsize=3, label='LS-LMSR')
plt.ylabel('Final market prediction accuracy (median)')
plt.title(r'Market accuracy vs. num. traders ($\alpha=0.03,k: 0.6 \rightarrow 0.2$)')
plt.xlabel(r'Number of traders')
plt.legend()
plt.savefig('figs/simple_noise_nt_acc.png')
plt.show()

##########################################################################
##########################################################################
