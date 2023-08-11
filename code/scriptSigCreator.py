import json

from rawtxcreator import createTxFromDict
import hashlib
from address import signatureGeneration, n

def createSig(tx, privKey, randNumber):
   #tx is Dictionary

   inputcounter = int(tx["InputCount"])
   for i in range(inputcounter):
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
   rawsig = hex(len(sig1))[2:] + sig1 + hex(len(sig2))[2:] + sig2

   return rawsig, rawtx2
   
def createDictWithSig(tx, privKey, randNumber):

   inputcounter = int(tx["InputCount"])
   for i in range(inputcounter):
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
      tx[f"sizeSig{i}"] = str(hex(len(rawsig))[2:]).zfill(4)

   return tx, rawtx2

def createEmptyTxForSign(tx):
   inputcounter = int(tx["InputCount"])
   for i in range(inputcounter):
      tx[f"scriptSig{i}"] = tx["scriptPubKey0"]
      tx[f"sizeSig{i}"] = tx["sizePk0"]

   rawtx = createTxFromDict(tx)

   rawtx = str(hashlib.sha256(rawtx.encode('utf-8')).hexdigest())
   rawtx2 = hashlib.sha256(rawtx.encode('utf-8')).hexdigest()
   rawtx2 = int(rawtx2, 16)

   return rawtx2
  
def main():
   tx = {'Version': '01', 'InputCount': '01', 'txid0': '7b6632fce3914fd9b098a10760a995a41dcb260a9a740b7ed6fd0902e2c47ed6', 'vout0': '0001', 'sizeSig0': '0005', 'scriptSig0': '0000000000', 'OutputCount': '01', 'value0': '0000000000000064', 'sizePk0': '0026', 'scriptPubKey0': '76a92169b75cdd59e53f0ced19cbf30efad3ec5ea3026f805d9e1ed6aea18f5a593e29b788ac', 'locktime': '00000000'}
   sig, message = createSig(tx, 2004, 3821382321084180)
   print(f"Signature = {sig}")
   print(f"Message = {message}")

   txDict, message = createDictWithSig(tx, 2004, 3821382321084180)
   print(json.dumps(txDict, indent=2))


if __name__ == "__main__":
   main()