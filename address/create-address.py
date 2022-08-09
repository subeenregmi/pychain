'''

address need to originate from a key or a set of numbers

hashed

and then a private key is outputted

so we need a way to randomly generate this number,

randint function

hash this key so therefore we can get a random digits meaning the public key
--> add a prefix so therefore it can be identified from a key

we also need to make it so that so this key can sign transactions to send coins
and also publicly own our tokens

the wallet need the ability to be able to spend the tokens
--> a transfer of coins is only a movement of permission to spend coins

'''



'''
def createAddress():

    private_key = random.randint(0, 2 ** 256)
    # this creates a private key that is a random number from 0 - 2^256

    string_private_key = str(private_key)
    # this converts the private key into a string format to encode into bytes

    encodedPrivateKey = string_private_key.encode()
    # encodes the pubkey ready for the sha hash

    hashPrivateKey = hashlib.sha1(encodedPrivateKey)
    # this hashes the encoded private key with a sha1 hash

    pubKey = hashPrivateKey.hexdigest()
    # this puts the hashed key into a hexidecimal format

    OxPubKey = ("0x" + pubKey)
    # this adds a 0x tag to identify the address

    print(private_key)
    print(OxPubKey)

createAddress()



'''


'''

the first step is to randomly generate a number between 1 - 2 ^ 256 


'''

import random

private_key = random.getrandbits(256)

print(private_key)

