#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 13:21:54 2018

@author: tianxiang
"""
'''
Q&A:
    1.call or put for question one
    2.rateCurve
    3.std not uniform
    4.return exception
'''

import numpy as np
import scipy as sp
import scipy.stats as st

norminv = st.distributions.norm.ppf
norm = st.distributions.norm.cdf
import numpy.linalg
from numpy import exp, sqrt, maximum, mean, std, log, cumsum
from numpy.random import randn, rand


def BSMonteCarlo(S0, K, T, sigma, checkpoints, rateCurve, samples=None):
    '''
    
    '''
    S0 = float(S0)
    K = float(K)
    T = float(T)
    sigma = float(sigma)
    rateCurve = float(rateCurve)

    if (samples == None):
        z = randn(checkpoints[-1], 1)
    elif (len(samples) == checkpoints[-1]):
        z = samples
    else:
        return False
    running_means = []
    running_total = 0
    start = 0
    for i in range(len(checkpoints)):
        end = checkpoints[i]
        price_samples = S0 * exp((rateCurve - 0.5 * sigma ** 2) * T + sigma * sqrt(T) * z[start:end])
        running_total = running_total + sum(price_samples)
        running_means.append(running_total / end)
        start = end

    vals = exp(-rateCurve * T) * maximum(0, price_samples - K)
    val = mean(vals)
    D = std(vals)
    error_est = D / sqrt(checkpoints[-1])
    dic = {'TV': val,  # The final value ( i.e. mean at checkpoints[-1] )
           'Means': running_means,  # The running mean at each checkpoint
           'StdDevs': D,  # The running standard deviation at each checkpoint
           'StdErrs': error_est,  # The running standard error at each checkpoint
           }
    return dic


K = 110.0;
S0 = 100.0;
r = 0.05;
sigma = 0.4;
T = 2.5;

answer = BSMonteCarlo(100, 110, 2.5, 0.4, [100, 200, 300, 400, 10000], 0.05)
print(answer)
