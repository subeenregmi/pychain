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

"""
Pay-To-Pubkey, where all that is needed to create this locking script, is the OP_CHECKSIG Function and the exact uncompressed public key
<number of bytes to push> <UncompressedKEY> <OP_CHECKSIG>

Pay-To-PubKey-Hash, where the locking script requires that the public address is hashed and matches with the address provided in the locking script.
<OP_DUP> <Hashing algorithm to get address> <number of bytes to push> <Compressed address> <OP_EQUALVERIFY> <OP_CHECKSIG>

Pay-To-MultiSig, where locking script requires the signature of more than one private address, takes alot of space
<NUM of signatures> <Publickey(s)> <NUM of publickeys> <OP_CHECKMULTISIG>
"""

p2pk = "4104a9d6840fdd1497b3067b8066db783acf90bf42071a38fe2cf6d2d8a04835d0b5c45716d8d6012ab5d56c7824c39718f7bc7486d389cd0047f53785f9a63c0c9dac"
p2pkh = "76a914fde0a08625e327ba400644ad62d5c571d2eec3de88ac"
p2ms = "524104be686ed7f0539affbaf634f3bcc2b235e8e220e7be57e9397ab1c14c39137eb43705125aac75a865268ef33c53897c141bd092cf4d1a306b2a57e37e1386826d4104bf10a4206842a08e3e5904996cc4d071bf500f8dbdf7767400624b1ce6dfebe639ebfdaa5e573953e9a9932c9dfd156b34768a09cd3c46045c8f63132d67e8394104f5f9698df63a1ca074df9ed59a59561d099c796f4d0aa683527bee35addf402ec2c5e795e32d3dc24e7b0925288dc23eb15f3f7746c11904328a4529cea6d9e653ae"  

def breakDownLockScript(scriptcode):

    script = []
    char = 0
    while char != len(scriptcode):
        byte = int(scriptcode[char:char+2], 16)
        char += 2 
        if byte <= 75:
            script.append(scriptcode[char : char + 2*byte])
            char += 2*byte
        else:
            hexbyte = hex(byte)[2:]
            if hexbyte in OPCodeDict:
                script.append(OPCodeDict[hexbyte])
                

    return script


def main():

    payToPubkey = breakDownLockScript(p2pk)
    payToPubkeyHash = breakDownLockScript(p2pkh)
    payToMultiSig = breakDownLockScript(p2ms)
    print(f"---------------PayToPubKey (P2PK)---------------")
    print(f"Raw: {p2pk}")
    print(f"Decomposed : {payToPubkey}")
    print(f"---------------PayToPubKeyHash (P2PKH)---------------")
    print(f"Raw : {p2pkh}")
    print(f"Decomposed : {payToPubkeyHash}")
    print(f"---------------PayToMultiSig (P2PKH)---------------")
    print(f"Raw : {p2ms}")
    print(f"Decomposed : {payToMultiSig}")

if __name__ == "__main__":
    main()

