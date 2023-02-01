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

        # To create a transaction, we need to intialise it with the lowest level of a transaction, the raw transactional data,
        # we use this rawtx whenever we want to send transactions on the blockchain.

        tx = decodeRawTx(rawtx)

        # this decodes our rawTx into a dictionary format to then be parsed into the following parameters

        self.txid = createTXID(rawtx)
        self.version = tx["Version"]
        self.inputscount = int(tx["InputCount"])
        self.outputcount = int(tx["OutputCount"])
        self.inputs = {}
        self.outputs = {}
        self.raw = rawtx
        
        # As a transaction can contain multiple inputs and outputs we need to store the data about both
    
        for x in range(int(tx["InputCount"])):
            self.inputs[f"txid{x}"] = {tx[f"txid{x}"] : (tx[f"vout{x}"], tx[f"scriptSig{x}"])}
        
        for x in range(int(tx["OutputCount"])):
            self.outputs[tx[f"value{x}"]] = tx[f"scriptPubKey{x}"]
        
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

def main():

    x = Transaction("0102ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d600001002046b7ebfe9b9639f6f88f77709b453f89ce380ae192202f1fd913864a4c3144948732d097e715d15e8ddd312749a97572bc97b6f8bc1692f08e82f90d0882258e00010020c2d28ed3a36ca0a8a3076d4c2dfa54c95383deee8ed16b63720f0561a86894650100000000000001f400201b7990b9fd11da0d24a0f539e3ed3407285538737785acc6b7dcb602b0a6849200000000")
    print(x.inputs)

if __name__ == "__main__":
    main()
