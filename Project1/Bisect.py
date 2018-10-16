import numpy as np


def bisect(target, function, start=None, bounds=None, tols=[0.001, 0.010], maxiter=1000):
    '''
    :param target:  The target value for the function f
    :param function: The handle for the function f
    :param start: The x-value to start looking at
    :param bounds: The upper and lower bound beyond which x shall not exceed
    :param tols: The stopping criteria
    :param maxiter: The maximum iteration count the solver shall note exceed
    :return: The entire series of x-values
    '''
    n = 1
    xVals = []
    fdiffs = []
    if (function(bounds[0]) - target) * (function(bounds[1])-target) > 0:
        print("error! Exceed the bounds!")
        return
    if abs(function(bounds[0] - target))<tols[1]:
        xVals.append(bounds[0])
        fdiffs.append(bounds[0])
        return xVals,fdiffs
    if abs(function(bounds[1] - target))<tols[1]:
        xVals.append(bounds[1])
        fdiffs.append(bounds[1])
        return xVals,fdiffs
    while n <= maxiter:
        c = np.mean(bounds)
        xVals.append(c)
        fdiffs.append(function(c))
        if abs(function(c) - target)<tols[1] or abs(bounds[0] - bounds[1])*0.5< tols[0]:
            return xVals,fdiffs
        n += 1
        if (function(bounds[0])-target)*(function(c)-target)<0:
            bounds[1] = c
        else:
            bounds[0] = c
    print("Exceed the maxiter")
    return None





#def main():
#    y = lambda x: x ** 3 + 2 * x ** 2 - 5
#    dy = lambda x: 3 * x ** 2 + 4 * x
##   print(newton(0, y, dy, 5.0, bounds=[-100, 100]))
#
#    print bisect(0, y, start=None, bounds=[-100, 100], maxiter=1000)
#
#
#if __name__ == '__main__':
#    main()
