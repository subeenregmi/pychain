import random
from address import *
from spubKeycreator import createPayToPubKeyHash
from rawtxcreator import createTxFromDict
from rawtxdecoder import decodeRawTx

"""
function to create a valid set of txs

person1 ---> person2 50 coins

person1 tx will contain a correct scriptPubKey based on person2s public key 

person 2 --> person3 50 coins 

person2 sends a random wallet person3 50 coins, this will have the correct script sig to break person1s scriptpubkey

"""

class Person:
    def __init__(self, privatekey):
        self.privatekey = privatekey
        self.publickey = ECmultiplication(self.privatekey, Gx, Gy)
        self.pyaddress = createAddress(self.publickey)

    def sendRandTransactionTX1(self, publicKey):
        
        scriptPubKey = createPayToPubKeyHash(publicKey)
        value = random.randint(1, 100)

        dict = {
            "Version":"01",
            "InputCount":"01",
            "txid0":"a441b15fe9a3cf56661190a0b93b9dec7d04127288cc87250967cf3b52894d11", #random hashed
            "vout0":"0001",
            "sizeSig0":"0020",
            "scriptSig0":"ce922519a3c3ecaf9b0986c2449c7680895c15f4b0e9818e994e14a4d28b6aaf", #transaction hashed 
            "OutputCount":"01",
            "value0":"{0:016x}".format(value),
            "sizePk0":"{0:04x}".format(len(scriptPubKey)//2),
            "scriptPubKey0":f"{scriptPubKey}",
            "locktime":"00000000"   
        }
        
        rawtx = createTxFromDict(dict)
        print(f"RawTX to {createAddress(publicKey)}\nPublic Key: {publicKey}\nScriptPubKey = {scriptPubKey}")
    
    def sendRandomTransactionTX2(self):
        pass



def main():
    p1 = Person(32323232232)
    p1.sendRandTransactionTX1(p1.publickey)


if __name__ == "__main__":
    main()