import numpy as np
import random 
from matplotlib import pyplot as plt
from AMM import BettingMarket

class Trader:
    def __init__(self, id, n, init_money):
        self.n = n
        self.id = id
        self.money = init_money
        self.payouts = [0]*n
    
    def set_belief(self, prob_vector):
        self.belief = prob_vector
    
    def bet(self, mkt: BettingMarket, i, amt, verbose=False):
        delta = [(1 if i==j else 0)*amt for j in range(self.n)]
        return mkt.submit_bet(self, delta, verbose)

    def play(self, mkt: BettingMarket, DELTA_FRAC=0.002, MAX_ITER=2/0.002, verbose=False):
        '''
         Makes bet for this Trader's turn by buying each asset while its price is less than probability distribution belief
           if Trader can afford the bet
         DELTA_FRAC: fraction of market to buy in each evaluation (in each delta/step) of price vs belief -- sets discretizing error
         MAX_ITER: sets maximum number of times for evaluating the price/probability and betting DELTA_FRAC of market
        '''
        # Q: could this infinite loop? do we really need MAX_ITER or not? 
        flag=True
        init_cost = mkt.cost()
        init_payouts = self.payouts

        while(flag and MAX_ITER >= 0):
            flag = False
            # this is hard-coded for a 2-item market
            if(mkt.get_price(0, mkt.q) < self.belief[0]):
                flag=True
                bet_cost = self.bet(mkt, 0, DELTA_FRAC*mkt.q[0])
                if bet_cost is None: 
                    flag=False
            if(mkt.get_price(1, mkt.q) < self.belief[1]):
                flag=True
                bet_cost = self.bet(mkt, 1, DELTA_FRAC*mkt.q[1])
                if bet_cost is None: 
                    flag=False
            MAX_ITER-=1
        
        final_cost = mkt.cost()
        if(verbose):
            print("Cost of transaction", final_cost-init_cost)
            print("Expected return from transaction", sum(self.belief[i]*self.payouts[i] for i in range(self.n)))
            print("Current price vs beliefs", [mkt.get_price(0, mkt.q), mkt.get_price(1, mkt.q)], self.belief)

        bet = [x[0]-x[1] for x in zip(self.payouts, init_payouts)]
        return bet, final_cost-init_cost

