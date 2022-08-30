from cmath import sqrt
import math
import time
import random


n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

gen_x = 55066263022277343669578718895168534326250603453777594175500187360389116729240

gen_y = 32670510020758816978083085130507043184471273380659243275938904335757337482424

def generate_priv_key():
    
    p = random.randint(1, 2**256)
    if p < n:
        return p 
    else:
        generate_priv_key()

private_key = generate_priv_key()
print(private_key)

for x in range(1, private_key):
    pass