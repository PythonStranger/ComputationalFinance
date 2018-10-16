#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 15:18:17 2018

@author: tianxiang

Q&A
1.tN == T ?
"""
from MCStockPrices import MCStockPrices
# from BSMonteCarlo import BSMonteCarlo
import numpy as np
import scipy.stats as st
from numpy.random import randn, rand
import pandas as pd

norminv = st.distributions.norm.ppf
norm = st.distributions.norm.cdf
from numpy import exp, sqrt, mean, maximum, std


def MCOptionPrices(S0, K, T, rateCurve, sigma, t,
                   checkpoints, samples, integrator):
    '''
    :param S0: is the stock prices at time t0.
    :param K: is the strike price.
    :param T: is the expiration date of the European option.
    :param rateCurve: is an InterestRateCurve stored as a numpy array.
    :param sigma: is the constant volatility.
    :param t: is an array of 
xing times ti; i = 1 : : :N to simulate to.
    :param checkpoints: is an ordered list of integer sample counts in
                        the range [1;M] at which to return the running mean, standard
                        deviation, and estimated error.
    :param samples: is an array of uniform random samples to use. The
                    length of samples should be N M where N is the number of
                    
xing times and M is the number of paths.
    :param integrator: controls how the samples are generated according
                        to the following value list
    :return:
    '''
    '''
    { 'TV': , # The final value ( i.e. mean of option price at time t_0
                using NxM uniform random samples)
        'Means': , # The running mean at each checkpoint
        'StdDevs': , # The running standard deviation at each checkpoint
        'StdErrs': , # The running standard error at each checkpoint
}
    '''
    S0 = float(S0)
    K = float(K)
    T = float(T)
    sigma = float(sigma)

    #    Get the stock price at time t0
    stock_path = MCStockPrices(S0, sigma, rateCurve, t, samples, integrator)[-1, :]
    #    BSMonteCarlo(S0, K, T, sigma, checkpoints, rateCurve, samples=None)

    running_std = []
    running_stdError = []
    running_means = []
    running_total = 0
    start = 0

    #   Get discount rate
    discount = 1
    for k in range(1, len(t)):
        tensors = [1, 3, 6, 12, 24, 36, 60]
        rate = np.interp(12 * t[k], tensors, rateCurve)
        discount = discount * exp(-rate * (t[k] - t[k - 1]))

    for i in range(len(checkpoints)):
        end = checkpoints[i]
        price_samples = stock_path[:end]
        vals = discount * maximum(0, price_samples - K)
        #        vals = [1,2]
        running_total = sum(vals)
        running_means.append(running_total / end)
        running_std.append(std(vals))
        running_stdError.append(std(vals) / sqrt(end))
    #        start = end

    val = mean(vals)

    dic = {'TV': val,  # The final value ( i.e. mean at checkpoints[-1] )
           'Means': running_means,  # The running mean before each checkpoint
           'StdDevs': running_std,  # The running standard deviation at each checkpoint
           'StdErrs': running_stdError,  # The running standard error at each checkpoint
           }
    return dic

# K = 110.0;
# S0 = 100.0;
# r = 0.05;
# sigma = 0.4;
# T = 2.5;
# a = MCOptionPrices(S0, K, T, [.01, .03, .04, .04, .05, .051, .1], sigma, [1, 2, 3, 4, 5], [100, 200, 300, 400, 10000],
#                    rand(5, 10000), 'milstein')
# b = MCOptionPrices(S0, K, T, [.01, .03, .04, .04, .05, .051, .1], sigma, [1, 2, 3, 4, 5], [100, 200, 300, 400, 10000],
#                    rand(5, 10000), 'euler')
# c = MCOptionPrices(S0, K, T, [.01, .03, .04, .04, .05, .051, .1], sigma, [1, 2, 3, 4, 5], [100, 200, 300, 400, 10000],
#                    rand(5, 10000), 'standard')
# K = 95.0;
# S0 = 100.0;
# r = 0.1;
# sigma = 0.5;
# T = 0.25;
# t = [0.05,0.1, 0.15, 0.2, 0.25]
# rateCurve = [.1, .1, .1, .1, .1, .1, .1]
#
# c = MCOptionPrices(S0, K, T, rateCurve, sigma, t, [100, 200, 300, 400, 10000],
#                    rand(5, 10000), 'standard')
# print(c)