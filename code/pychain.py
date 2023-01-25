import json
from address import * 
import random

def loadBlockchain():
    pass



def getKeys(): 
    try:
        f = open('keys.json')
        data = json.load(f) 
        accounts = data["Accounts"]
        print("Private keys have been loaded : ")
        for privatekey in accounts:
            print(privatekey)
        f.close()
        return accounts[0]
    except: 
        randomkey = random.randint(0, n)
        print("No found wallet keys, or incorrect format")
        print(f"New Keys: {randomkey}")

def generatePublicKey(priv):
    publicKey = ECmultiplication(priv, Gx, Gy)
    pyaddress = createAddress(publicKey)
    print(f"Public Key = {publicKey}")
    print(f"Pychain Address = {pyaddress}")
    return publicKey, pyaddress

def main():
    private_key = getKeys()
    public_key, pychain_address = generatePublicKey(private_key)

    

if __name__ == "__main__":
    main()




