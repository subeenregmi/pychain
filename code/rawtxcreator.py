
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

def main():
   pass
 
if __name__ == "__main__":
   main()