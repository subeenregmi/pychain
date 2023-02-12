from blockcreator import Block
import hashlib
import rawtxdecoder
import scriptsigdecoder
import spubKeydecoder
import address
import rawtxcreator
import rawtxdecoder

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

class Blockchain():
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
                block = Block()
                block.createBlockFromRaw(line)
                block.validateBlock()
                self.blocks.append(block)
                self.height += 1
        except:
            pass

            # print("File not there!")
            # blockchain = open(blockchainfile, "a")

    # This finds a txid in the blocks and returns the raw if found, or it returns false if its not there.

    def findTxid(self, txid):
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.txid == txid: 
                    print(f"Found {transaction.txid}!\nBlock Height: {block.height}\nTransaction Index :{block.transactions.index(transaction)}")
                    print(f"RAW TX: {transaction.raw}")
                    return transaction.raw
        else:
            print("TXID not in blockchain")
            return False

    # This finds a blockid in the blockchain and returns raw if found, or returns false if not there. 

    def findBlockId(self, blockid):
        for block in self.blocks:
            if block.blockid == blockid:
                print(f"Found {block.blockid}!\nBlock Height: {block.height}")
                print(f"RAW BLOCK: {block.raw}")
                return block.raw
        else: 
            print("Block Id not Found!")
            return False        

    # This function searches the blockchain for transactions that are either from the public address or to the public address and will output two lists
    # There are going to be three types of transactions: Inputs, Outputs, and Coinbase
    # Inputs to the address: 
    #   - This will be easy as we can just search the blockchain, by checking the scriptPubKey and decrypting it and seeing if we have a match with our public key
    #   - Then adding this in our input lists
    # Coinbase Transactions: 
    #   - We can check if the scriptSig to this account is equal to the hash of coinbase and the scriptPubKey is the same
    #   - We can also check if the miner of the block is the same pychain address
    #   - Add to inputs List
    # Outputs from the address
    #   - For each transaction find the 'rawtx2' (from 'scriptSigCreator'), then and use the verifySig with the public keys in 'address'
    #   - If each any of the signature matches then add it on the Outputs list
    # Then display in a nice format and returning all inputs and outputs

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
        for input in inputs:
            print(input.txid)

        print(f"---------OUTPUTS----------")
        for output in outputs:
            print(output.txid)
            
            

    def setReward(self, reward):
        self.reward = reward

    
    # This will calculate the average time of the blocks and move the difficulty up or down by using a multiplier.
    # We get the last ten blocks, find the difference between the last block and the most recent block, and then divide by 60
    # We need to get this towards 1 so if we multiply by a multiplier that is 60/average this would be the best way to get to 60 average time 

    def calculateDifficulty(self):
        try:
            secondBlock = self.blocks[-2].blocktime
            currentBlock = self.blocks[-1].blocktime
            difference = currentBlock - secondBlock
            print(f"TIME DIFFERENCE = {difference}")
            difficulty = self.blocks[-1].difficulty
            if difference == 0:
                multiplier = 60
            else:
                multiplier = 60 / difference
            if multiplier > 1.01:
                multiplier = 1.01
            if multiplier < 0.9:
                multiplier = 0.95

            difficulty = difficulty / multiplier
            difficulty = int(difficulty)
            print(f"NEW DIFFICULTY = {difficulty}")
            return difficulty
        except IndexError:
            print("ERROR")
            print(self.blocks)
            return self.blocks[-1].difficulty


    # We need to implement alot of features for a valid chain:
    #   - All blocks need to be in sequential order
    #   - All blocks need to have the correct previous block id
    #   - All blocks need to have a correct id (rehash the details of the block)

    def validateChain(self):

        self.validChain = False

        for i in range(len(self.blocks)):

            if len(self.blocks) == 1: 
                self.validChain = True

            if i != len(self.blocks) - 1:
                # We are iterating through each block by comparing the nth block to the n+1th block, upto the nth block in the list
                
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

        if self.validChain == False:
            print("Chain is invalid")
            return False
        else:
            print("Chain is valid")
            return True

def main():
    test1 = Blockchain("blockchain.txt")
    print(test1.height)
    for block in test1.blocks:
        print(f"blockraw : {block.raw}")
        for transaction in block.transactions:
            print(transaction.raw)
            print(transaction.tx)
            print(transaction.txid)
    print(test1.findTxid("7b6632fce3914fd9b098a10760a995a41dcb260a9a740b7ed6fd0902e2c47ed6"))

    #print(test1.blocks)
    # for block in test1.blocks:
    #     print(block.raw)
    #test1.findTxid("fcef71991fa65b75b67ab8dc7234c8e852b12f0f6f16932e75a592447ffc92c7")
    #
    #test1.findTxidsRelatingToKey((3, 5555))
    #test1.calculateDifficulty()
    #test1.validateChain()
    #print(test1.blocks[-1].transactions[1].txid)
    # test1.findTxid("d26a47abbd0906ea35e6e2570a89c419ad0cdcc0fb64d324f6a1a207f7dc8dd3")
    #test1.findBlockId("0001b328dad9542fada895e80af5e0c59111ee437375bf52de4d170937e291b1")
    #print(test1.blocks[16].transactions[0].raw)
    # print(test1.blocks[-1].transactions[0].inputTxids())
    # print(test1.blocks[-1].transactions[0].txid)
    # print(test1.blocks[-1].transactions[-1].findTotalValueSent())
    # test1.validateChain()

if __name__ == "__main__":
    main()
            