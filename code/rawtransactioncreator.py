"""

   01    01 fc9e4f9c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a56779 0001 006a {scriptsig} 01 000000000021af4b 0019 76a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac 00000000
Version  IC                         TXID of input                            VOUT size  scriptsig  OC     Value        size                     ScriptPubKey                   Locktime

"""


from ast import Raise


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
         txid = str(input(f"Txid{i}"))
         vout = 
         rawtx += txid
         scriptsig = str(input(f"Script Sig : "))
         size = hex(len(scriptsig)//2)
         rawtx += size + scriptsig


   else:
      print("Only Version 1 transactions are supported")

   return rawtx



rawtxs = createTxFromUser()
print(rawtxs)
