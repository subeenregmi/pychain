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
    print(breakDownLockScript("76a92169b75cdd59e53f0ced19cbf30efad3ec5ea3026f805d9e1ed6aea18f5a593e29b788ac"))
    print(breakDownLockScript("4104d30199d74fb5a22d47b6e054e2f378cedacffcb89904a61d75d0dbd407143e6595038d9d0ae3d5c3b3d6dec9e98380651f760cc364ed819605b3ff1f24106ab9ac"))
    print(breakDownLockScript("514104d30199d74fb5a22d47b6e054e2f378cedacffcb89904a61d75d0dbd407143e6595038d9d0ae3d5c3b3d6dec9e98380651f760cc364ed819605b3ff1f24106ab94104d30199d74fb5a22d47b6e054e2f378cedacffcb89904a61d75d0dbd407143e6595038d9d0ae3d5c3b3d6dec9e98380651f760cc364ed819605b3ff1f24106ab952ae"))

if __name__ == "__main__":
    main()

