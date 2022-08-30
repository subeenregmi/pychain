import math
import time

P1_x = 1
P1_y = math.sqrt(2)

P2_x = 2
P2_y = 3


def ECadd(x1, x2, y1, y2):

    start  = time.perf_counter()

    lam = (y2 - y1) / (x2 - x1)

    x3 = (lam**2) - x1 - x2

    y3 = lam * (x1 - x3) - y1

    end = time.perf_counter()

    print(f"R coordinates\nx : {x3}\ny : {y3}\nLam:{lam}\nExecuted in {end - start}")
    
ECadd(P1_x, P2_x, P1_y, P2_y)


