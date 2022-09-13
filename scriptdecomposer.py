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

p2pk = "4104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac"
p2pkh = "76a91412ab8dc588ca9d5787dde7eb29569da63c3a238c88ac"
p2ms = "514104cc71eb30d653c0c3163990c47b976f3fb3f37cccdcbedb169a1dfef58bbfbfaff7d8a473e7e2e6d317b87bafe8bde97e3cf8f065dec022b51d11fcdd0d348ac4410461cbdcc5409fb4b4d42b51d33381354d80e550078cb532a34bfa2fcfdeb7d76519aecc62770f5b0e4ef8551946d8a540911abe3e7854a26f39f58b25c15342af52ae"  

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

