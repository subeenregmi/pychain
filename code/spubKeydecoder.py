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
    result = breakDownLockScript("76a92069bfe8b0512755539097b01056836c042751803ff2b24c830444de0233fe1b56988ac")
    print(list(result.queue))

if __name__ == "__main__":
    main()

