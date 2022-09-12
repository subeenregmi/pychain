from pickletools import OpcodeInfo


OPCodeDict = {
    "ac" : "OP_CHECKSIG"
}

"""
Pay-To-Pubkey, where all that is needed to create this locking script, is the OP_CHECKSIG Function and the exact uncompressed public key
<number of bytes to push><UncompressedKEY><OP_CHECKSIG>
"""

p2pk = "4104a9d6840fdd1497b3067b8066db783acf90bf42071a38fe2cf6d2d8a04835d0b5c45716d8d6012ab5d56c7824c39718f7bc7486d389cd0047f53785f9a63c0c9dac"
n = 2

def breakDownLockScript(ScriptCode):
    Script = []
    CurrentChar = 0 
    byte = int(ScriptCode[0:2], 16)
    CurrentChar += 2
    if byte <= 75:
        Script.append(ScriptCode[CurrentChar:CurrentChar + 2 * byte])
    CurrentChar += 2*byte
    byte = int(ScriptCode[CurrentChar: CurrentChar + 2], 16)
    if byte <= 75:
        Script.append(ScriptCode[CurrentChar:CurrentChar + 2 * byte])
    else:
        hexByte = hex(byte)[2:]
        if hexByte in OPCodeDict:
            opcode = OPCodeDict[hexByte]
            Script.append(opcode)



    return Script
        


        
    
    

OurScript = breakDownLockScript(p2pk)
print(OurScript)