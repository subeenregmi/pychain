from rawtxcreator import createTxFromDict
import hashlib
from address import signatureGeneration, n

def createSig(tx, privKey, randNumber):

   inputcounter = int(tx["InputCount"])
   for i in range(inputcounter):
      tx[f"vout{i}"] = "0000"
      tx[f"scriptSig{i}"] = tx["scriptPubKey0"]
      tx[f"sizeSig{i}"] = tx["sizePk0"]
   
   rawtx = createTxFromDict(tx) 

   rawtx = str(hashlib.sha256(rawtx.encode('utf-8')).hexdigest())
   rawtx2 = hashlib.sha256(rawtx.encode('utf-8')).hexdigest()
   rawtx2 = int(rawtx2, 16)

   sig = signatureGeneration(privKey, randNumber, rawtx2)

   if sig[1] > n/2:
      sigU = (sig[0], n - sig[1])
   else:
      sigU = sig

   sig1 = hex(sigU[0])[2:]
   sig2 = hex(sigU[1])[2:]
   rawsig = hex(len(sig1) // 2)[2:] + sig1 + hex(len(sig2) // 2)[2:] + sig2

   return rawsig, rawtx2
   
def createDictWithSig(tx, privKey, randNumber):

   inputcounter = int(tx["InputCount"])
   for i in range(inputcounter):
      tx[f"vout{i}"] = "0000"
      tx[f"scriptSig{i}"] = tx["scriptPubKey0"]
      tx[f"sizeSig{i}"] = tx["sizePk0"]
      
   rawtx = createTxFromDict(tx) 

   rawtx = str(hashlib.sha256(rawtx.encode('utf-8')).hexdigest())
   rawtx2 = hashlib.sha256(rawtx.encode('utf-8')).hexdigest()
   rawtx2 = int(rawtx2, 16)

   sig = signatureGeneration(privKey, randNumber, rawtx2)

   if sig[1] > n/2:
      sigU = (sig[0], n - sig[1])
   else:
      sigU = sig

   sig1 = hex(sigU[0])[2:]
   sig2 = hex(sigU[1])[2:]
   rawsig = hex(len(sig1))[2:] + sig1 + hex(len(sig2))[2:] +sig2

   for i in range(inputcounter):
      tx[f"scriptSig{i}"] = f"{rawsig}"
      tx[f"sizeSig{i}"] = str(hex(len(rawsig))[2:])

   return tx, rawtx2
  
def main():
   pass

if __name__ == "__main__":
   main()