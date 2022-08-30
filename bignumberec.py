import math
import decimal

decimal.getcontext().prec = 10000

gen_x = 55066263022277343669578718895168534326250603453777594175500187360389116729240

gen_y = 32670510020758816978083085130507043184471273380659243275938904335757337482424


def ECadd(x1, x2, y1, y2):

    lam = (y2 - y1) / (x2 - x1)

    x3 = (lam**2) - x1 - x2

    y3 = lam * (x1 - x3) - y1

    print(f"R coordinates\nx : {x3}\ny : {y3}\nLam:{lam}\n")

    return x3, y3

def ECdouble(x1, y1):

    lam = (decimal.Decimal(3)*(decimal.Decimal(x1)**decimal.Decimal(2))+decimal.Decimal(7))/(decimal.Decimal(2)*decimal.Decimal(y1))

    x3 = (lam**2) - (2*x1)

    y3 = -(lam**3) + (3*lam*x1) - (y1)

    print(f"\nECDOUBLE COORDINATES:\n\nx:{x3}\n\ny:{y3}\n")

    return x3, y3


for i in range(32):
    gen_x, gen_y = ECdouble(gen_x, gen_y)