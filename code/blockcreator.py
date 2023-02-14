import hashlib
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

        # This just adds the transactions to the block
        if transactions is not None:
            self.transactions = transactions
            for transaction in self.transactions:
                self.merkle += transaction.raw

        # The merkle root/hash is the raw transactional.py data hashed together, this creates a unique hash for those
        # specific transactions
        self.merkle = hashlib.sha256(self.merkle.encode('utf-8')).hexdigest()

    def mine(self, publicKey, fee):
        # This is the algorithm to mine a block, which consists of finding a hash of the block with an included nonce
        # value which is lower than the difficulty, thus being a valid block

        # Coinbase Transaction will be added for the reward
        rawCoinbase = createCoinbaseTx(publicKey, 100 + fee, self.height+1)
        CoinbaseTx = Transaction(rawCoinbase)
        self.transactions.append(CoinbaseTx)

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
                self.addBlockToChain()
                break

    def validateBlock(self):

        # This checks if a block is valid, after its being mined, by hashing the data again with the nonce provided
        # this should match the block id and be less than the difficulty

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
        if self.blockmined == False:
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
        # This function adds the block into the blockchain file.

        if not self.blockmined:
            print("Cannot add a unmined block.")

        else:
            file = open(self.blockchainfile, "a")
            file.write(self.raw)
            file.write("\n")
            file.close()
            print("Successfully added to the blockchain!")

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

def main():

    #x = Block(1, [Transaction("01017898db070c4bcc871a55da6c53486421c97d2ec9c6b37d0f36a06ac857c36a50000100050000000001010000000000000064002676a921692a3463a826237019f2e3b8106e955c92ff7dbdaaa34288ae2a6697ee24c3714d88ac00000000")], 11056817284059613142410972512193377984481879657863353468882227275223423263, "1b7990b9fd11da0d24a0f539e3ed3407285538737785acc6b7dcb602b0a68492")
    # x = Block("blockchain.txt", 0, [], 1105681727986405912613142410975121469398887965786353467233272752666322463, "1b7990b9fd11da0d24a0f539e3ed3407285538737785acc6b7dcb602b0a68492")
    # x.mine((92641855401206585750031304985966472123204240504167073082041014802408154789641, 5320727137213493453320294950656953718594582159943012446202168292331376026727), 0)
    # x.validateBlock()
    # print(x.raw)
    # print(x.transactions)
    # for transaction in x.transactions:
    #     print(f"TX = {transaction.raw}")
    #
    v = Block("testchain.txt")
    v.createBlockFromRaw("000000300301e0469e198a83575b1b1a41ad795e4edcd652d6c420ced9e472b4000000000057ef73000167633094300000000007cb95d760cbecec3e8f537d55a307ba8e5598ecce09ece40fcffc50ca702873500000000000000000000000000000000000000324ca88ef79937cee42eb7bdfe51e3bcca471e9cd3553333334c076c00e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b85500000000c8000000c001018266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb44000100050000000001010000000000000064002676a92169a45fd1b1733c7967f1452dcdd77cb488f55977af24229ef49ccce62e780d285388ac0000000069a45fd1b1733c7967f1452dcdd77cb488f55977af24229ef49ccce62e780d2853")
    print(v.validateBlock())
    # print(v.transactions[0].inputs)
    # v.validateBlock()

    #
    #
    # v = Block()

    # print(x.blocktime)
    # for tx in x.transactions:
    #     print(f"Txs: {tx.findTotalValueSent()}")

    # v = Block()
    # v.createBlockFromRaw(x.raw)


    # print(v.blocktime)

    # if v.blocktime == x.blocktime:
    #     print("s23232")

    # if v.nonce == x.nonce:
    #     print("Success")

    # print(v.height)



if __name__ == "__main__":
    main()




