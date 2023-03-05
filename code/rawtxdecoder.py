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

    rawtx = "010340528c7a2fe647f6ecb0ba9e4351092b3addde070c0e3d6d884997e8cc83296b0000008440141deb0858c0fcc8e91e9b7ab00819a14839dfccfcff6f3f465a6f09dd61c459406ab8b559ddb5b44c8c79188da949df058d9e22aba6e4a230a64e108593a423907aae21cd95f841e095ae7ae7803267544c7cec9938e75fe6cfae27bf9a53912e0000008440141deb0858c0fcc8e91e9b7ab00819a14839dfccfcff6f3f465a6f09dd61c459406ab8b559ddb5b44c8c79188da949df058d9e22aba6e4a230a64e108593a4239027e877d963da2c3fe5fd2e6617591f87bd8468402ba65dba109f26985c2368bd0000008440141deb0858c0fcc8e91e9b7ab00819a14839dfccfcff6f3f465a6f09dd61c459406ab8b559ddb5b44c8c79188da949df058d9e22aba6e4a230a64e108593a423900200000000000000d5004c76a942690ddda9dc4549494465421bbd400bb1896a0527390701457e7997e80dc4d2841588ac00000000000000bb004c76a9426916ad8380a8adea012e9bcf7590e6f86be12a3ce083978c913da56262f833b09b88ac00000000"
    decoded = decodeRawTx(rawtx)
    print(json.dumps(decoded, indent=2))

    # coinbase = "01018266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb440001000a0000000003010000000000000064004c76a942694d1a07490934841e2d0497147c0a1fa690e4785f96c1d50974a572f2e8c7d05088ac00000000"
    # decoded = decodeRawTx(coinbase)
    # print(json.dumps(decoded, indent=2))


if __name__ == "__main__":
    main()