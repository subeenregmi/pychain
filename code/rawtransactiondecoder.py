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

rawtx = "0101fc9e4f9c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a567790001006a47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a82501000000000021af4b001976a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac00000000"

def decodeRawTx(RawTx):

    inputs = {}
    outputs = {}
    
    end = 2
    Version = RawTx[0:end]
    end += 2
    InputCount = RawTx[2:end]
    
    for i in range(int(InputCount, 16)):

        txid = rawtx[end:end + 64]
        inputs[f"txid{i}"] = txid
        end += 64

        vout = rawtx[end:end + 4]
        inputs[f"vout{i}"] = vout
        end += 4

        size = rawtx[end:end+4]
        inputs[f"size{i}"] = size
        end +=4

        size = int(size, 16)
        size *= 2

        scriptSig = rawtx[end:end + size]
        inputs[f"scriptSig{i}"] = scriptSig
        end += size
    
    OutputCount = rawtx[end:end+2]
    end += 2

    for i in range(int(InputCount, 16)):

        value = rawtx[end: end + 16]
        outputs[f"value{i}"] = value
        end += 16

        size = rawtx[end: end+4]
        outputs[f"size{i}"] = size
        end += 4

        size = int(size, 16)
        size *= 2

        scriptPubKey = rawtx[end : end + size]
        outputs[f"scriptPubKey{i}"] = scriptPubKey
        end += size


    locktime = rawtx[end: end + 8]

    print("-----------------------------------")

    print(f"Version = {Version}")
    print(f"Input Count = {InputCount}")
    for key, value in inputs.items():
        print(key + ":" + value)

    print("-----------------------------------")

    print(f"Output Count = {OutputCount}")
    for key, value in outputs.items():
        print(key + ":" + value)

    print("-----------------------------------")

    print(f"Locktime = {locktime}")

    print("-----------------------------------")

    return Version, InputCount, inputs, OutputCount, outputs, locktime










    
        


decodeRawTx(rawtx)