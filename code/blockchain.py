from blockcreator import Block
import hashlib
import rawtxdecoder
import scriptsigdecoder
import spubKeydecoder
import address
import rawtxcreator

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
        self.height = 0
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
                self.blocks.append(block)
                self.height += 1
        except:
            blockchain = open(blockchainfile, "a")


    def findTxid(self, txid):
        for block in self.blocks:
            for transaction in block.transactions:
                txidBlock = hashlib.sha256(transaction.raw.encode('utf-8')).hexdigest()
                if txidBlock == txid:
                    print(f"TXID FOUND == {txid}\nTXID IS IN BLOCK {self.blocks.index(block) + 1}, TX NUMBER = {block.transactions.index(transaction) +1}")
                    print(f"TX RAW = {transaction.raw}")
                    return transaction

        print("TXID not found!")
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
        inputs = {}
        outputs = []

        # for block in self.blocks:

        #     for transaction in block.transactions:
        #         transactionID = 
        #         transaction = rawtxdecoder.decodeRawTx(transaction)

        #         # checking for a inputs to the address 
        #         for i in range(int(transaction['OutputCount'])):
        #             input = transaction[f'scriptPubKey{i}']
        #             input = spubKeydecoder.breakDownLockScript(input)
        #             if (pyAddress in input) or (uncompressedAddress in input):
                        

                

        print(f"---------INPUTS----------")
        for input in inputs:
            print(input)
            

    def setReward(self, reward):
        self.reward = reward

    
    # This will calculate the average time of the blocks and move the difficulty up or down by using a multiplier.
    # We get the last ten blocks, find the difference between the last block and the most recent block, and then divide by 60
    # We need to get this towards 1 so if we multiply by a multiplier that is 60/average this would be the best way to get to 60 average time 

    def calculateDifficulty(self):
        totalTime = 0
        twentyBlock = self.blocks[-10].blocktime
        currentBlock = self.blocks[-1].blocktime
        difference = currentBlock - twentyBlock
        difficulty = self.blocks[-1].difficulty
        multiplier = 600 / difference
        difficulty *= multiplier
        difficulty = int(difficulty)
        print(f"NEW DIFFICULTY = {difficulty}")
        return difficulty
                  
    # We need to implement alot of features for a valid chain:
    #   - All blocks need to be in sequential order
    #   - All blocks need to have the the correct previous block id
    #   - All blocks need to have a correct id (rehash the details of the block)

    def validateChain(self):
        for block in self.blocks:
            pass



            


def main():
    test1 = Blockchain("blockchain.txt")
    test1.findTxid("1ac44d7f4e027b1b4c63ddcd2fc155de8ea04bd7658729372aa83ec981bc3e76")
    #test1.findTxidsRelatingToKey((27478882617205022913866810798513923342921168189223, 55112522602840616896238107825541525589537144918969385911224019968193895183400))
    #test1.calculateDifficulty()
    #test1.validateChain()
    print(test1.blocks[-1].transactions[1].txid)
    test1.findTxid("d26a47abbd0906ea35e6e2570a89c419ad0cdcc0fb64d324f6a1a207f7dc8dd3")

if __name__ == "__main__":
    main()
            