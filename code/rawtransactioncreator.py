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

   #rawtxs = createTxFromUser()
   #print(rawtxs)

   prevtx = {'Version': '01', 'InputCount': '01', 'txid0': 'fc9e4f9c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a56779', 'vout0': '0000', 'sizeSig0': '0000', 'scriptSig0': '', 'OutputCount': '01', 'value0': '000000000021af4b', 'sizePk0': '0019', 'scriptPubKey0': '76a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac', 'locktime': '00000000'}
   rawtx = createTxFromDict(prevtx)
   print(rawtx)

   rawemptytx = EmptyRawTxFromUser()
   print(rawemptytx)

   rawtx_dict = createTxFromDict({'Version': '01', 'InputCount': '01', 'txid0': 'fc00000c334d55c1dc53...5e18a56779', 'vout0': '0000', 'sizeSig0': '0019', 'scriptSig0': '76a914db4d1141d0048b...368b0e88ac', 'OutputCount': '01', 'value0': '00000000002dc6c0', 'sizePk0': '0019', 'scriptPubKey0': '76a914db4d1141d0048b...368b0e88ac', 'locktime': '00000000'})
   print(rawtx_dict)
   
if __name__ == "__main__":
   main()