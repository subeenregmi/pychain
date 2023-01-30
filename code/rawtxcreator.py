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
   return txid

def createCoinbaseTx(publicKey, reward):
   # The coinbase transaction is the reward the u
   CoinbaseTemplateDict = {
      "Version":"01",
      "InputCount":"01",
      "txid0":"8266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb44", #hash of 'COINBASE'
      "vout0":"0001",
      "sizeSig0":"000A",
      "scriptSig0":"0000000000",
      "OutputCount":"01",
      "value0":"",
      "sizePk0":"",
      "scriptPubKey0":"",
      "locktime":"00000000"   
   }

   scriptPubKey = createPayToPubKeyHash(publicKey)
   value = str(hex(reward)[2:]).zfill(16)
   CoinbaseTemplateDict["value0"] = value
   

   pass

def main():

   # print("tx from dict")
   # dict = {
   # "Version":"01",
   # "InputCount":"01",
   # "txid0":"ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d60",
   # "vout0":"0001",
   # "sizeSig0":"0020",
   # "scriptSig0":"46b7ebfe9b9639f6f88f77709b453f89ce380ae192202f1fd913864a4c314494",
   # "OutputCount":"01",
   # "value0":"00000000000001f4",
   # "sizePk0":"0026",
   # "scriptPubKey0":"76a92169f38a6b51de7e9345992f2161c9c811a8b57cb2c1f31b8f98211b21af61096bd588ac",
   # "locktime":"00000000"   
   # }

   # rawtx = createTxFromDict(dict)
   # print(rawtx)
   createCoinbaseTx("dasd", 100)




if __name__ == "__main__":
   main()