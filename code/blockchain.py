from blockcreator import Block
import address
import rawtxdecoder
import spubKeydecoder
from transaction import Transaction

'''
This will be the blockchain class that will regulate the rewards for the blocks, blockheight and difficulty,
This will also parse the blockchain into blocks, for easy searching of transactions, this will also act as the distribution of the blockchain files. 

Properties in a blockchain
    - Reward Mechanism
    - Difficulty Mechanism
    - Dictionary of TXIDs for specific address
    - TXID Search
    - Blockchain parsing into Blocks 
'''

class Blockchain:
    def __init__(self, blockchainfile):

        '''
            Here are some parameters:-
            Blocks - is the list of blocks currently in the blockchain file
            The height of blocks, the number of blocks in the blockchain file
            validChain - The validity of the chain, this is used to contribute a new block to the chain 
            Difficulty - this parameter is calculated based on the time it took to mine each block
            Reward - this is based on the current supply of tokens, or is a fixed amount
        '''

        self.blocks = []
        self.height = -1
        self.validChain = False
        self.difficulty = None
        self.reward = None
        self.averageBlockTime = 60

        try:
            blockchain = open(blockchainfile, "r")
            for line in blockchain.readlines():
                line = line[:-1]
                block = Block(blockchainfile)
                block.createBlockFromRaw(line)
                block.validateBlock()
                self.blocks.append(block)
                self.height += 1
        except:
            pass

    def findBlockIdwithTxid(self, txid):

            for block in self.blocks:
                for transaction in block.transactions:
                    if transaction.txid == txid:
                        print(f"Found {transaction.txid}!\nBlock Height: {block.height}\nTransaction Index :{block.transactions.index( transaction )}" )
                        print(f"RAW TX: {transaction.raw}")
                        return transaction, block

            print("TXID not in blockchain")
            return False

    def findTxid(self, txid):

        # This finds a txid in the blocks and returns the raw if found, or it returns false if it's not there.
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.txid == txid:
                    print(f"Found {transaction.txid}!\nBlock Height: {block.height}\nTransaction Index :{block.transactions.index(transaction)}")
                    print(f"RAW TX: {transaction.raw}")
                    return transaction.raw

        print("TXID not in blockchain")
        return False

    def findBlockId(self, blockid):

        # This finds a block id in the blockchain and returns raw if found, or returns false if not there.
        for block in self.blocks:
            if block.blockid == blockid:
                print(f"Found {block.blockid}!\nBlock Height: {block.height}")
                print(f"RAW BLOCK: {block.raw}")
                return block.raw

        print("Block Id not Found!")
        return False

    def findTxidsRelatingToKey(self, publicKey):

        pyAddress = address.createAddress(publicKey)
        inputs = []
        outputs = []

        for block in self.blocks:
            for transaction in block.transactions:
                if pyAddress in transaction.outputAddress():
                    inputs.append(transaction)

        for block in self.blocks:
            for transaction in block.transactions:
                for input in inputs:
                    if input.txid in transaction.inputTxids():
                        outputs.append(transaction)

        uniqueOutputs = []
        for output in outputs:
            if output not in uniqueOutputs:
                uniqueOutputs.append(output)

        outputs = uniqueOutputs

        for output in outputs:
            for outputInputTxid in output.inputTxids():
                for input in inputs:
                    if input.txid == outputInputTxid:
                        inputs.remove(input)

        return inputs, outputs

    def findALLTxidsRelatingToKey(self, publicKey):

        pyAddress = address.createAddress(publicKey)
        transactions = []

        for block in self.blocks:
            for transaction in block.transactions:
                try:
                    for item in transaction.outputAddress():
                        if item == pyAddress:
                            transactions.append(transaction)
                except:
                    pass

                for input in transactions:
                    for i in transaction.inputTxids():
                        if i in transactions:
                            continue
                        if i == input.txid:
                            transactions.append(transaction)

        uniquetransactions = []
        for transaction in transactions:
            if transaction not in uniquetransactions:
                uniquetransactions.append(transaction)

        transactions = uniquetransactions

        return transactions

    def findWhoSentTransaction(self, tx):
        # This will look at the transactions inputs and try to find them in the blockchain if found we can return the
        # address of script public key
        decodedTx = rawtxdecoder.decodeRawTx(tx.raw)
        for i in range(tx.inputcount):
            txidSearch = decodedTx[f'txid{i}']
            txidVout = decodedTx[f'vout{i}']

            # Check if a transaction is a coinbase
            if txidSearch == "8266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb44":
                return "Coinbase Transaction"

            # Break down the scriptPubKey of the input tx, to find the address.
            searchedTxRaw = self.findTxid(txidSearch)
            if searchedTxRaw:
                searchedTxDict = rawtxdecoder.decodeRawTx(searchedTxRaw)
                scriptPubKey = searchedTxDict[f"scriptPubKey{int(txidVout, 16)}"]
                opcodes = spubKeydecoder.breakDownLockScript(scriptPubKey)
                for opcode in list(opcodes.queue):
                    if opcode[:2] == "69":
                        return opcode

    def setReward(self, reward):
        self.reward = reward

    def calculateDifficulty(self):
        # This gets the second last and last block mined, and compares the time difference, if the block time is above
        # the average block time then we increase the target by 5% as this makes mining the blocks much easier, if the
        # time difference is below the average block time we decrease the target by 1% to make the blocks mining harder

        try:
            secondBlock = self.blocks[-2].blocktime
            currentBlock = self.blocks[-1].blocktime
            difference = currentBlock - secondBlock
            difficulty = self.blocks[-1].difficulty
            if difference == 0:
                multiplier = 1.05
            else:
                multiplier = self.averageBlockTime / difference
                if multiplier > 1.01:
                    multiplier = 1.01

                if multiplier < 0.9:
                    multiplier = 0.95

            difficulty = difficulty / multiplier
            difficulty = int(difficulty)

            print(f"NEW DIFFICULTY = {difficulty}")
            return difficulty

        except IndexError:
            # This is the default difficulty to roughly mine a block every 60 seconds.
            return 1356070408455159313443799316196141083528793813420493365093272204628459527

    def validateChain(self):
        # We need to implement alot of features for a valid chain:
        #   - All blocks need to be in sequential order
        #   - All blocks need to have the correct previous block id
        #   - All blocks need to have a correct id (rehash the details of the block)

        self.validChain = False
        for i in range(len(self.blocks)):
            if len(self.blocks) == 1:
                self.validChain = True

            # We compare every block with the next one.
            if i != len(self.blocks) - 1:
                block1 = self.blocks[i]
                block2 = self.blocks[i+1]

                # This checks if the blocks are in sequential order
                if block1.height < block2.height:
                    self.validChain = True
                else:
                    self.validChain = False
                    print("Blocks Are Not Ordered Sequentially.")
                    break

                # This checks the blocks previous hash is the hash of the previous block 
                if block2.previousblockhash == block1.blockid:
                    self.validChain = True
                else:
                    self.validChain = False
                    print("Block(s) Previous Hash's are not the same.")
                    break

                # This validates the block to make sure the blockid is the correct 
                if (block1.validateBlock()) and (block2.validateBlock()):
                    self.validChain = True
                else:
                    self.validChain = False
                    print("Blocks have wrong block id.")
                    break

        if not self.validChain:
            print("Chain is invalid")
            return False

        else:
            print("Chain is valid")
            return True

def main():
    test = Blockchain("blockchains/pychain.txt")
    public_key = (103106455141897256590050535433311244247821437712848739395258315148311206142216, 35272270782237393198583873716500957634512402507620183512278104868856770902733)

    # Finding a txid
    inputs, outputs = test.findTxidsRelatingToKey(public_key)
    print(inputs)
    print(outputs)

    print("Inputs")
    for input in inputs:
        print(input.txid)
        print(input.tx)

    print("outputs")
    for output in outputs:
        print(output.tx)
        print(output.txid)

    test.validateChain()






if __name__ == "__main__":
    main()
