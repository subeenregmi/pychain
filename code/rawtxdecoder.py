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
    rawtx = "0105bca065da3279ff78f360f3d0ae70b22fe4bd34b60510bda5b7d4cc6d17970fcb0000004240d96e2e29345a917d3e53490b9de155b6726a2e7c48e3a8edf656ab7a17b17c8c4063cdc8e17a8a68433e4097219d8f229c6d0a11f9cdac38d4d467ed9bbf4a8c8fcd1b75e9bd1d170afa45ef11a2807420080d7fe08a85bea4d7667dd6b78c32940000004240d96e2e29345a917d3e53490b9de155b6726a2e7c48e3a8edf656ab7a17b17c8c4063cdc8e17a8a68433e4097219d8f229c6d0a11f9cdac38d4d467ed9bbf4a8c8f3c579fd881aaea064ceb3806446a01e1de60027624347a155e1958f45e80ab790000004240d96e2e29345a917d3e53490b9de155b6726a2e7c48e3a8edf656ab7a17b17c8c4063cdc8e17a8a68433e4097219d8f229c6d0a11f9cdac38d4d467ed9bbf4a8c8fd4e549ad307d49326bd94b288e8370900906b3984890f16cdc358b1d79fa219e0000004240d96e2e29345a917d3e53490b9de155b6726a2e7c48e3a8edf656ab7a17b17c8c4063cdc8e17a8a68433e4097219d8f229c6d0a11f9cdac38d4d467ed9bbf4a8c8f03ad79e7c9de56aa3ece1a01a9b780f50113e63670bca4f3fb6d6b2c8180088f0000004240d96e2e29345a917d3e53490b9de155b6726a2e7c48e3a8edf656ab7a17b17c8c4063cdc8e17a8a68433e4097219d8f229c6d0a11f9cdac38d4d467ed9bbf4a8c8f0200000000000001c0002576a92069bfe8b0512755539097b01056836c042751803ff2b24c830444de0233fe1b56988ac00000000000000fc002676a92169d0d6247e713098d507bab69a14fe2ae731a1542f881a6cd27e8518dbf18a730688ac00000000"
    decoded = decodeRawTx(rawtx)
    print(json.dumps(decoded, indent=2))

if __name__ == "__main__":
    main()