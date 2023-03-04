import json

def decodeRawTx(RawTx):

    dectxid = {}
    
    end = 2
    Version = RawTx[0:end]
    dectxid["Version"] = Version

    end += 2
    InputCount = RawTx[2:end]
    dectxid["InputCount"] = InputCount
    
    for i in range(int(InputCount)):

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

        scriptPubKey = RawTx[end : end + sizePk]
        dectxid[f"scriptPubKey{i}"] = scriptPubKey
        end += sizePk


    locktime = RawTx[end: end + 8]
    dectxid["locktime"] = locktime

    return dectxid
        
def main():

    rawtx = "0102c487062affb4596846495422be76a83b893b085f1eb8f0dfd794da9130c8c969000000844023f997df77592f36700060d0ad16dd7a29a86ffb263be5161a117e4f49a3ffc5405def57c7b59782f84893be173ef9ff8cbb8ad2b1e1336947e0e47edac2cb2ee840528c7a2fe647f6ecb0ba9e4351092b3addde070c0e3d6d884997e8cc83296b000000844023f997df77592f36700060d0ad16dd7a29a86ffb263be5161a117e4f49a3ffc5405def57c7b59782f84893be173ef9ff8cbb8ad2b1e1336947e0e47edac2cb2ee80200000000000000b9004c76a942690ddda9dc4549494465421bbd400bb1896a0527390701457e7997e80dc4d2841588ac000000000000000f004c76a9426916ad8380a8adea012e9bcf7590e6f86be12a3ce083978c913da56262f833b09b88ac00000000"
    decoded = decodeRawTx(rawtx)
    print(json.dumps(decoded, indent=2))

    coinbase = "01018266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb440001000a0000000003010000000000000064004c76a942694d1a07490934841e2d0497147c0a1fa690e4785f96c1d50974a572f2e8c7d05088ac00000000"
    decoded = decodeRawTx(coinbase)
    print(json.dumps(decoded, indent=2))


if __name__ == "__main__":
    main()