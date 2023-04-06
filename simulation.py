from AMM import BettingMarket
from BaseTrader import Trader
import numpy as np
from matplotlib import pyplot as plt
import random

class Simulation:

    def __init__(self):
        self.market = BettingMarket(2, [1000, 1000])
        self.betters = []
    
    def add_better(self, trader: Trader):
        self.betters.append(trader)