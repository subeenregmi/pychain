from rawtransactioncreator import createTxFromDict
import hashlib
from address import signatureGeneration, verifySig, n
"""
prevtx = {
   "Version": "01",
   "InputCount": "01",
   "txid0": "fc9e4f9c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a56779",
   "vout0": "0001",
   "sizeSig0": "006a",
   "scriptSig0": "47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a825",
   "OutputCount": "01",
   "value0": "000000000021af4b",
   "sizePk0": "0019",
   "scriptPubKey0": "76a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac",
   "locktime": "00000000"
}

{
   "Version":"01",
   "InputCount":"01",
   "txid0":"fc9e4f9c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a56779",
   "vout0":"0000",
   "sizeSig0":"0000",
   "scriptSig0":"76a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac",
   "OutputCount":"01",
   "value0":"000000000021af4b",
   "sizePk0":"0019",
   "scriptPubKey0":"76a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac",
   "locktime":"00000000"
}

rawtx = "0101fc9e4f9c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a567790000000001000000000021af4b001976a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac00000000"
double_hash = "f0db496a0f4da7a1bbcf44522de1e44301496970ceaea064add4ad576023e835"

prev_rawtx = "0101fc9e4f9c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a567790001006a47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a82501000000000021af4b001976a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac00000000"

txid_of_prevtx = "6e79b0cf91ee9a6ef4144abc4b93fb3f83b902ed0bc8c4465ee9295daa293721"

"""

tx = {
   "Version": "01",
   "InputCount": "01",
   "txid0": "fc9e4f9c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a56779",
   "vout0": "0001",
   "sizeSig0": "006a",
   "scriptSig0": "47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a825",
   "OutputCount": "01",
   "value0": "000000000021af4b",
   "sizePk0": "0019",
   "scriptPubKey0": "76a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac",
   "locktime": "00000000"
}

privKey = 300000000 #user will input all of this
randNumber = 286956185438058443321138297203732852104207394385708832038396965181764147

def createSig(tx):
   inputcounter = int(tx["InputCount"])
   for i in range(inputcounter):
      tx[f"vout{i}"] = "0000"
      tx[f"scriptSig{i}"] = tx["scriptPubKey0"]
      tx[f"sizeSig{i}"] = tx["sizePk0"]
      
   rawtx = createTxFromDict(tx) 

   rawtx = hashlib.sha256(rawtx.encode('utf-8')).hexdigest()
   rawtx = hashlib.sha256(rawtx.encode('utf-8')).hexdigest()

   rawtx = int(rawtx, 16)

   sig = signatureGeneration(privKey, randNumber, rawtx)

   if sig[1] > n/2:
      sig[1] = n - sig[1]

   sig1 = hex(sig[0])[2:]
   sig2 = hex(sig[1])[2:]
   rawsig = hex(len(sig1) // 2)[2:] + sig1 + hex(len(sig2) // 2)[2:]
   return rawsig
   
  
def main():
   sig = createSig(tx)
   print(sig)


if __name__ == "__main__":
   main()