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
    print(breakDownLockScript("4104a09760dae68f23cb1a57cffd3bd4d2247f6128d9695f6f0802248809d1639023301c863f672a2c62d622fc5d42a7d2a72c4fb77bb5637d547cbf0ac6e9999027ac"))

if __name__ == "__main__":
    main()

