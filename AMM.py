import numpy as np
import random 

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
            beta = self.alpha*sum(self.q)
            return self.cost_LMSR(beta)
    
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


t1 = Trader(id=1, n=2, init_money=1000)
t2 = Trader(id=2, n=2, init_money=1000)
b = BettingMarket(2, [100,100], "LMSR", None, 1, [0.8, 0.2])

t1_LS = Trader(id=3, n=2, init_money=1000)
t2_LS = Trader(id=4, n=2, init_money=1000)
b_LS = BettingMarket(2, [100,100], "LSLMSR", 1, None, [0.8, 0.2])

###### 
print(b.cost())
b.submit_bet(t1, [5,0], verbose=True)
b_LS.submit_bet(t1_LS, [5,0], verbose=True)

b.submit_bet(t2, [5,0], verbose=True)
b_LS.submit_bet(t2_LS, [5,0], verbose=True)

print(t1.money)
print(t2.money)
print(t1_LS.money)
print(t2_LS.money)


