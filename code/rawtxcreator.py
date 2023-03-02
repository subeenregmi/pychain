import hashlib
from spubKeycreator import createPayToPubKeyHash

def createTxFromUser():

   rawtx = ""
   version = int(input("Version : "))
   
   if version == 1:
      rawtx += "{0:02x}".format(version)
      inputcounter = int(input("Inputs : "))
      if inputcounter > 99:
         print("Inputs have to be in the range (0 - 99)")
         createTxFromUser()
      rawtx += "{0:02d}".format(inputcounter)
      for i in range(inputcounter):
         txid = str(input(f"Txid{i}: "))
         rawtx += txid
         vout = int(input(f"VOUT{i}: "))
         rawtx += "{0:04x}".format(vout)
         scriptsig = str(input(f"Script Sig{i} : "))
         size = (len(scriptsig))
         rawtx += "{0:04x}".format(size) + scriptsig
      outputcounter = int(input("Outputs : "))
      if inputcounter > 99:
         print("Outputs have to be in the range (0 - 99)")
         createTxFromUser()
      rawtx += "{0:02d}".format(outputcounter)
      for z in range(outputcounter):
         value = int(input(f"Value{z}: "))
         rawtx += "{0:016x}".format(value)
         scriptPubKey = str(input(f"ScriptPubKey{z}: "))
         size = (len(scriptPubKey))
         rawtx += "{0:04x}".format(size) + scriptPubKey

   else:
      print("Only Version 1 transactions are supported")

   rawtx += "00000000"
   return rawtx

def EmptyRawTxFromUser():
   
   rawtx = ""
   version = int(input("Version : "))
   
   if version == 1:
      rawtx += "{0:02x}".format(version)
      inputcounter = int(input("Inputs : "))
      if inputcounter > 99:
         print("Inputs have to be in the range (0 - 99)")
         createTxFromUser()
      rawtx += "{0:02d}".format(inputcounter)
      for i in range(inputcounter):
         txid = str(input(f"Txid{i}: "))
         rawtx += txid
         vout = 0
         rawtx += "{0:04x}".format(vout)
         scriptsig = ""
         size = 0
         rawtx += "{0:04x}".format(size) + scriptsig
      outputcounter = int(input("Outputs : "))
      if inputcounter > 99:
         print("Outputs have to be in the range (0 - 99)")
         createTxFromUser()
      rawtx += "{0:02d}".format(outputcounter)
      for z in range(outputcounter):
         value = int(input(f"Value{z}: "))
         rawtx += "{0:016x}".format(value)
         scriptPubKey = str(input(f"ScriptPubKey{z}: "))
         size = (len(scriptPubKey))
         rawtx += "{0:04x}".format(size) + scriptPubKey

   else:
      print("Only Version 1 transactions are supported")

   rawtx += "00000000"
   return rawtx

def createTxFromDict(tx2):
   rawtx = ""
   for item in tx2.items():
      rawtx += item[1]

   return rawtx

def createTXID(rawtx):
   txid = hashlib.sha256(rawtx.encode('utf-8')).hexdigest()
   txid = hashlib.sha256(txid.encode('utf-8')).hexdigest()
   
   return txid

def createCoinbaseTx(publicKey, reward, blockheight):
   # The coinbase transaction is the reward the u
   CoinbaseTemplateDict = {
      "Version":"01",
      "InputCount":"01",
      "txid0":"8266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb44", #hash of 'COINBASE'
      "vout0":"0001",
      "sizeSig0":"000a",
      "scriptSig0":"0000000000",
      "OutputCount":"01",
      "value0":"",
      "sizePk0":"",
      "scriptPubKey0":"",
      "locktime":"00000000"   
   }

   scriptPubKey = createPayToPubKeyHash(publicKey)
   value = str(hex(reward)[2:]).zfill(16)
   CoinbaseTemplateDict["scriptSig0"] = str(blockheight).zfill(10)
   CoinbaseTemplateDict["value0"] = value
   CoinbaseTemplateDict["sizePk0"] = str(hex(len(scriptPubKey))[2:]).zfill(4)
   CoinbaseTemplateDict["scriptPubKey0"] = scriptPubKey
   raw = createTxFromDict(CoinbaseTemplateDict)
   return raw
   

def main():

   tx1 = createTxFromDict({'Version': '01', 'InputCount': '03', 'txid0': 'c6aa507dfcb1995d6203e094d46f2c6eea2579e7bd153b7b6329fbbbc9c9af1e', 'sizeSig0': '0042', 'scriptSig0': '409cef4aab73080ec94b85921fab7655eb14ef20b9be99efdd1c394d4a4dff8481401e09d666ab546f15e1d0345e35c4e3d074b6e9c4bd6d9d0dccd7d09f308bffba', 'txid1': 'bca065da3279ff78f360f3d0ae70b22fe4bd34b60510bda5b7d4cc6d17970fcb', 'sizeSig1': '0042', 'scriptSig1': '409cef4aab73080ec94b85921fab7655eb14ef20b9be99efdd1c394d4a4dff8481401e09d666ab546f15e1d0345e35c4e3d074b6e9c4bd6d9d0dccd7d09f308bffba', 'txid2': 'ddfb7d53b1d69f534f26ddbb46e0f6cb07cd30a838779c0bc434fee19e33620d', 'sizeSig2': '0042', 'scriptSig2': '409cef4aab73080ec94b85921fab7655eb14ef20b9be99efdd1c394d4a4dff8481401e09d666ab546f15e1d0345e35c4e3d074b6e9c4bd6d9d0dccd7d09f308bffba', 'OutputCount': '03', 'value0': '00000000000000ea', 'sizePk0': '0026', 'scriptPubKey0': '76a92169b75cdd59e53f0ced19cbf30efad3ec5ea3026f805d9e1ed6aea18f5a593e29b788ac', 'value1': '0000000000000042', 'sizePk1': '0026', 'scriptPubKey1': '76a92169d0d6247e713098d507bab69a14fe2ae731a1542f881a6cd27e8518dbf18a730688ac', 'vout0': '0000', 'vout1': '0000', 'vout2': '0000'})
   print(f"Tx1 = {tx1}")



if __name__ == "__main__":
   main()