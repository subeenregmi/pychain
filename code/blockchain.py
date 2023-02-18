from blockcreator import Block
import address


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
        uncompressedAddress = "04 " + str(hex(publicKey[0])[2:]) + str(hex(publicKey[1]))[2:]
        inputs = []
        outputs = []

        for block in self.blocks:
            for transaction in block.transactions:
                try:
                    if pyAddress in transaction.outputAddress():
                        inputs.append(transaction)
                except:
                    pass

                for input in inputs:
                    if input.txid in transaction.inputTxids():
                        if input not in outputs:
                            outputs.append(transaction)

        uniqueOutputs = []
        for output in outputs:
            if output not in uniqueOutputs:
                uniqueOutputs.append(output)

        outputs = uniqueOutputs

        print(f"---------INPUTS----------")
        for txidinput in inputs:
            print(txidinput.txid)

        print(f"---------OUTPUTS----------")
        for output in outputs:
            print(output.txid)

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
            return 135607040845515931344379931619614108352879381342049336509327220462845952

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
    for block in test.blocks:
        for transaction in block.transactions:
            print(transaction.txid)
            print(transaction.tx)

    print(test.findTxid("9d62dc5dda5e01d7f9aa919e2f2b9c9e424b7cf1f8092d2fb6138223e6356cc3"))
    print(test.findTxidsRelatingToKey((63954422509139660694275478881573291931659433822585593108077818434106113196321, 26900081337699559997929288916999997486541154242084777368521628620275013037611)))
    print(test.findBlockId("0000015cae0a93eb716a443497386b36c1e9675627288a811191157b6aa04e97"))
    test.calculateDifficulty()
    test.validateChain()

if __name__ == "__main__":
    main()
