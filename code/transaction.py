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

    def findTotalValueSent(self, address=None):
        totalValue = 0
        for key in self.outputs:
            if address is not None:
                spk = key[1]
                spk = breakDownLockScript(spk)
                if address in spk:
                    continue
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

    x = Transaction("01017b6632fce3914fd9b098a10760a995a41dcb260a9a740b7ed6fd0902e2c47ed600000042408b22520c20af4de60e54aa2af78486e661efbffc38286253a54bcf24ab2b79934020d79daebf01adb60a15f87eec4c2f41bf5804eab89a8aa995b6224f15f5782c010000000000000064002676a92169b75cdd59e53f0ced19cbf30efad3ec5ea3026f805d9e1ed6aea18f5a593e29b788ac00000000")
    print(x.tx)
    print(x.txid)
    print(x.version)
    print(x.inputcount)
    print(x.outputcount)
    print(x.inputs)
    print(x.outputs)
    print(f"raw = {x.raw}")
    print(x.inputTxids())

if __name__ == "__main__":
    main()
