
def decodeRawTx(RawTx):

    dectxid = {}
    
    end = 2
    Version = RawTx[0:end]
    dectxid["Version"] = Version

    end += 2
    InputCount = RawTx[2:end]
    dectxid["InputCount"] = InputCount
    
    for i in range(int(InputCount, 16)):

        txid = RawTx[end:end + 64]
        dectxid[f"txid{i}"] = txid
        end += 64

        vout = RawTx[end:end + 4]
        dectxid[f"vout{i}"] = vout
        end += 4

        sizeSig = RawTx[end:end+4]
        dectxid[f"sizeSig{i}"] = sizeSig
        end +=4

        sizeSig = int(sizeSig, 16)
        sizeSig *= 2

        scriptSig = RawTx[end:end + sizeSig]
        dectxid[f"scriptSig{i}"] = scriptSig
        end += sizeSig
    
    OutputCount = RawTx[end:end+2]
    dectxid["OutputCount"] = OutputCount
    end += 2

    for i in range(int(OutputCount, 16)):

        value = RawTx[end: end + 16]
        dectxid[f"value{i}"] = value
        end += 16

        sizePk = RawTx[end: end+4]
        dectxid[f"sizePk{i}"] = sizePk
        end += 4

        sizePk = int(sizePk, 16)
        sizePk *= 2

        scriptPubKey = RawTx[end : end + sizePk]
        dectxid[f"scriptPubKey{i}"] = scriptPubKey
        end += sizePk


    locktime = RawTx[end: end + 8]
    dectxid["locktime"] = locktime

    return dectxid
        
def main():
    rawtx = "01018266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb44000100050000000000010000000000000064002676a921697e66d2a581463fafe887d892fd1d724825bbe214b7b2547639dbc8a87f7cc25d88ac00000000"
    decoded = decodeRawTx(rawtx)
    print(decoded)
    
if __name__ == "__main__":
    main()