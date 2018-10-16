#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 08:49:41 2018

@author: tianxiang
"""
import math
import numpy as np

class StockOption(object):
    def __init__(self, params):
        
        self.S0 = params.get("S0",0)
        self.K = params.get("K",0)
        self.r = params.get("r",0)
        self.T = params.get("T",0)
        self.N = params.get("N", 0)
        self.N = max(1, self.N) # Ensure N have at least 1 time step
        self.u = params.get("u", 0)  # ratio of up state
        self.d = params.get("d", 0)  # ratio of down state
        self.div = params.get("div", 0)  # Divident yield
        self.sigma = params.get("sigma", 0)  # Volatility
        self.is_call = params.get("is_call", True)  # Call or put
        self.is_european = params.get("is_eu", True)  # Eu or Am
        self.STs = None  # Declare the stock prices tree
        
        """ Computed values """
        self.dt = self.T/float(self.N)  # Single time step, in years
        self.df = math.exp(-(self.r) * self.dt)  # Discount factor
        
# _ make method private in class
# __ avoid method to be overided
# __xx__ magic method 
        
class BinomialEuropeanOption(StockOption):

    def _setup_para_(self):
        self.M = self.N + 1
        self.qu = (math.exp((self.r-self.div)*self.dt) -
                   self.d) / (self.u-self.d)
        self.qd = 1-self.qu
        
    def _initialize_stock_price_tree_(self):
        self.STs = np.zeros(self.M)
        
        for i in range(self.M):
            self.STs[i] = self.S0 * (self.u**(self.N-i))*(self.d ** i)
#        print self.STs 
    
    def _initialize_payoff_tree_(self):
        if self.is_call == True:
            payoffs = np.maximum(self.STs - self.K, 0)
        else:
            payoffs = np.maximum(self.K- self.STs, 0)
        return payoffs
    
    def _traverse_tree_(self):
        payoffs = self._initialize_payoff_tree_()
        for i in range(self.N):
#            print i, payoffs
            payoffs = (payoffs[:-1]*self.qu + payoffs[1:] * self.qd) * self.df
        return payoffs
    
    def price(self):
        self._setup_para_()
        self._initialize_stock_price_tree_()
#        payoffs = self._initialize_payoff_tree_()
        payoffs = self._traverse_tree_()
        return payoffs
    
class BinomialTreeOption(StockOption):

    def _setup_parameters_(self):

        self.qu = (math.exp((self.r-self.div)*self.dt) -
                   self.d)/(self.u-self.d)
        self.qd = 1-self.qu

    def _initialize_stock_price_tree_(self):
        # Initialize a 2D tree at T=0
        self.STs = [np.array([self.S0])]

        # Simulate the possible stock prices path
        for i in range(self.N):
            prev_branches = self.STs[-1]
            st = np.concatenate((prev_branches*self.u,
                                 [prev_branches[-1]*self.d]))
            self.STs.append(st)  # Add nodes at each time step
#            print(self.STs)

    def _initialize_payoffs_tree_(self):
        # The payoffs when option expires
        return np.maximum(
            0, (self.STs[self.N]-self.K) if self.is_call
            else (self.K-self.STs[self.N]))

    def __check_early_exercise__(self, payoffs, node):
        early_ex_payoff = \
            (self.STs[node] - self.K) if self.is_call \
            else (self.K - self.STs[node])

        return np.maximum(payoffs, early_ex_payoff)

    def _traverse_tree_(self, payoffs):
        for i in reversed(range(self.N)):
            # The payoffs from NOT exercising the option
            payoffs = (payoffs[:-1] * self.qu +
                       payoffs[1:] * self.qd) * self.df

            # Payoffs from exercising, for American options
            if not self.is_european:
                payoffs = self.__check_early_exercise__(payoffs,
                                                        i)

        return payoffs

    def __begin_tree_traversal__(self):
        payoffs = self._initialize_payoffs_tree_()
        return self._traverse_tree_(payoffs)

    def price(self):
        self._setup_parameters_()
        self._initialize_stock_price_tree_()
        payoffs = self.__begin_tree_traversal__()

        return payoffs[0]
        
        
inputdict_am =  {"S0":40.0, "K": 39.0, "r": 0.05, "T": 3, "N": 3, "u": 1.105170918, 
              "is_eu": False, "d": 0.904837418, "is_call": True,"div":0.01}
inputdict_eu = {"S0":40.0, "K": 39.0, "r": 0.05, "T": 3, "N": 3, "u": 1.105170918, 
              "is_eu": True, "d": 0.904837418, "is_call": True,"div":0.01}
am_option = BinomialTreeOption(inputdict_am) 
eu_option = BinomialTreeOption(inputdict_eu) 
print am_option.price(),eu_option.price()


        