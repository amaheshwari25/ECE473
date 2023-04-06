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

    def play(self, mkt: BettingMarket, verbose=False, DELTA_FRAC=0.002):
        '''
         Makes bet for this Trader's turn by buying each asset while its price is less than probability distribution belief.
         Check that 
         DELTA_FRAC: fraction of market to buy in each evaluation (in each delta/step) of price vs belief -- sets discretizing error
        '''

