from address import createAddress

OPCodeDict = {
    "ac" : "OP_CHECKSIG", 
    "76" : "OP_DUP", #done
    "a9" : "OP_HASH", #done
    "88" : "OP_EQUALVERIFY", #done
    "ae" : "OP_CHECKMULTISIG",
    "51" : "OP_1",
    "52" : "OP_2",
    "53" : "OP_3",
}

def createPayToPubKey(public_Key):

    raw = "04" + str(hex(public_Key[0])[2:]) + str(hex(public_Key[1])[2:])
    bytes = len(raw)
    raw = str(hex(bytes)[2:]) + "04" + str(hex(public_Key[0])[2:]) + str(hex(public_Key[1])[2:]) + "ac"
    return raw

def createPayToPubKeyHash(public_Key):
    hashadd = createAddress(public_Key)
    bytes = len(hashadd)
    raw = "76" + "a9" + str(hex(bytes)[2:]) + str(hashadd) + "88" + "ac"
    return raw

def createPayToPubKeyHashwithHash(hash):
    hashadd = hash
    bytes = len(hashadd)
    raw = "76" + "a9" + str(hex(bytes)[2:]) + str(hashadd) + "88" + "ac"
    return raw


def createPayToMultiSig(pk1, pk2, pk3=None):

    if pk3 != None:
        
        pk1 = "04" + str(hex(pk1[0])[2:]) + str(hex(pk1[1])[2:])
        pk1len = len(pk1)
        pk2 = "04" + str(hex(pk2[0])[2:]) + str(hex(pk2[1])[2:])
        pk2len = len(pk2)
        pk3 = "04" + str(hex(pk3[0])[2:]) + str(hex(pk3[1])[2:])
        pk3len = len(pk3)
        raw = "52" + str(hex(pk1len)[2:]) + pk1 + str(hex(pk2len)[2:]) + pk2 + str(hex(pk3len)[2:]) + pk3 + "53" + "ae"
        
        return raw

    else: 

        pk1 = "04" + str(hex(pk1[0])[2:]) + str(hex(pk1[1])[2:])
        pk1len = len(pk1)
        pk2 = "04" + str(hex(pk2[0])[2:]) + str(hex(pk2[1])[2:])
        pk2len = len(pk2)
        raw = "51" + str(hex(pk1len)[2:]) + pk1 + str(hex(pk2len)[2:]) + pk2 + "52" + "ae"
        
        return raw

def main():

    p2pk = createPayToPubKey((109202608928186078798810435615768733302210942101644208012371426004931197383580, 71410754864688073695457690215266571394339322412556530640671956032708356876659))
    print(f"p2pk: {p2pk}")

    p2pkh = createPayToPubKeyHash((95440839670107969455973995843666399663662641812074432045896568980475242364517, 67400892360194400039319989411395972789004161889863182881857158544061243615929))
    print(f"p2pkh: {p2pkh}")

    p2pkh = createPayToPubKeyHashwithHash("694d1a07490934841e2d0497147c0a1fa690e4785f96c1d50974a572f2e8c7d050")
    print(f"p2pkh created with hash: {p2pkh}")


if __name__ == "__main__":
    main()