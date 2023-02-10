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
         size = (len(scriptsig)//2)
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
         size = (len(scriptPubKey)//2)
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
         size = (len(scriptPubKey)//2)
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
      "sizeSig0":"0005",
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
   CoinbaseTemplateDict["sizePk0"] = str(hex(len(scriptPubKey) // 2)[2:]).zfill(4)
   CoinbaseTemplateDict["scriptPubKey0"] = scriptPubKey
   raw = createTxFromDict(CoinbaseTemplateDict)
   return raw
   

def main():
   coinbase = createCoinbaseTx((95440839670107969455973995843666399663662641812074432045896568980475242364517, 67400892360194400039319989411395972789004161889863182881857158544061243615929), 100, 2)
   print(f"Coinbase = {coinbase}")
   tx1 = createTxFromDict({'Version': '01', 'InputCount': '01', 'txid0': '7b6632fce3914fd9b098a10760a995a41dcb260a9a740b7ed6fd0902e2c47ed6', 'vout0': '0001', 'sizeSig0': '0005', 'scriptSig0': '0000000000', 'OutputCount': '01', 'value0': '0000000000000064', 'sizePk0': '0026', 'scriptPubKey0': '76a92169b75cdd59e53f0ced19cbf30efad3ec5ea3026f805d9e1ed6aea18f5a593e29b788ac', 'locktime': '00000000'})
   print(f"Tx1 = {tx1}")



if __name__ == "__main__":
   main()