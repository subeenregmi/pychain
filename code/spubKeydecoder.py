import queue

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

    script = queue.Queue()
    char = 0
    while char != len(scriptcode):
        byte = int(scriptcode[char:char+2], 16)
        char += 2 
        if byte <= 75:
            script.put(scriptcode[char: char + byte])
            char += byte
        else:
            hexbyte = hex(byte)[2:]
            if hexbyte in OPCodeDict:
                script.put(OPCodeDict[hexbyte])

    return script

def main():

    # Pay-to-Pub-Key-Hash (P2PKH)
    lockscript = "76a94269dfa746b659c0b7d17f3772079dcd70eddec704c1a888a3ef2e71e17cc5fef4e488ac"

    result = breakDownLockScript(lockscript)
    print(list(result.queue))

if __name__ == "__main__":
    main()

