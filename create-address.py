'''
so we need to generate a secure number that is between 1 and 2^256 and make sure that this
number is less than n (a predetermined number given by the sec) this is to make sure 
that our private key cannot be backdoored, 

then we will get that private key and use eleptical-curve-addition to multiply the private key and a base number called g,
and then that will be our public key

after getting the public key we will use hashing to condense it into a format where it is seen as an address.

I will be using the p calculator that i created, an algorithm to break down any number into the format

i will also be using secp256k1
'''

import random
from telnetlib import EC
import decimal
import hashlib



# variables 

n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

gen_x = 55066263022277343669578718895168534326250603453777594175500187360389116729240

gen_y = 32670510020758816978083085130507043184471273380659243275938904335757337482424

p_solved = False

p_order = []

cur_gen_x = gen_x

cur_gen_y = gen_y

decimal.getcontext().prec = 20000

# this function will generate a key less than n

def generate_private_key():

    priv_key = random.randint(1, 2**256)

    if priv_key < n:
        return priv_key

    else:
        generate_private_key()
        #if a key is bigger than n then it will create another one


private_key = generate_private_key()

print(f"Private Key : {hex(private_key)}")

# this part will break down the private key into the quickest steps to get to that number in terms of ECC doubling and adding.

p = private_key

while p_solved == False:
    
    if p % 2 == 0:
        p //= 2
        p_order.insert(0, "double")

    else:
        p -=1 
        p_order.insert(0, "add")

    if p == 1:
        p_solved = True


print(f"ORDER: {p_order}\n")

# this will only be used for testing the use of inserting rather than appending.

'''
est_p = 1 

for item in p_order:
    if item == "double":
        est_p *= 2 
    else:
        est_p += 1

print(est_p)

if est_p == private_key:
    print("correcto")
else:
    print("false")
    
'''

#using this algorithm to do eleptical curve addition

def ECadd(x1, x2, y1, y2):

    lam = (decimal.Decimal(y2) - decimal.Decimal(y1)) / (decimal.Decimal(x2) - decimal.Decimal(x1))

    x3 = (lam**2) - x1 - x2

    y3 = lam * (x1 - x3) - y1

    return x3, y3

# this algorithm is used to multiply

def ECdouble(x1, y1):
    
    lam = (decimal.Decimal(3)*(decimal.Decimal(x1)**decimal.Decimal(2))+decimal.Decimal(7))/(decimal.Decimal(2)*decimal.Decimal(y1))

    x3 = (lam**2) - (2*x1)

    y3 = -(lam**3) + (3*lam*x1) - (y1)

    return x3, y3



for item in p_order:
    if item == "double":
        cur_gen_x, cur_gen_y = ECdouble(cur_gen_x, cur_gen_y)
    if item == "add":
        cur_gen_x, cur_gen_y = ECadd(cur_gen_x, gen_x, cur_gen_y, gen_y)

print(f"Public Key: x = {hex(int(cur_gen_x))}\n\ny = {hex(int(cur_gen_y))}")

public_key = "04" + str(hex(int(cur_gen_x))) + str(hex(int(cur_gen_y)))

print(f"The real pub key = \n \n{public_key}")

pychain_address = hashlib.sha256(public_key.encode('utf-8')).hexdigest()

print(f"\nPychain_address is {pychain_address}")