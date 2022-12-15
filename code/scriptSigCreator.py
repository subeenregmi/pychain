from rawtransactioncreator import createTxFromDict
import hashlib
from address import signatureGeneration, n

tx1 = {
   "Version":"01",
   "InputCount":"01",
   "txid0":"fc00000c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a56779",
   "vout0":"0000",
   "sizeSig0":"0000",
   "scriptSig0":"",
   "OutputCount":"01",
   "value0":"00000000002dc6c0",
   "sizePk0":"0019",
   "scriptPubKey0":"76a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac",
   "locktime":"00000000"
}

privKey = 3000000 #user will input all of this
randNumber = 286956185438058443321138297203732852104207394385708832038396965181764147

def createSig(tx):
   inputcounter = int(tx["InputCount"])
   for i in range(inputcounter):
      tx[f"vout{i}"] = "0000"
      tx[f"scriptSig{i}"] = tx["scriptPubKey0"]
      tx[f"sizeSig{i}"] = tx["sizePk0"]
      
   rawtx = createTxFromDict(tx) 
   print(rawtx)

   rawtx = str(hashlib.sha256(rawtx.encode('utf-8')).hexdigest())
   rawtx2 = hashlib.sha256(rawtx.encode('utf-8')).hexdigest()

   rawtx2 = int(rawtx2, 16)
   print(f"rawtxhashedtwice : {rawtx2}")

   sig = signatureGeneration(privKey, randNumber, rawtx2)

   if sig[1] > n/2:
      sigU = (sig[0], sig[1])

   sig1 = hex(sigU[0])[2:]
   sig2 = hex(sigU[1])[2:]
   rawsig = hex(len(sig1) // 2)[2:] + sig1 + hex(len(sig2) // 2)[2:] + sig2
   return rawsig
   
  
def main():
   sig = createSig(tx1)
   print(sig)




if __name__ == "__main__":
   main()