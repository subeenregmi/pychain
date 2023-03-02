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
        if address is None:
            for key in self.outputs:
                totalValue += int(key, 16)
            return totalValue
        else:
            index = 0
            for key in self.outputs:
                spk = breakDownLockScript(list(self.outputs.values())[index])
                if address in list(spk.queue):
                    pass
                else:
                    totalValue += int(key, 16)
                index += 1
            return totalValue

    
    # This function goes through the outputs to find the addresses that our transaction is being sent to. 

    def outputAddress(self):
        addresses = []
        for key in self.outputs:
            lock_script = self.outputs[key]
            opcodes = breakDownLockScript(lock_script)
            for item in list(opcodes.queue):
                if item.startswith("69"):
                    addresses.append(item)
        
        return addresses

    def inputTxids(self):
        inputs = []
        for i in range(self.inputcount):
            inputs.append(self.tx[f"txid{i}"])
        return inputs


def main():

    x = Transaction("010220ed724671484174625415ab8ff408aaffe42bd8c8f08c0c4a525bfcb329881800000084405d98466f9073a0c63b2ce212c0bc6d170af18f9b79421d3d3a87902b76042777404bb1bf8dd89d719e279ac7185decd226aa8115884527f84b61a26d08c10bce05e32ca14d53bec6f6471307bc01d670bc6dc51104ff01a92dbb4ef3c3117f4a8200000084405d98466f9073a0c63b2ce212c0bc6d170af18f9b79421d3d3a87902b76042777404bb1bf8dd89d719e279ac7185decd226aa8115884527f84b61a26d08c10bce050200000000000000bb004b76a94169bfe8b0512755539097b01056836c042751803ff2b24c830444de0233fe1b56988ac000000000000000d004c76a94269d0d6247e713098d507bab69a14fe2ae731a1542f881a6cd27e8518dbf18a730688ac00000000")
    print(x.findTotalValueSent())
    print(x.outputAddress())

if __name__ == "__main__":
    main()
