'''
so here we would need to prove that you are using a private key pair

we do this buy checking if the private key that you submit turns into the address

if so we can spend the funds on this specific address and therefore create a transaction

this is a small step to just verify ownership
'''

import hashlib

def verifiedOwner(publicKey, privKey):

    string_private_key = str(privKey)
    # this converts the private key into a string format to encode into bytes

    encodedPrivateKey = string_private_key.encode()
    # encodes the pubkey ready for the sha hash

    hashPrivateKey = hashlib.sha1(encodedPrivateKey)
    # this hashes the encoded private key with a sha1 hash

    pubKey = hashPrivateKey.hexdigest()
    # this puts the hashed key into a hexidecimal format

    pubKey = ("0x" + pubKey)
    # this adds a 0x tag to identify the address

    if publicKey == pubKey:
        _verified = True
    else:
        _verified = False
