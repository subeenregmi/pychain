from  address import createAddress

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
    bytes = len(raw) // 2 
    raw = str(hex(bytes)[2:]) + "04" + str(hex(public_Key[0])[2:]) + str(hex(public_Key[1])[2:]) + "ac"
    return raw

def createPayToPubKeyHash(public_Key):
    hashadd = createAddress(public_Key)
    bytes = len(hashadd) // 2
    raw = "76" + "a9" + str(hex(bytes)[2:]) + str(hashadd) + "88" + "ac"
    return raw

def createPayToMultiSig(pk1, pk2, pk3=None):

    if pk3 != None:
        
        pk1 = "04" + str(hex(pk1[0])[2:]) + str(hex(pk1[1])[2:])
        pk1len = len(pk1) // 2
        pk2 = "04" + str(hex(pk2[0])[2:]) + str(hex(pk2[1])[2:])
        pk2len = len(pk2) // 2
        pk3 = "04" + str(hex(pk3[0])[2:]) + str(hex(pk3[1])[2:])
        pk3len = len(pk3) // 2
        raw = "52" + str(hex(pk1len)[2:]) + pk1 + str(hex(pk2len)[2:]) + pk2 + str(hex(pk3len)[2:]) + pk3 + "53" + "ae"
        
        return raw

    else: 

        pk1 = "04" + str(hex(pk1[0])[2:]) + str(hex(pk1[1])[2:])
        pk1len = len(pk1) // 2
        pk2 = "04" + str(hex(pk2[0])[2:]) + str(hex(pk2[1])[2:])
        pk2len = len(pk2) // 2
        raw = "51" + str(hex(pk1len)[2:]) + pk1 + str(hex(pk2len)[2:]) + pk2 + "52" + "ae"
        
        return raw

def main():
    pass

if __name__ == "__main__":
    main()