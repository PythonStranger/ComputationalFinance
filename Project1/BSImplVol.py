from Bisect import newton, bisect
from BS import bsformula


def bsimpvol(callput, S0, K, r, T, price, q=0., priceTolerance=0.01,
             method='bisect', reportCalls=False):
    '''
    :param callput: Callput is 1 for a call and -1 for a put
    :param S0: The stock price at time zero
    :param K: The strike price
    :param r: Risk-free interest rate
    :param T: The maturity time
    :param price: The price of the option
    :param q: A continuous return rate on the underlying
    :param priceTolerance:
    :param method: The method used to calculate sigma
    :param reportCalls: The record of call bsformula
    :return: sigma, numbers of calling bsformula
    '''

    y = lambda sigma: bsformula(callput, S0, K, r, T, sigma)[0]
    dy = lambda sigma: bsformula(callput, S0, K, r, T, sigma)[2]
    if method == 'bisect':
        if bisect(price, y, bounds=[0.01, 1])[0] == None:
            return None
        item = bisect(price, y, bounds=[0.01, 1])[0]
    elif method == 'newton':
        if newton(price, y, dy, start=1, bounds=[0.01, 1])[0] ==None:
            return None
        item = newton(price, y, dy, start=1, bounds=[0.01, 1])[0]
 
    if item != None:
        sigma = item[-1]
    else:
        sigma = item
        return None
    if reportCalls == True:
        return (sigma, len(item))
    else:
        return sigma


a = bsimpvol(1, 100, 180, 0.1, 0.25,  0.000289, q=0., priceTolerance=0.01,
             method='bisect', reportCalls=False)
b = bsimpvol(1, 100, 180, 0.1, 0.25,  0.000289, q=0., priceTolerance=0.01,
             method='newton', reportCalls=False)
##c =  bsimpvol(1, 100, 95, 0.1, 0.25, 13.6953, q=0., priceTolerance=0.01,
##             method='bisect', reportCalls=True)
##d = bsimpvol(1, 100, 95, 0.1, 0.25,  13.6953, q=0., priceTolerance=0.01,
##             method='newton', reportCalls=True)
print a,b
##print c,d
