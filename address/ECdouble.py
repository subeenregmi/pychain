import math 


def ECdouble(x1, y1, a):
    
    lam = (3*(x1**2)+a)/(2*y1)

    x3 = (lam**2) - (2*x1)

    y3 = -(lam**3) + (3*lam*x1) - (y1)

    print(f"\nECDOUBLE COORDINATES:\n\nx:{x3}\ny:{y3}\n")

    return x3, y3

ECdouble(1, math.sqrt(2), 0)