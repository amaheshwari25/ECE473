from AMM import BettingMarket
from BaseTrader import Trader
import numpy as np
from matplotlib import pyplot as plt
import random

class Simulation:

    def __init__(self):
        self.betters = []
        self.traders_LMSR = []
        self.traders_LSLMSR = []
    
    # def add_better(self, trader: Trader):
    #     self.betters.append(trader)

    def getLMSRtraders(self):
        return self.traders_LMSR

    def getLSLMSRtraders(self):
        return self.traders_LSLMSR

    def draw_unif_ground_truth(self, low, high):
        p0 = low+(high-low)*random.random()
        return [p0, 1-p0]

    def create_market_comp(self, init_quant, msr1, msr2, msr1_const, msr2_const, ground_truth):
        b1 = BettingMarket(2, init_quant, msr1, (None if msr1 == "LMSR" else msr1_const), (None if msr1 == "LS-LMSR" else msr1_const), ground_truth)
        b2 = BettingMarket(2, init_quant, msr2, (None if msr2 == "LMSR" else msr2_const), (None if msr2 == "LS-LMSR" else msr2_const), ground_truth)
        return [b1, b2]

    def compute_b(self, alpha, init_quant):
        lslmsr =  BettingMarket(2, init_quant, "LSLMSR", alpha, None, [-1, -1])
        worst_case_loss = lslmsr.init_cost # worst-case LS-LMSR loss is just C(q0)
        # worst-case LMSR loss is -b ln (exp(q0_i /b) / sum(exp(q0_j / b))), where q0_i is the max value in init_quant
        #   (this formula reduces to b ln(n) for uniform initial distribution; TBD: check that correct for general case)
        uniform_flag = True
        for x in init_quant:
            if not x == init_quant[0]:
                uniform_flag = False
                break
        assert(uniform_flag)
        b = worst_case_loss / np.log(2)
        return b, worst_case_loss
    
    def perfect_trader_sim(self, ntraders, trader_money, markets, silence=False, verbose=False):
        b1, b2 = markets[0], markets[1]
        assert(b1.true_dist == b2.true_dist)
       
        if not silence:
            print()
            print()
            print('GROUND TRUTH:', b1.true_dist)
            print('INITIAL PRICE: LMSR', [b1.get_price_vector(b1.q)])
            print('INITIAL PRICE: LS-LMSR', [b2.get_price_vector(b2.q)])
            print()

        traders_b1 = []
        bets_b1 = []
        costs_b1 = []
        traders_b2 = []
        bets_b2 = []
        costs_b2 = []

        for i in range(ntraders):
            traderv1 = Trader(i, 2, trader_money)
            traderv1.set_belief(b1.true_dist)
            traders_b1.append(traderv1)
            traderv2 = Trader(i, 2, trader_money)
            traderv2.set_belief(b1.true_dist)
            traders_b2.append(traderv2)
            
            if not silence:
                print("LMSR market trader", i, ":")
            bet1, cost1 = traderv1.play(b1, verbose=verbose)
            bets_b1.append(bet1)
            costs_b1.append(cost1)
            if not silence:
                print("Final: bet:", bet1, "cost:", cost1)
                print('------')

                print("LS-LMSR market trader", i, ":")
            bet2, cost2 = traderv2.play(b2, verbose=verbose)
            bets_b2.append(bet2)
            costs_b2.append(cost2)
            if not silence:
                print("Final: bet:", bet2, "cost:", cost2)
                print()
        if not silence:
            print('==========')
            print('LMSR market: ')
        b1.get_market_state(silence=silence)
        if not silence:
            print()
            print('LS-LMSR market')
        b2.get_market_state(silence=silence)

        return (b1.get_price_vector(b1.q), b2.get_price_vector(b2.q), b1.get_revenue(b1.outcome), b2.get_revenue(b2.outcome)) # change this to same outcome?
    
    def noisyinfo_sim(self, ntraders, trader_money, markets, priv_info_noise=0.2, p_signal_low=0.5, p_signal_high=0.5, silence=False, verbose=False):
        '''
        Parameters:
         - priv_info_noise: private info will be uniform in [ground_truth-priv_info_noise, ground_truth+priv_info_noise]
             (Note: for intended simulation, this should be pretty noisy!)
         - p_signal: probability with which any given trader will consider the current market value too 
        '''
        ## TBD: MODELING CHANGES ## 
        #  - add shifting ground truth for market? #
        #  - [DONE] make p_signal vary in time? # 

        b1, b2 = markets[0], markets[1]
        assert(b1.true_dist == b2.true_dist)
        if not silence:
            print()
            print()
            print('GROUND TRUTH:', b1.true_dist)
            print('priv_info_noise:', priv_info_noise, '; p_signal_low:', p_signal_low, '; p_signal_high:', p_signal_high)
            print('INITIAL PRICE: LMSR', [b1.get_price_vector(b1.q)])
            print('INITIAL PRICE: LS-LMSR', [b2.get_price_vector(b2.q)])
            print()
        
        traders_b1 = []
        bets_b1 = []
        costs_b1 = []
        traders_b2 = []
        bets_b2 = []
        costs_b2 = []

        for i in range(ntraders):
            traderv1 = Trader(i, 2, trader_money)
            traders_b1.append(traderv1)
            traderv2 = Trader(i, 2, trader_money)
            traders_b2.append(traderv2)
            # MAIN: Set this trader's belief
            # 1. some private info distributed noisily around ground truth (want this to be pretty noisy?)
            priv_info = min(random.random()*(2*priv_info_noise)+max(b1.true_dist[0]-priv_info_noise, 0.001), 0.999)
            trad_b1_p0 = priv_info
            trad_b2_p0 = priv_info
            # 2. with p_signal probability, update to be between this and current market value price-probability 
            p_signal = ((i+1)/ntraders)*(p_signal_high - p_signal_low) + p_signal_low # idea: increases from p_signal_low to p_signal_high over time
            # ^^ possible issue: high p_signal by the end regardless of ntraders, if compute as fraction of ntraders
            if(random.random() >= p_signal):
                trad_b1_p0 += min(0.999, max(0.001, random.random()*(b1.get_price_prob(b1.q)[0]-priv_info)))
                trad_b2_p0 += min(0.999, max(0.001, random.random()*(b2.get_price_prob(b2.q)[0]-priv_info)))
                ## NEW MODEL: sample between current market belief and true market belief
                # trad_b1_p0 = min(0.999, max(0.001, random.random()*(b1.get_price_prob(b1.q)[0]-b1.true_dist[0])+b1.true_dist[0]))
                # trad_b2_p0 = min(0.999, max(0.001, random.random()*(b2.get_price_prob(b2.q)[0]-b2.true_dist[0])+b2.true_dist[0]))
            traderv1.set_belief([trad_b1_p0, 1-trad_b1_p0])
            traderv2.set_belief([trad_b2_p0, 1-trad_b2_p0])

            if not silence:
                print("LMSR market trader", i, ":")
            bet1, cost1 = traderv1.play(b1, verbose=verbose)
            bets_b1.append(bet1)
            costs_b1.append(cost1)
            if not silence:
                print("Final: bet:", bet1, "cost:", cost1)
                print('------')

                print("LS-LMSR market trader", i, ":")
            bet2, cost2 = traderv2.play(b2, verbose=verbose)
            bets_b2.append(bet2)
            costs_b2.append(cost2)
            if not silence:
                print("Final: bet:", bet2, "cost:", cost2)
                print()

        if not silence:
            print('==========')
            print('LMSR market: ')
        b1.get_market_state(silence=silence)
        if not silence:
            print()
            print('LS-LMSR market')
        b2.get_market_state(silence=silence)

        return (b1.get_price_prob(b1.q), b2.get_price_prob(b2.q), b1.get_expected_revenue(), b2.get_expected_revenue())

    def simple_noise_sim(self, ntraders, trader_money, markets, priv_info_noise=0.2, look_back = 50, k=0.5, k_min=None, k_max=None, silence=False, verbose=False):
        '''
        Idea: at each time instant (for each trader), 
          (1) draw some (noisy) private info
          (2) use average of last look_back market prices 
          (3) trader belief is a weighted average (weighted by k) of market average and private info 
        Parameters:
         - priv_info_noise: private info will be uniform in [ground_truth-priv_info_noise, ground_truth+priv_info_noise]
             (Note: for intended simulation, this should be pretty noisy!)
         - look_back: number of previous market price beliefs to consider 
         - k: weight for weighted average belief (OR: k_min --> k_max)
        '''
        b1, b2 = markets[0], markets[1]
        assert(b1.true_dist == b2.true_dist)
       
        if not silence:
            print()
            print()
            print('GROUND TRUTH:', b1.true_dist)
            print('priv_info_noise:', priv_info_noise, '; look_back:', look_back, '; k:', k)
            print('INITIAL PRICE: LMSR', [b1.get_price_vector(b1.q)])
            print('INITIAL PRICE: LS-LMSR', [b2.get_price_vector(b2.q)])
            print()
        
        traders_b1 = []
        bets_b1 = []
        costs_b1 = []
        traders_b2 = []
        bets_b2 = []
        costs_b2 = []
        prev_b1market_p0 = []
        prev_b2market_p0 = []

        for i in range(ntraders):
            traderv1 = Trader(i, 2, trader_money)
            traders_b1.append(traderv1)
            traderv2 = Trader(i, 2, trader_money)
            traders_b2.append(traderv2)

            prev_b1market_p0.append(b1.get_price_prob(b1.q)[0])
            prev_b2market_p0.append(b2.get_price_prob(b2.q)[0])

            # MAIN: Set this trader i's belief: lambda*(priv_info) + (1-lambda)*(market_avg_till_now, up to look_back)
            # 1. some private info distributed noisily around ground truth (want this to be pretty noisy?)
            #  [TBD: determine what distribution should private info be drawn from]
            priv_info = min(random.random()*(2*priv_info_noise)+max(b1.true_dist[0]-priv_info_noise, 0.001), 0.999)
            trad_b1_p0, trad_b2_p0 = priv_info, priv_info
            # 2. compute average of look_back previous market values
            b1avg, b2avg  = np.mean(prev_b1market_p0[-1*min(look_back, i+1):]), np.mean(prev_b2market_p0[-1*min(look_back, i+1):])
            # 3. weight previous market prob values with private info based on k: k*(MY INFO)+(1-k)*(MARKET AVG)
            #      with possibility for using a k linearly varying from **k_max to k_min** (NOTE DIRECTION!) across ntraders
            #       e.g. 1st trader uses k=k_max=0.8 (rely on private info), final trader uses k=k_min=0.2 (rely on market avg)
            k = ((k_max+(k_min-k_max)*(i+1)/ntraders) if k_min is not None else k)
            # note: variable k does NOT seem to work great for increasing accuracy trend -- does lead to BETTER MM revenue? somehow?
            trad_b1_p0 = k*trad_b1_p0 + (1-k)*b1avg
            trad_b2_p0 = k*trad_b2_p0 + (1-k)*b2avg 

            traderv1.set_belief([trad_b1_p0, 1-trad_b1_p0])
            traderv2.set_belief([trad_b2_p0, 1-trad_b2_p0])
            if not silence:
                print("LMSR market trader", i, ":")
            bet1, cost1 = traderv1.play(b1, verbose=verbose)
            bets_b1.append(bet1)
            costs_b1.append(cost1)
            if not silence:
                print("Final: bet:", bet1, "cost:", cost1)
                print('------')

                print("LS-LMSR market trader", i, ":")
            bet2, cost2 = traderv2.play(b2, verbose=verbose)
            bets_b2.append(bet2)
            costs_b2.append(cost2)
            if not silence:
                print("Final: bet:", bet2, "cost:", cost2)
                print()
        if not silence:
            print('==========')
            print('LMSR market: ')
        b1.get_market_state(silence=silence)
        if not silence:
            print()
            print('LS-LMSR market')
        b2.get_market_state(silence=silence)

        return (b1.get_price_prob(b1.q), b2.get_price_prob(b2.q), b1.get_expected_revenue(), b2.get_expected_revenue())
