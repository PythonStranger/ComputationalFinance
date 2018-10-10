#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 13:21:54 2018

@author: tianxiang
"""
'''
Q&A:
    1. running std for interval between checkpoint or ?
'''

import scipy.stats as st
import numpy as np

norminv = st.distributions.norm.ppf
norm = st.distributions.norm.cdf
from numpy import exp, sqrt, maximum, mean, std
from numpy.random import randn, rand


def BSMonteCarlo(S0, K, T, sigma, checkpoints, rateCurve, samples=None):
    '''
    :param S0:
    :param K:
    :param T:
    :param sigma:
    :param checkpoints:
    :param rateCurve:
    :param samples:
    :return:
    '''

    S0 = float(S0)
    K = float(K)
    T = float(T)
    sigma = float(sigma)
    tensors = [1, 3, 6, 12, 24, 36, 60]
    rate = np.interp(12 * T, tensors, rateCurve)

    if (samples == None):
        z = rand(checkpoints[-1], 1)
    elif (len(samples) >= checkpoints[-1]):
        z = samples
    else:
        raise Exception("The samples are less than required")
    z = norminv(z)

    running_means = []
    running_std = []
    running_stdError = []
    running_total = 0
    start = 0

    for i in range(len(checkpoints)):
        end = checkpoints[i]
        price_samples = S0 * exp((rate - 0.5 * sigma ** 2) * T + sigma * sqrt(T) * z[0:end])
        #        price_samples_2 = S0 * exp((rate - 0.5 * sigma ** 2) * T + sigma * sqrt(T) * z[0:end])
        #        running_total = running_total + sum(price_samples)
        vals = exp(-rate * T) * maximum(0, price_samples - K)
        #        val = mean(vals)
        running_total = sum(vals)
        running_means.append(running_total[0] / end)
        running_std.append(std(vals))
        running_stdError.append(std(vals) / sqrt(end))
    #        start = end

    #    vals = exp(-rate * T) * maximum(0, price_samples - K)
    val = mean(vals)
    #    The running means and stdDevs and StdErrs I calculated are option's Means and StdDevs and StdErrs,
    #    before the each checkpoint not between the each point

    dic = {'TV': val,  # The final value ( i.e. mean at checkpoints[-1] )
           'Means': running_means,  # The running mean before each checkpoint
           'StdDevs': running_std,  # The running standard deviation at each checkpoint
           'StdErrs': running_stdError,  # The running standard error at each checkpoint
           }
    return dic

#
# K = 110.0;
# S0 = 100.0;
# r = 0.05;
# sigma = 0.4;
# T = 2.5;
#
# answer = BSMonteCarlo(100, 110, 2.5, 0.4, [100, 200, 300, 400, 10000],
#                      [.01, .03, .04, .04, .05, .051, .1])
# print(answer)
