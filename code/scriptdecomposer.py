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

p2pk = "4104be686ed7f0539affbaf634f3bcc2b235e8e220e7be57e9397ab1c14c39137eb43705125aac75a865268ef33c53897c141bd092cf4d1a306b2a57e37e1386826dac"
p2pkh = "76a92169f4930d4f0bad423784acb5e6d6ac1622e4558c0db8a1c9343dcef22e7bca06e788ac"
p2ms = "514104be686ed7f0539affbaf634f3bcc2b235e8e220e7be57e9397ab1c14c39137eb43705125aac75a865268ef33c53897c141bd092cf4d1a306b2a57e37e1386826d4104bf10a4206842a08e3e5904996cc4d071bf500f8dbdf7767400624b1ce6dfebe639ebfdaa5e573953e9a9932c9dfd156b34768a09cd3c46045c8f63132d67e83952ae"  

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

