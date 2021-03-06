#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 13:21:54 2018

@author: tianxiang

Q&A:
1. N*M or M*N
"""
import numpy as np
import scipy.stats as st
from numpy.random import randn, rand

norminv = st.distributions.norm.ppf
norm = st.distributions.norm.cdf
from numpy import exp, sqrt, mean


def MCStockPrices(S0, sigma, rateCurve, t, samples, integrator):
    '''
    :param S0: is the stock prices at time t0.
    :param sigma: is the constant volatility.
    :param rateCurve: is an InterestRateCurve stored as a numpy array.
    :param t: is an array of fixing times ti; i = 1 : : :N to simulate to.
    :param samples: is an array of uniform random samples to use. The
                    length of samples should be N M where N is the number of 
                    fixing times and M is the number of paths.
    :param integrator: controls how the samples are generated according to the following value list
            'standard', where the paths are generated by using the
            solution of the Black-Scholes SDE step-by-step
            'euler', to use Euler-method integration of the Black-
            Scholes SDE
            'milstein', to use Milstein-method integration of the Black-
            Scholes SDE
    :return: a numpy array of simulated stock prices having the same dimensions as samples.
    '''
    S0 = float(S0)
    sigma = float(sigma)

    if samples.all() == None:
        raise Exception("Please input samples!")
    samples = norminv(samples)

    N, M = np.shape(samples)
    stock_path = np.zeros((N, M))

    # standard    
    if (integrator == 'standard'):
        for n in range(len(t)):
            tensors = [1, 3, 6, 12, 24, 36, 60]
            rate = np.interp(12 * t[n], tensors, rateCurve)
            if (n == 0):
                stock_path[n, :] = S0 * exp((rate - 0.5 * sigma ** 2) * t[n] + sigma * sqrt(t[n]) * samples[n, :])
            else:
                stock_path[n, :] = stock_path[n - 1, :] * exp(
                    (rate - 0.5 * sigma ** 2) * (t[n] - t[n - 1]) + sigma * sqrt((t[n] - t[n - 1])) * samples[
                                                                                                      n, :])

    # euler
    if (integrator == 'euler'):
        for n in range(len(t)):
            tensors = [1, 3, 6, 12, 24, 36, 60]
            rate = np.interp(12 * t[n], tensors, rateCurve)
            if (n == 0):
                stock_path[n, :] = S0 * (1.0 + rate * t[n] + sigma * sqrt(t[n]) * samples[n, :])
            else:
                stock_path[n, :] = stock_path[n - 1, :] * (
                        1.0 + rate * (t[n] - t[n - 1]) + sigma * sqrt((t[n] - t[n - 1])) * samples[n, :])

    # milstein
    if (integrator == 'milstein'):
        for n in range(len(t)):
            tensors = [1, 3, 6, 12, 24, 36, 60]
            rate = np.interp(12 * t[n], tensors, rateCurve)
            if (n == 0):
                stock_path[n, :] = S0 * (1.0 + rate * t[n] + sigma * sqrt((t[n])) * samples[n, :]
                                         + sigma ** 2 * (samples[n, :] ** 2 - 1) * t[n] / 2.0)
            else:
                stock_path[n, :] = stock_path[n - 1, :] * (
                        1.0 + rate * (t[n] - t[n - 1]) + sigma * sqrt((t[n] - t[n - 1])) * samples[n, :]
                        + sigma ** 2 * (samples[n, :] ** 2 - 1) * (t[n] - t[n - 1]) / 2.0)

    return stock_path

#
K = 95.0;
S0 = 100.0;
r = 0.1;
sigma = 0.5;
T = 0.25;
t = [0.05,0.1, 0.15, 0.2, 0.25]
rateCurve = [.1, .1, .1, .1, .1, .1, .1]
# # (S0, sigma, rateCurve, t, samples, integrator)
# a = {"standard":mean(
#    MCStockPrices(S0, sigma, [.01, .03, .04, .04, .05, .051, .1], [1, 2, 3, 4, 5], rand(5, 1000000), 'standard')[-1,
#    :]),
#     "euler":mean(MCStockPrices(S0, sigma, [.01, .03, .04, .04, .05, .051, .1], [1, 2, 3, 4, 5], rand(5, 1000000), 'euler')[-1,
#          :]),
#     "milstein":mean(MCStockPrices(S0, sigma, [.01, .03, .04, .04, .05, .051, .1], [1, 2, 3, 4, 5], rand(5, 1000000), 'milstein')[
#          -1, :])}
#
b = MCStockPrices(S0, sigma, rateCurve, t,  rand(5, 1000000), 'standard')[0, :]
