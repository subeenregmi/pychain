import hashlib
from address import signatureGeneration, verifySig

'''
UPDATE - 14/12/2022 checksig needs to get hash from scriptsigcalculator
'''

script = ["a", "b", "b"]

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

stack = ["20ee920b0b5a37047165a0ceac5b57ff163524dfc6200e52a5ebea88c0345f01d320",  ]

def OPCHECKSIG(stack):
    



