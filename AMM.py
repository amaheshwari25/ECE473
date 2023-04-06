import numpy as np
import random 
from matplotlib import pyplot as plt

class BettingMarket: 

    def __init__(self, n, init_quant, msr_type, alpha, beta, true_dist):
        self.n = n
        self.q = init_quant # a list of length n
        self.msr = msr_type # a string representing type market scoring rule
        self.alpha = alpha  # the constant alpha for LS-LMSR
        self.beta = beta    # the constant beta for LMSR
        
        self.true_dist = true_dist # a "ground truth" probability distribution from which to draw the result 
        self.outcome = None 

        self.traders = []
        self.init_q = init_quant 
        self.init_cost = self.cost()
        # self.revenue = -self.init_cost
        

    def cost_LMSR(self, beta):
        return beta*np.log(np.sum(np.exp(np.array(self.q)/beta)))

    
    def cost(self):
        if self.msr == "LMSR":
            return self.cost_LMSR(self.beta)
        else: # want "LS_LMSR"
            b = self.alpha*sum(self.q)
            return self.cost_LMSR(b)
    
    def get_price(self, i):
        if self.msr == "LMSR":
            return np.exp(self.q[i]/self.beta)/np.sum(np.exp(np.array(self.q)/self.beta))
        else:
            b = self.alpha*sum(self.q)
            sum_term = np.sum(np.exp(self.q/b))
            term1 = self.alpha * np.log(sum_term)
            term2_num = (np.sum(self.q)*np.exp(self.q[i]/b) - np.sum([x*np.exp(x/b) for x in self.q]))
            term2_denom = np.sum(self.q)*sum_term
            return term1 + term2_num/term2_denom
                           

    
    def submit_bet(self, trader, delta, verbose=False):
        new_q = [sum(x) for x in zip(self.q, delta)]
        curr_cost = self.cost()
        self.q = new_q
        new_cost = self.cost()
        trader.money -= (new_cost-curr_cost)
        trader.payouts = [sum(x) for x in zip(trader.payouts, delta)]

        if verbose:
            print("Trader", trader.id, "updates to", self.q, "for price of", (new_cost-curr_cost))
    
    def get_market_state(self):
        if self.outcome is None: # draw the outcome the first time this is called
            self.outcome = random.choices(list(range(self.n)), weights=self.true_dist)
        
        revenue = self.cost()-self.init_cost-self.q[self.outcome]
        print("State:", self.q)
        print("Outcome realized:", self.outcome)
        print("Revenue:", revenue)

    
    # TBD: IMPLEMENT "MOVE FORWARD IN OBLIGATION SPACE" requirement
            

class Trader:
    def __init__(self, id, n, init_money):
        self.n = n
        self.id = id
        self.money = init_money
        self.payouts = [0]*n

############
# 1. Test against UNC paper initial market cost 
# test_market = BettingMarket(2, [1000, 1000], "LSLMSR", 1, 1, [0.8, 0.2])
# print(test_market.cost())


# ############
# 2. Try out LMSR scoring rule
# t1 = Trader(id=1, n=2, init_money=1000)
# t2 = Trader(id=2, n=2, init_money=1000)
# b = BettingMarket(2, [100,100], "LMSR", None, 1, [0.8, 0.2])
# print(b.cost())
# b.submit_bet(t2, [5,0], verbose=True)
# b.submit_bet(t1, [5,0], verbose=True)
# print(t1.money)
# print(t2.money)


############
# 3. Try out LS-LMSR scoring rule
# t1_LS = Trader(id=3, n=2, init_money=1000)
# t2_LS = Trader(id=4, n=2, init_money=1000)
# b_LS = BettingMarket(2, [100,100], "LSLMSR", 0.05, None, [0.8, 0.2])
# b_LS.submit_bet(t1_LS, [5,0], verbose=True)
# b_LS.submit_bet(t1_LS, [0,5], verbose=True)
# b_LS.submit_bet(t2_LS, [5,0], verbose=True)
# print(t1_LS.money)
# print(t2_LS.money)

############
# 4. Try to replicate numerical analysis of CMU paper in terms of liquidity

# CMU FIGURE 1
bm_y250 = BettingMarket(2, [0, 250], "LSLMSR", alpha=0.05, beta=None, true_dist=[0.8, 0.2])
bm_y500 = BettingMarket(2, [0, 500], "LSLMSR", alpha=0.05, beta=None, true_dist=[0.8, 0.2])
bm_y750 = BettingMarket(2, [0, 750], "LSLMSR", alpha=0.05, beta=None, true_dist=[0.8, 0.2])
bm = [bm_y250, bm_y500, bm_y750]

x_vals = np.arange(0, 1000, 5)
traders = [Trader(x, 2, 10000000000) for x in range(3)]
prices = [[], [], []]

for i in range(3):
    for x in x_vals:
        bm[i].submit_bet(traders[i], [x-bm[i].q[0], 0])
        prices[i].append(bm[i].get_price(0))

plt.plot(x_vals, prices[0], label='q_y = 250')
plt.plot(x_vals, prices[1], label='q_y = 500')
plt.plot(x_vals, prices[2], label='q_y= 750')

plt.xlabel(r'$q_x$')
plt.ylabel(r'$p_x(q)$')
plt.title(r'Price variation as a function of complement quantity, $\alpha=0.05$')
plt.savefig('cmu_fig1.png')
plt.close()


