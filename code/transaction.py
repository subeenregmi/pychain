from address import *
from scriptPubKeycreator import *
from rawtransactioncreator import *
from scriptPubKeydecomposer import *
from rawtransactiondecoder import *


"""
person1 sends person2 some tokens (100)[tx1] then the person2 sends to person3[tx2] we are going to check if that can happen using the scriptPubkey from tx1 and the signature in tx2

"""
#person 1

private_key_1 = 8000
public_key_1 = ECmultiplication(private_key_1, Gx, Gy)
print(f"Person 1: {public_key_1}")

#person 2 

private_key_2 = 3300
public_key_2 = ECmultiplication(private_key_2, Gx, Gy)
print(f"Person 2: {public_key_2}")

#creation of tx1 p1 --> p2 the txid of input doesnt matter we are only making the scriptPubKey(locking) script accurate using the p2 public key P2PKH

scriptPubKey_1 = createPayToPubKeyHash(public_key_1)
print(f"ScriptPubKey for tx1: {scriptPubKey_1}")

rawtx1 = "0101fb06ef2e5858ee85d4a65ba4811adf6da8d6a0b3d3390740b6592263b90f40d100010020a60a52382d7077712def2a69eda3ba309b19598944aa459ce418ae53b7fb5d58010000000000000064002676a9216957e946669918c2235f7d82fb35b4d41273f3793536434ea19c6dfeda8f2c05ff88ac00000000"
print(f"RawTx1: {rawtx1}")
txid1 = hashlib.sha256(rawtx1.encode('utf-8')).hexdigest()
print(f"Txid for tx1 {txid1}")

rawtx1_dict = {
    'Version': '01', 
    'InputCount': '01', 
    'txid0': 'fb06ef2e5858ee85d4a65ba4811adf6da8d6a0b3d3390740b6592263b90f40d1', #these really dont matter
    'vout0': '0001', 
    'sizeSig0': '0020', 
    'scriptSig0': 'a60a52382d7077712def2a69eda3ba309b19598944aa459ce418ae53b7fb5d58', #these really dont matter
    'OutputCount': '01', 
    'value0': '0000000000000064', 
    'sizePk0': '0026', 
    'scriptPubKey0': '76a9216957e946669918c2235f7d82fb35b4d41273f3793536434ea19c6dfeda8f2c05ff88ac', #this is the only thing that matters
    'locktime': '00000000'
}




