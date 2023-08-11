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

   tx1 = createTxFromDict({'Version': '01', 'InputCount': '02', 'txid0': 'c487062affb4596846495422be76a83b893b085f1eb8f0dfd794da9130c8c969', 'vout0': '0000', 'sizeSig0': '0084', 'scriptSig0': '4023f997df77592f36700060d0ad16dd7a29a86ffb263be5161a117e4f49a3ffc5405def57c7b59782f84893be173ef9ff8cbb8ad2b1e1336947e0e47edac2cb2ee8', 'txid1': '40528c7a2fe647f6ecb0ba9e4351092b3addde070c0e3d6d884997e8cc83296b', 'vout1': '0000', 'sizeSig1': '0084', 'scriptSig1': '4023f997df77592f36700060d0ad16dd7a29a86ffb263be5161a117e4f49a3ffc5405def57c7b59782f84893be173ef9ff8cbb8ad2b1e1336947e0e47edac2cb2ee8', 'OutputCount': '02', 'value0': '00000000000000b9', 'sizePk0': '004c', 'scriptPubKey0': '76a942690ddda9dc4549494465421bbd400bb1896a0527390701457e7997e80dc4d2841588ac', 'value1': '000000000000000f', 'sizePk1': '004c', 'scriptPubKey1': '76a9426916ad8380a8adea012e9bcf7590e6f86be12a3ce083978c913da56262f833b09b88ac', 'locktime': '00000000'})
   print(f"Transaction from dictionary = {tx1}")

   txid = createTXID(tx1)
   print(f"TXID = {txid}")

   public_key = (55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)
   coinbaseTransaction = createCoinbaseTx(public_key, 100, 3)
   print(f"Coinbase Transaction = {coinbaseTransaction}")




if __name__ == "__main__":
   main()