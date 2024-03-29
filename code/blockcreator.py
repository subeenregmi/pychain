import hashlib
import json
import time
from address import createAddress
from rawtxcreator import createCoinbaseTx
from transaction import Transaction

class Block():

    """
    Constructor to create a block, the block requires multiple parameters or can be created
    The block height - this is checked with the blockchain, to create order or multiple versions of that chain
    Transactions - these are transactions included within the block, these are required to be verified by each miner,
                   these are now Transaction Objects
    Difficulty - this is usually set by the blockchain, and will be checked to verify if it is a valid block
    Previous Block Hash - this is the previous blocks' id/hash
    """

    def __init__(self, blockchainfile, height=None, transactions=None, difficulty=None, previousblockhash=None):
        # The constructor has no default values, as blocks can be created with a rawTx using createBlockFromRaw(rawtx)

        self.height = height
        self.difficulty = difficulty
        self.previousblockhash = previousblockhash
        self.merkle = ""
        self.nonce = 0
        self.blockid = 0
        self.blocktime = 0
        self.blockmined = False
        self.raw = ""
        self.miner = ""
        self.blockchainfile = blockchainfile
        self.mining = True

        # This just adds the transactions to the block
        if transactions is not None:
            self.transactions = transactions
            list_txids = []

            # Calculating the merkle root
            for transaction in self.transactions:
                list_txids.append(transaction.txid)

            merkle = self.calculateMerkleRoot(list_txids)
            self.merkle = merkle

    def mine(self, publicKey, fee):
        # This is the algorithm to mine a block, which consists of finding a hash of the block with an included nonce
        # value which is lower than the difficulty, thus being a valid block

        # Coinbase Transaction will be added for the reward
        rawCoinbase = createCoinbaseTx(publicKey, 100 + fee, self.height+1)
        CoinbaseTx = Transaction(rawCoinbase)
        self.transactions.append(CoinbaseTx)

        list = []
        for transaction in self.transactions:
            list.append(transaction.txid)
        self.merkle = self.calculateMerkleRoot(list)

        # This calculates the string that needs to be hashed
        timeofmine = int(time.time())
        tobehashed = str(timeofmine) + str(self.height) + self.previousblockhash + str(self.difficulty) + self.merkle
        for transaction in self.transactions:
            TxLength = str(hex(len(transaction.raw))[2:]).zfill(8)
            tobehashed += TxLength
            tobehashed += transaction.raw

        # This appends the miners address at the end of each block
        minerAddress = createAddress(publicKey)
        tobehashed += minerAddress

        while True:
            # We calculate random hashes by incrementing a nonce value, we do this to try and get a hash value which is
            # less than the difficulty.
            if self.mining is False:
                break

            self.nonce += 1
            tobehashed2 = str(self.nonce) + tobehashed
            tobehashed2 = hashlib.sha256(tobehashed2.encode('utf-8')).hexdigest()
            # print(f"Trying Nonce Value = {self.nonce}, hash is {tobehashed2}")

            # If the hash is lower than the difficulty, it calculates the raw and the saves blocks time information
            if int(tobehashed2, 16) < self.difficulty:

                self.blockid = tobehashed2
                self.blocktime = timeofmine
                print(f"Valid Block Found! NONCE = {self.nonce}, blockid is {self.blockid} at {timeofmine}\nBlockHash is {self.blockid}")
                self.blockmined = True
                self.miner = minerAddress
                self.calculateRaw()
                # self.addBlockToChain()
                break

    def validateBlock(self):

        # This checks if a block is valid, after its being mined, by hashing the data again with the nonce provided
        # this should match the block id and be less than the difficulty
        try:
            # This just creates the string we need to hash in the mining algorithm again
            checkid = str(self.nonce) + str(self.blocktime) + str(self.height) + self.previousblockhash + str(self.difficulty) + self.merkle

            for transaction in self.transactions:
                TxLength = str(hex(len(transaction.raw))[2:]).zfill(8)
                checkid += TxLength
                checkid += transaction.raw
            checkid += self.miner

            checkid = hashlib.sha256(checkid.encode('utf-8')).hexdigest()

            if int(checkid, 16) == int(self.blockid, 16):
                self.blockmined = True
                # print("Validated Block")
            else:
                self.blockmined = False
                # print("False!")
        except:
            pass

        return self.blockmined

    def calculateRaw(self):
        # This calculates the raw block after the block has been mined.
        """
        These are the standard form of a block in raw format
        BLOCKID - 64 chars
        NONCE - 16 chars
        BLOCKTIME - 13 chars
        BLOCKHEIGHT - 10 chars
        PREVIOUSBLOCKHASH - 64 chars
        DIFFICULTY - 96 chars
        MERKLE - 96 chars
        SIZETX ~ amount of chars in the blocks transactions - 10 chars
        TRANSACTIONS - Variable chars, each transaction is prepended with a length stored in 8 chars
        MINER ADDRESS - 64 chars
        """

        # To make a raw block, we need to have mined the block 
        if not self.blockmined:
            print("Cannot generate raw of unmined block")
        else:

            nonce = hex(self.nonce)[2:]
            nonce = nonce.zfill(16)

            blocktime = str(self.blocktime).zfill(13)
            blockheight = str(self.height).zfill(10)

            difficultlyOfBlock = hex(self.difficulty)[2:]
            difficultlyOfBlock = str(difficultlyOfBlock).zfill(96)

            transactions = ""
            for transaction in self.transactions:
                TxLength = str(hex(len(transaction.raw))[2:]).zfill(8)
                transactions += TxLength
                transactions += transaction.raw

            sizeTx = hex(len(transactions))[2:]
            sizeTx = sizeTx.zfill(10)

            raw = self.blockid + nonce + blocktime + blockheight + self.previousblockhash + difficultlyOfBlock + self.merkle + sizeTx + transactions + self.miner
            self.raw = raw

            print("----------------------")
            print(f"BLOCK ID: {self.blockid}")
            # print(f"NONCE: {nonce}")
            print(f"BLOCKTIME: {blocktime}")
            print(f"BLOCK HEIGHT: {blockheight}")
            print(f"PREVIOUS BLOCK ID/HASH : {self.previousblockhash}")
            print(f"DIFFICULTY: {difficultlyOfBlock}")
            # print(f"MERKLE ROOT: {self.merkle}")
            # print(f"SIZE OF TXS : {sizeTx}")
            # print(f"TXS : {transactions}")
            # print(f"MINER: {self.miner}")
            print("----------------------")

    def addBlockToChain(self):
        # This function adds the block into the blockchain file. This also checks if the block has been mined and is not
        # already in the blockchain

        file = open(self.blockchainfile, "r")
        for line in file:
            if line == self.raw:
                print("Block already in blockchain")
                file.close()
                return False

        if not self.blockmined:
            print("Cannot add a unmined block.")
            return False

        file = open(self.blockchainfile, "a")
        file.write(self.raw)
        file.write("\n")
        file.close()
        print("Successfully added to the blockchain!")
        return True

    def createBlockFromRaw(self, raw):
        # Grabbing info from the raw block data

        blockid = raw[0:64]
        nonce = raw[64:80]
        blocktime = raw[80:93]
        blockheight = raw[93:103]
        prevblockid = raw[103:167]
        difficulty = raw[167:263]
        merkle = raw[263:327]
        sizeofTXs = int(raw[327:337], 16)
        transactions = raw[337:337+sizeofTXs]
        miner = raw[-66:]

        # Parsing the transactions from raw to a transactions array
        index = 0
        self.transactions = []

        while index <= len(transactions):
            txSize = transactions[0:8]
            txSize = int(txSize, 16)
            index += 8
            tx = transactions[index:index+txSize]
            if tx == '':
                break
            # print(tx)
            txO = Transaction(tx)
            self.transactions.append(txO)
            index += txSize

        # Correlating the current blocks attributes to these variables
        self.blockid = blockid
        self.nonce = int(nonce, 16)
        self.blocktime = int(blocktime)
        self.height = int(blockheight)
        self.previousblockhash = prevblockid
        self.difficulty = int(difficulty, 16)
        self.merkle = merkle
        self.miner = miner
        self.raw = raw
        self.blockmined = True

    def calculateMerkleRoot(self, list):
        # Function to calculate the merkle root
        if len(list) == 0:
            return ""

        if len(list) == 1:
            return list[0]

        newlist = []
        for i in range(0, len(list)-1, 2):
            pair = list[i] + list[i+1]
            pairHash = hashlib.sha256(pair.encode('utf-8')).hexdigest()
            newlist.append(pairHash)

        if len(list) % 2 == 1:
            pair = list[-1] + list[-1]
            pairHash = hashlib.sha256(pair.encode('utf-8')).hexdigest()
            newlist.append(pairHash)

        return self.calculateMerkleRoot(newlist)

def main():

    x = Block('blockchains/testchains.txt')
    print(x.validateBlock())

if __name__ == "__main__":
    main()
