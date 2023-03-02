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
    rawtx = "010220ed724671484174625415ab8ff408aaffe42bd8c8f08c0c4a525bfcb329881800000084405d98466f9073a0c63b2ce212c0bc6d170af18f9b79421d3d3a87902b76042777404bb1bf8dd89d719e279ac7185decd226aa8115884527f84b61a26d08c10bce05e32ca14d53bec6f6471307bc01d670bc6dc51104ff01a92dbb4ef3c3117f4a8200000084405d98466f9073a0c63b2ce212c0bc6d170af18f9b79421d3d3a87902b76042777404bb1bf8dd89d719e279ac7185decd226aa8115884527f84b61a26d08c10bce050200000000000000bb004b76a94169bfe8b0512755539097b01056836c042751803ff2b24c830444de0233fe1b56988ac000000000000000d004c76a94269d0d6247e713098d507bab69a14fe2ae731a1542f881a6cd27e8518dbf18a730688ac00000000"
    decoded = decodeRawTx(rawtx)
    print(json.dumps(decoded, indent=2))


if __name__ == "__main__":
    main()