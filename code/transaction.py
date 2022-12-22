from rawtxdecoder import *
from rawtxcreator import createTXID
from spubKeydecoder import *

class Transaction:
    def __init__(self, rawtx):
        self.__txid = createTXID(rawtx)
        tx = decodeRawTx(rawtx)
        self.__version = tx["Version"]
        self.__inputscount = int(tx["InputCount"])
        self.__outputcount = int(tx["OutputCount"])
        self.__inputs = {}
        self.__outputs={}
        
        for x in range(int(tx["InputCount"])):
            self.__inputs[f"txid{x}"] = {tx[f"txid{x}"] : (tx[f"vout{x}"], tx[f"scriptSig{0}"])}
        
        for x in range(int(tx["OutputCount"])):
            self.__outputs[tx[f"value{x}"]] = tx[f"scriptPubKey{x}"]
        
        self.__locktime = "00000000"

    def getTxid(self):
        return self.__txid

    def getVersion(self):
        return self.__version

    def getInputCount(self):
        return self.__inputscount

    def getInputs(self):
        return self.__inputs

    def getOutputCount(self):
        return self.__outputcount

    def getOutputs(self):
        return self.__outputs

    def getLocktime(self):
        return self.__locktime


    def findTotalValue(self):
        totalValue = 0
        for key in self.__outputs:
            totalValue += int(key, 16)
    
        return totalValue

    
    def outputAddress(self):
        addresses = []
        for key in self.__outputs:
            lock_script = self.__outputs[key]
            opcodes = breakDownLockScript(lock_script)
            for item in opcodes:
                if item.startswith("69"):
                    addresses.append(item)
        
        return addresses



x = Transaction("0102ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d600001002046b7ebfe9b9639f6f88f77709b453f89ce380ae192202f1fd913864a4c3144948732d097e715d15e8ddd312749a97572bc97b6f8bc1692f08e82f90d0882258e00010020c2d28ed3a36ca0a8a3076d4c2dfa54c95383deee8ed16b63720f0561a86894650100000000000001f4002676a92169f38a6b51de7e9345992f2161c9c811a8b57cb2c1f31b8f98211b21af61096bd588ac00000000")

