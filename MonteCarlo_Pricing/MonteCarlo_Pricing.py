#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 10:36:28 2018

@author: tianxiang
"""

import math
import numpy as np
import scipy.stats as st
from numpy.random import randn, rand
norminv = st.distributions.norm.ppf

class MonteCarloPrice(object):
    def __init__(self,params):
        self.S0 = params.get("S0",0)
        self.K = params.get("K",0)
        self.r = params.get("r",0)
        self.sample = params.get("sample", 0)
        self.sigma = params.get("sigma", 0)  # Volatility
        self.delta_t = params.get("delta_t",0)
        self.is_call = params.get("is_call", True)  # Call or put
        self.is_european = params.get("is_eu", True)  # Eu or Am

        
    def _mirror_sample(self):
        self.sample = np.concatenate((self.sample,-self.sample), axis = 1)
        
    def _initialize_stock_tree(self):
        self.N, self.M = np.shape(self.sample)
        self.stock_tree = np.zeros((self.N,self.M))
        self.stock_tree[0,:] = self.S0 * np.exp((self.r- (self.sigma**2)/2) * self.delta_t
                                                    + self.sigma * math.sqrt(self.delta_t)
                                                    * self.sample[0,:])
                                                    
        for i in range(1,self.N):
            self.stock_tree[i,:] = self.stock_tree[i-1,:] * np.exp((self.r- (self.sigma**2)/2) * self.delta_t
                                                    + self.sigma * math.sqrt(self.delta_t)
                                                    * self.sample[i,:])
    def price(self):
        self._mirror_sample()
        self._initialize_stock_tree()
        if self.is_call == True:
            payoffs = np.maximum(self.stock_tree[-1,:] - self.K, 0)
        else:
            payoffs = np.maximum(self.K- self.stock_tree[-1,:], 0)
        option_price = payoffs.mean() * math.exp(-(self.r)*(self.delta_t*self.N))
        return option_price
    
inputdict =  {"S0":40.0, "sigma":0.1, "K": 39.0, "r": 0.05, "delta_t": 1, "sample" : randn(4,1000000), "is_call": True}
eu_option = MonteCarloPrice(inputdict)
print eu_option.price()

        
        
        