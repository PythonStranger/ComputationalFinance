from math import sqrt, exp, log, pi
from scipy.stats import norm


def bsformula(callput, S0, K, r, T, sigma, q=0.):
    '''
    :param callput: Callput is 1 for a call and -1 for a put
    :param S0: The stock price at time zero
    :param K: The strike price
    :param r: Risk-free interest rate
    :param T: The maturity time
    :param sigma: The volatility
    :param q: A continuous return rate on the underlying
    :return: A 3-tuple optionValue, delta, vega
    '''
    d_plus = ((r - q + (sigma ** 2.0) / 2) * T + log(float(S0) / K)) / (sigma * sqrt(T))
    d_minus = d_plus - sigma * sqrt(T)
    if callput == 1:
        optionValue = S0 * exp(-q * T) * norm.cdf(d_plus) - K * exp(-r * T) * norm.cdf(d_minus)
        delta = exp(-q * T) * norm.cdf(d_plus)
    elif callput == -1:
        optionValue = K * exp(-r * T) * norm.cdf(-d_minus) - S0 * exp(-q * T) * norm.cdf(-d_plus)
        delta = -exp(-q * T) * norm.cdf(-d_plus)
    else:
        print("False,input 1 or -1 for callput!")
        return
    vega = S0 * exp(-q * T) * sqrt(T) * 1 / sqrt(2.0 * pi) * exp(-d_plus ** 2 / 2.0)

    return (optionValue, delta, vega)
