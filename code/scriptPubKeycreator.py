from address import createAddress

"""
14/12/2022 - Pretty sure this is completed, still need to add the opcodes into the opcodefunction.py

"""
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

pubKey = (86123958339353589454334613954037009250298301442165544159467110006827437489844, 24886167583395101331704142008829378675881745768490090403994652035580982362733)
#04 be686ed7f0539affbaf634f3bcc2b235e8e220e7be57e9397ab1c14c39137eb4 3705125aac75a865268ef33c53897c141bd092cf4d1a306b2a57e37e1386826d
pubKey2 = (86421156392539388491549897069068729212295469295611327985689750828632076446694, 26198792164421013146142002135638421386663415198568094292560769009615322474553)
#04 bf10a4206842a08e3e5904996cc4d071bf500f8dbdf7767400624b1ce6dfebe6 39ebfdaa5e573953e9a9932c9dfd156b34768a09cd3c46045c8f63132d67e839
pubKey3 = (111257321332679705494982024658038382038063280471842751199694592601667680550958, 88098359841277684460968143846434495772302670620595266603260096078387947690470)
#04 f5f9698df63a1ca074df9ed59a59561d099c796f4d0aa683527bee35addf402e c2c5e795e32d3dc24e7b0925288dc23eb15f3f7746c11904328a4529cea6d9e6

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

    print("--------------------PayToPubKeyCreated--------------------")
    print(f"Public Key = {pubKey}")
    rawp2pk = createPayToPubKey(pubKey)
    print(f"Code = {rawp2pk}")

    print("--------------------PayToPubKeyHashCreated--------------------")
    print(f"Public Key = {pubKey}")
    rawp2pkh = createPayToPubKeyHash(pubKey)
    print(f"Code = {rawp2pkh}")

    print("--------------------PayToMultSig (3) Created--------------------")
    print(f"Public Key 1 = {pubKey}\nPublic Key 2 = {pubKey2}\nPublic Key 3 = {pubKey3}")
    rawp2ms = createPayToMultiSig(pubKey, pubKey2, pubKey3)
    print(f"Code = {rawp2ms}")

    print("--------------------PayToMultSig (2) Created--------------------")
    print(f"Public Key 1 = {pubKey}\nPublic Key 2 = {pubKey2}")
    rawp2ms2 = createPayToMultiSig(pubKey, pubKey2)
    print(f"Code = {rawp2ms2}")
    print("----------------------------------------------------------------")
    
if __name__ == "__main__":
    main()