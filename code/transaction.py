from rawtxdecoder import *
from rawtxcreator import createTXID
from spubKeydecoder import *

class Transaction:
    '''
    This is the object for transactions, the reason I chose to make it an object rather than to keep it as a dictionary, 
    was to make doing functions on the transactions much easier and for it to be more concise, also keeping everything
    in objects allowed me to design much better.
    '''
    
    def __init__(self, rawtx):

        # To create a transaction, we need to intialise it with the lowest level of a transaction, the raw transactional.py data,
        # we use this rawtx whenever we want to send transactions on the blockchain.

        self.tx = decodeRawTx(rawtx)

        # this decodes our rawTx into a dictionary format to then be parsed into the following parameters

        self.txid = createTXID(rawtx)
        self.version = self.tx["Version"]
        self.inputcount = int(self.tx["InputCount"])
        self.outputcount = int(self.tx["OutputCount"])
        self.inputs = {}
        self.outputs = {}
        self.raw = rawtx
        
        # As a transaction can contain multiple inputs and outputs we need to store the data about both
    
        for x in range(int(self.tx["InputCount"])):
            self.inputs[f"txid{x}"] = {self.tx[f"txid{x}"] : (self.tx[f"vout{x}"], self.tx[f"scriptSig{x}"])}
        
        for x in range(int(self.tx["OutputCount"])):
            self.outputs[self.tx[f"value{x}"]] = self.tx[f"scriptPubKey{x}"]
        
        self.locktime = "00000000"

    # This function goes through the outputs to find the total value being sent

    def findTotalValueSent(self):
        totalValue = 0
        for key in self.outputs:
            totalValue += int(key, 16)
        return totalValue
    
    # This function goes through the outputs to find the addresses that our transaction is being sent to. 

    def outputAddress(self):
        addresses = []
        for key in self.outputs:
            lock_script = self.outputs[key]
            opcodes = breakDownLockScript(lock_script)
            for item in opcodes:
                if item.startswith("69"):
                    addresses.append(item)
        
        return addresses

    def inputTxids(self):
        inputs = []
        for i in range(self.inputcount):
            inputs.append(self.tx[f"txid{i}"])
        return inputs


def main():

    x = Transaction("0101fcef71991fa65b75b67ab8dc7234c8e852b12f0f6f16932e75a592447ffc92c7000100208266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb440100000000000000640021697e66d2a581463fafe887d892fd1d724825bbe214b7b2547639dbc8a87f7cc25d00000000")
    print(x.tx)
    print(x.txid)
    print(x.version)
    print(x.inputcount)
    print(x.outputcount)
    print(x.inputs)
    print(x.outputs)
    print(f"raw = {x.raw}")

if __name__ == "__main__":
    main()
