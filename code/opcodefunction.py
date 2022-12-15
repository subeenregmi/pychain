import hashlib
from address import signatureGeneration, verifySig

'''
UPDATE - 14/12/2022 checksig needs to get hash from scriptsigcalculator
UPDATE - 15/12/2022 Should be complete, maybe hash function needs to be looked at
'''

script2 = ["20ee920b0b5a37047165a0ceac5b57ff163524dfc6200e52a5ebea88c0345f01d320d86a3605edc878dc2472cfb1e8b823f4bd6f9edfbbd48725597c2af3a18afe07", (63903915208591347724822146685237875155546454145184102584121905894531049006320, 110503086526727362077439996637761199487973715182762248869328538836131925568226)]

def updateScript(stack):

    address = stack.pop()
    sig = stack.pop()
    size1 = int(sig[0:2], 16) * 2
    print(size1)
    sigx = sig[2:2+size1]
    print(sigx)
    size2 = int(sig[2+size1:4+size1], 16) *2
    print(size2)
    sigy = sig[4+size1:4+size1+size2]
    print(sigy)

    sigx = int(sigx, 16)
    sigy = int(sigy, 16)

    stack.append((sigx, sigy))
    stack.append(address)

    return stack



"""
OP_DUP
- Function that takes the top element in a stack and then duplicates it and puts in back in the stack
"""

def DUPLICATE(stack):
    stack.append(stack[-1])
    return stack

"""
OP_HASH 
- Function that hashes the public address into a userfriendly format, SHA256(SHA256(uncompressedpubkey)), + 5
"""

def HASH(stack):
    element = stack.pop()
    hash1 = hashlib.sha256(element.encode('utf-8')).hexdigest()
    hash2 = hashlib.sha256(hash1.encode('utf-8')).hexdigest()
    stack.append(hash2)
    return stack

"""
OP_EQUALVERIFY 
- Function that pops two elements and compares them and if they are equal dont return anything, if not return OP_FALSE 
"""

def EQUALVERIFY(stack):
    element1 = stack.pop()
    element2 = stack.pop()
    if element1 == element2:
        return stack
    else:
        stack.append("OP_FALSE")
        return stack
 
"""
 OP_CHECKSIG 
 - Function that checks the signature and public key and verfies that it is true
 """

rawtx = 95138051470213852759051785283334535143817064313784315739465689276908210910353


def OPCHECKSIG(stack):
    public_address = stack.pop()
    signature = stack.pop()
    result = verifySig(signature[0], signature[1], rawtx, public_address)
    if result == True:
        stack.append(1)
    else:
        stack.append(0)

    print(stack)


script1 = updateScript(script2)
print(script1)
OPCHECKSIG(script1)

