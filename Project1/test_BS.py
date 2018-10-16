from BS import bsformula as bs


def main():
#    Take an example to test
#    for Stock = 100, Strike =95, riskfree = 0.1, Maturity=0.25,Vol=0.5
#    The answers from bsimpvol:
#    The call price = 13.695272738608146, delta = 0.6664651640893666 vega = 18.184325575277
#    The put price = 6.349714381299734, delta = -0.3335 vega = 18.184325575277
#    The results from matlab are that
#    call price = 13.6953, put price =6.3495
#   delta for call = 0.6665, delta for put = -0.3335
#   vega = 18.1843
    return  bs(1, 100, 95, 0.1, 0.25, 0.5), bs(-1, 100, 95, 0.1, 0.25, 0.5)



#if __name__ == '__main__':
#    main()