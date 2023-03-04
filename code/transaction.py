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

    x = Transaction("0102c487062affb4596846495422be76a83b893b085f1eb8f0dfd794da9130c8c969000000844023f997df77592f36700060d0ad16dd7a29a86ffb263be5161a117e4f49a3ffc5405def57c7b59782f84893be173ef9ff8cbb8ad2b1e1336947e0e47edac2cb2ee840528c7a2fe647f6ecb0ba9e4351092b3addde070c0e3d6d884997e8cc83296b000000844023f997df77592f36700060d0ad16dd7a29a86ffb263be5161a117e4f49a3ffc5405def57c7b59782f84893be173ef9ff8cbb8ad2b1e1336947e0e47edac2cb2ee80200000000000000b9004c76a942690ddda9dc4549494465421bbd400bb1896a0527390701457e7997e80dc4d2841588ac000000000000000f004c76a9426916ad8380a8adea012e9bcf7590e6f86be12a3ce083978c913da56262f833b09b88ac00000000")

    print(json.dumps(x.tx, indent=2))
    print(x.txid)
    print(x.inputs)
    print(x.outputs)
    print(x.outputAddress())
    print(x.findTotalValueSent())
    print(x.findTotalValueSent("690ddda9dc4549494465421bbd400bb1896a0527390701457e7997e80dc4d28415"))
    print(x.inputTxids())


if __name__ == "__main__":
    main()
