import numpy as np

def newton(target, function, derivfun, start, bounds=None, tols=[0.001, 0.01], maxiter=1000):
    '''
    :param target: The target value for the function f
    :param function: The name of the pPthon function f
    :param derivfun: The name of the Python function representing df
    :param start: The x-value to start looking at
    :param bounds: The upper and lower bound beyond which x shall not exceed
    :param tols: The stopping criteria
    :param maxiter: The maximum iteration count the solver will be al- lowed
    :return: The entire series of x-values
    '''
    n = 1
    xVal = []
    fdiffs = []
    while n <= maxiter:
        x1 = start + (target - function(start)) / float(derivfun(start))
        y = function(x1)
        xVal.append(x1)
        fdiffs.append(y)
        if x1 > bounds[1] or x1 < bounds[0]:
            print("error! Exceed the bounds!")
            return
        elif abs(x1 - start) < tols[0] or abs(function(x1)-target)<tols[1]:
            return xVal,fdiffs
        else:
            start = x1
            n += 1
    print("Exceed the maxiter")
    return None