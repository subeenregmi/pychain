
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
    rawtx = "0103c6aa507dfcb1995d6203e094d46f2c6eea2579e7bd153b7b6329fbbbc9c9af1e000000424048a218902bb9fd0faa6163885c9ba29887c076abfef8c6e91b15fe59bde20b8c4022ffd50b18f3b835cfb7160ce453a83159f31a6a8650e64b60a10aa3824bef12bca065da3279ff78f360f3d0ae70b22fe4bd34b60510bda5b7d4cc6d17970fcb000000424048a218902bb9fd0faa6163885c9ba29887c076abfef8c6e91b15fe59bde20b8c4022ffd50b18f3b835cfb7160ce453a83159f31a6a8650e64b60a10aa3824bef12ddfb7d53b1d69f534f26ddbb46e0f6cb07cd30a838779c0bc434fee19e33620d000000424048a218902bb9fd0faa6163885c9ba29887c076abfef8c6e91b15fe59bde20b8c4022ffd50b18f3b835cfb7160ce453a83159f31a6a8650e64b60a10aa3824bef120200000000000000e0002676a92169b75cdd59e53f0ced19cbf30efad3ec5ea3026f805d9e1ed6aea18f5a593e29b788ac000000000000004c002676a92169d0d6247e713098d507bab69a14fe2ae731a1542f881a6cd27e8518dbf18a730688ac"
    decoded = decodeRawTx(rawtx)
    print(decoded)
    
if __name__ == "__main__":
    main()