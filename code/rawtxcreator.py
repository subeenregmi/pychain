import hashlib

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
   rawtx1 = hashlib.sha256(rawtx.encode('utf-8')).hexdigest()
   txid = hashlib.sha256(rawtx1.encode('utf-8')).hexdigest()
   return txid

def main():

   print("tx from dict")
   dict = {
   "Version":"01",
   "InputCount":"02",
   "txid0":"ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d60",
   "vout0":"0001",
   "sizeSig0":"0020",
   "scriptSig0":"46b7ebfe9b9639f6f88f77709b453f89ce380ae192202f1fd913864a4c314494",
   "txid1":"8732d097e715d15e8ddd312749a97572bc97b6f8bc1692f08e82f90d0882258e",
   "vout1":"0001",
   "sizeSig1":"0020",
   "scriptSig1":"c2d28ed3a36ca0a8a3076d4c2dfa54c95383deee8ed16b63720f0561a8689465",
   "OutputCount":"01",
   "value0":"00000000000001f4",
   "sizePk0":"0026",
   "scriptPubKey0":"76a92169f38a6b51de7e9345992f2161c9c811a8b57cb2c1f31b8f98211b21af61096bd588ac",
   "locktime":"00000000"   
   }

   rawtx = createTxFromDict(dict)
   print(rawtx)




if __name__ == "__main__":
   main()