'''
14/12/2022 - pretty sure this is done and can be used
'''

"""
01 - Version (1 Bytes)
01 - Input Count (1 Byte)
Inputs --> 
    TXID - 32 Bytes
    Vout - 4 Bytes 
    ScriptSigSize - 00 01 (2 BYTES)
    ScriptSig
Output Count - 1 Byte
Outputs --> 
    Value - 8bytes
    ScriptPubKeySize - 2 Bytes
Locktime - 4 Bytes (00 00 00 00)
"""

"""
01000000 --> Flip
01
7967a5185e907a25225574544c31f7b059c1a191d65b53dcc1554d339c4f9efc --> Flip
00 01 --> Flip
6a
47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a825
ffffffff - sequence (Remove)
01
4baf210000000000 - Flip
19
76a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac
00000000 - Flip

"""

"""
   01    01 fc9e4f9c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a56779 0001 006a {scriptsig} 01 000000000021af4b 0019 76a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac 00000000
Version  IC                         TXID of input                            VOUT size             OC     Value        size                     ScriptPubKey                   Locktime

"""

rawtx = "0101fb06ef2e5858ee85d4a65ba4811adf6da8d6a0b3d3390740b6592263b90f40d100010020a60a52382d7077712def2a69eda3ba309b19598944aa459ce418ae53b7fb5d58010000000000000064002676a9216957e946669918c2235f7d82fb35b4d41273f3793536434ea19c6dfeda8f2c05ff88ac00000000"

def decodeRawTx(RawTx):

    dectxid = {}
    
    end = 2
    Version = RawTx[0:end]
    dectxid["Version"] = Version

    end += 2
    InputCount = RawTx[2:end]
    dectxid["InputCount"] = InputCount
    
    for i in range(int(InputCount, 16)):

        txid = rawtx[end:end + 64]
        dectxid[f"txid{i}"] = txid
        end += 64

        vout = rawtx[end:end + 4]
        dectxid[f"vout{i}"] = vout
        end += 4

        sizeSig = rawtx[end:end+4]
        dectxid[f"sizeSig{i}"] = sizeSig
        end +=4

        sizeSig = int(sizeSig, 16)
        sizeSig *= 2

        scriptSig = rawtx[end:end + sizeSig]
        dectxid[f"scriptSig{i}"] = scriptSig
        end += sizeSig
    
    OutputCount = rawtx[end:end+2]
    dectxid["OutputCount"] = OutputCount
    end += 2

    for i in range(int(OutputCount, 16)):

        value = rawtx[end: end + 16]
        dectxid[f"value{i}"] = value
        end += 16

        sizePk = rawtx[end: end+4]
        dectxid[f"sizePk{i}"] = sizePk
        end += 4

        sizePk = int(sizePk, 16)
        sizePk *= 2

        scriptPubKey = rawtx[end : end + sizePk]
        dectxid[f"scriptPubKey{i}"] = scriptPubKey
        end += sizePk


    locktime = rawtx[end: end + 8]
    dectxid["locktime"] = locktime

    return dectxid
        

def main():
    decodedTxid = decodeRawTx(rawtx)
    print(decodedTxid)

if __name__ == "__main__":
    main()