import numpy as np
import random 
from matplotlib import pyplot as plt
# from BaseTrader import Trader

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
        self.init_cost = self.cost(self.q)
        # self.revenue = -self.init_cost
        

    def cost_LMSR(self, beta, q):
        return beta*np.log(np.sum(np.exp(np.array(q)/beta)))

    # TBD: DEAL WITH OVERFLOW IN EXP

    def cost(self, q):
        if self.msr == "LMSR":
            return self.cost_LMSR(self.beta, q)
        else: # want "LS_LMSR"
            b = self.alpha*np.sum(q)
            return self.cost_LMSR(b, q)
    
    def get_price(self, i, q):
        if self.msr == "LMSR":
            return np.exp(q[i]/self.beta)/np.sum(np.exp(np.array(q)/self.beta))
        else: # "LS-LMSR"
            b = self.alpha*sum(q)
            sum_term = np.sum(np.exp(np.array(q)/b))
            term1 = self.alpha * np.log(sum_term)
            term2_num = (np.sum(q)*np.exp(q[i]/b) - np.sum([x*np.exp(x/b) for x in q]))
            term2_denom = np.sum(q)*sum_term
            return term1 + term2_num/term2_denom

    def submit_bet(self, trader, delta, verbose=False):
        new_q = [sum(x) for x in zip(self.q, delta)]
        curr_cost = self.cost(self.q)
        new_cost = self.cost(new_q)
        if(new_cost-curr_cost > trader.money):
            if verbose:
                print("Insufficient trader funds: trader money={m}, transaction cost={c}".format(m=trader.money, c=new_cost-curr_cost))
            return None
        self.q = new_q
        trader.money -= (new_cost-curr_cost)
        trader.payouts = [sum(x) for x in zip(trader.payouts, delta)]

        if verbose:
            print("Trader", trader.id, "updates to", self.q, "for cost of", (new_cost-curr_cost))
        return new_cost - curr_cost
    
    def get_market_state(self):
        if self.outcome is None: # draw the outcome the first time this is called
            self.outcome = random.choices(list(range(self.n)), weights=self.true_dist)[0]
        
        revenue = self.cost(self.q)-self.init_cost-self.q[self.outcome]
        print("State:", self.q)
        print("Final instantaneous prices:", [self.get_price(0, self.q), self.get_price(1, self.q)])
        print("Outcome realized:", self.outcome)
        print("Revenue:", revenue)

    
    # TBD: IMPLEMENT "MOVE FORWARD IN OBLIGATION SPACE" requirement
    







