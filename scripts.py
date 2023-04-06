import numpy as np
import random 
from matplotlib import pyplot as plt
from BaseTrader import Trader
from AMM import BettingMarket

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

#############
# 4. Testing how price varies while slowly increasing quantity 
t = Trader(id=1, n=2, init_money=100000)
b = BettingMarket(2, [100,100], "LSLMSR", 0.05, None, [0.8, 0.2])
t.set_belief([0.7, 0.3])
FRAC = 0.002
init_cost = b.cost()
while(b.get_price(0, b.q) < t.belief[0]):
    t.bet(b, 0, frac*b.q[0], True)
final_cost = b.cost()
print(final_cost-init_cost, t.belief[0]*t.payouts[0]) # (4.643657905161106 5.220465226863531)
print(b.get_price(0, b.q), t.belief[0]) # (0.7040043888083869 0.7)