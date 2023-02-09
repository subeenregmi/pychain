# This file will contain all the following, blockchain, blocks, transactions all in one and addresses, other small
# scripts will be imported.

import hashlib
import time
from rawtxdecoder import decodeRawTx
from rawtxcreator import createTXID, createCoinbaseTx
from spubKeydecoder import breakDownLockScript

Pcurve = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

################################################# ADDRESS CREATION ####################################################
def ECadd(x1, x2, y1, y2):
    # This function adds two co-ordinate points using elliptic-curve-addition and returns the sum.

    lam = ((y2 - y1) * pow((x2 - x1), -1, Pcurve)) % Pcurve
    x3 = (lam * lam - x1 - x2) % Pcurve
    y3 = (lam * (x1 - x3) - y1) % Pcurve

    return x3, y3


def ECdouble(x1, y1):
    # This functions doubles the co-ordinate point using elliptic-curve-arithmetic, and returns the product.

    lamD = ((3 * (x1 * x1) + 0) * pow((2 * y1), -1, Pcurve)) % Pcurve
    x3 = ((lamD * lamD) - (2 * x1)) % Pcurve
    y3 = (lamD * (x1 - x3) - y1) % Pcurve

    return x3, y3


def ECmultiplication(Scalar, GenX, GenY):
    # This function allows us to do elliptic-curve-multiplication using a scalar, it does this by converting our scalar
    # to binary and then where ever there is a 1, we do ECdouble and where ever there is a zero, we do ECaddition, by
    # repeating this process we get to a cryptographically secure co-ordinate which will serve as our public key.

    # We need to check that our scalar does not exceed the n constant, if it does it would produce keys, that are
    # unsecure.
    if Scalar == 0 or Scalar >= n:
        raise Exception("Invalid")

    scalar_binary = str(bin(Scalar))[2:]
    CurX, CurY = GenX, GenY

    for i in range(1, len(scalar_binary)):
        CurX, CurY = ECdouble(CurX, CurY)
        if scalar_binary[i] == "1":
            CurX, CurY = ECadd(CurX, GenX, CurY, GenY)

    return CurX, CurY


def signatureGeneration(privateKey, randomNumber, hashedMessage):
    # This function generates a digital signature created by the private key, and can be verified with the public key.

    x, y = ECmultiplication( randomNumber, Gx, Gy )
    r = x % n
    s = (pow(randomNumber, -1, n) * (hashedMessage + r * privateKey)) % n

    return r, s


def verifySig(r1, s1, hashedMessage, publicKey):
    # This function uses a digital signature, the data used in the signature, and a public key to verify that the public
    # key owns this signature.

    if (r1 <= 0) or (s1 <= 0) or (r1 >= n) or (s1 >= n):
        raise Exception("Invalid")

    u1 = hashedMessage * pow(s1, -1, n)
    u2 = r1 * pow(s1, -1, n)

    xu1, yu1 = ECmultiplication(u1 % n, Gx, Gy)
    xu2, yu2 = ECmultiplication(u2 % n, publicKey[0], publicKey[1])

    x, y = ECadd(xu1, xu2, yu1, yu2)

    if r1 == x % n:
        return True
    else:
        return False


def createAddress(publickey):
    # This function creates a pychain address by hashing the public key effectively creating a unique address.

    pubkeyStr = str(publickey[0]) + str(publickey[1])
    hash1 = hashlib.sha256(pubkeyStr.encode('utf-8')).hexdigest()
    hash2 = hashlib.sha256(hash1.encode('utf-8')).hexdigest()
    address = "69" + str(hash2)

    return address

#------------------------------------- TRANSACTIONS -----------------------------------------------------------------

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
            self.inputs[f"txid{x}"] = {self.tx[f"txid{x}"]: (self.tx[f"vout{x}"], self.tx[f"scriptSig{x}"])}

        for x in range(int(self.tx["OutputCount"])):
            self.outputs[self.tx[f"value{x}"]] = self.tx[f"scriptPubKey{x}"]

        self.locktime = "00000000"

    def findTotalValueSent(self):
        # This functions iterate through all the outputs to determine the value of that transaction.

        totalValue = 0
        for key in self.outputs:
            totalValue += int( key, 16 )
        return totalValue

    def outputAddress(self):
        # This function goes through the outputs to find the addresses that our transaction is being sent to.

        addresses = []
        for key in self.outputs:
            lock_script = self.outputs[key]
            opcodes = breakDownLockScript( lock_script )
            for item in opcodes:
                if item.startswith("69"):
                    addresses.append(item)

        return addresses

    def inputTxids(self):
        # This function outputs all the txids, the transaction refers to.

        inputs = []
        for i in range(self.inputcount):
            inputs.append(self.tx[f"txid{i}"])
        return inputs

    def validateTransaction(self):
        # This function will validate the transaction by searching the TXIDS, and checking if they are present and
        # exceeding the values sent. And if the scriptSig matches the input.
        pass


#-------------------------------------  BLOCKS -----------------------------------------------------------------

class Block:

    def __init__(self, height=None, transactions=None, difficulty=None, previousblockhash=None):
        '''
            Constructor to create a block, the block requires multiple parameters or can be created
            The block height - this is checked with the blockchain, to create order or multiple versions of that chain
            Transactions - these are transactions included in the block, these are required to be verified by each miner
            Difficulty - this is usually set by the blockchain, and will be checked to verify if it is a valid block
            Previous Block Hash - this is the previous blocks' id/hash
        '''

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
        self.blockchainfile = "blockchain.txt"

        # This just adds the transactions to the block
        if transactions is not None:
            self.transactions = transactions
            for transaction in self.transactions:
                self.merkle += transaction.raw

        # The merkle root/hash is the raw transactional.py data hashed together, this creates a unique hash for those
        # transactions

        self.merkle = hashlib.sha256(self.merkle.encode('utf-8')).hexdigest()

    def mine(self, publicKey):
        # This is the algorithm to mine a block, which consists of finding a hash of the block with an included nonce
        # value which is lower than the difficulty, thus being a valid block

        # Coinbase Transaction will be added for the reward
        rawCoinbase = createCoinbaseTx(publicKey, 100, self.height)
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
            # This checks if the hash of the block turns out to be less than difficulty

            # We calculate random hashes by incrementing a nonce value
            self.nonce += 1
            tobehashed2 = str(self.nonce) + tobehashed
            tobehashed2 = hashlib.sha256(tobehashed2.encode('utf-8')).hexdigest()
            print( f"Trying Nonce Value = {self.nonce}, hash is {tobehashed2}")

            # If the hash is lower than the difficulty, it calculates the raw and the blocktime information
            if int( tobehashed2, 16 ) < self.difficulty:
                self.blockid = tobehashed2
                self.blocktime = timeofmine
                print(f"Valid Block Found! NONCE = {self.nonce}, blockid is {self.blockid} at {timeofmine}\nBlockHash is {self.blockid}")
                self.blockmined = True
                self.miner = minerAddress
                self.calculateRaw()
                self.addBlockToChain(self.blockchainfile)
                break

    def validateBlock(self):
        # This checks if a block is valid, after its being mined, by hashing the data again with the nonce provided as
        # this should match the self.blockid and be less than the difficulty

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
            print("Validated Block")
        else:
            self.blockmined = False
            print("False!")

        return self.blockmined

    def calculateRaw(self):
        # This is the function to calculate a raw version of the block after it has been mined.

        '''
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
        '''

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
            print(f"NONCE: {nonce}")
            print(f"BLOCKTIME: {blocktime}")
            print(f"BLOCK HEIGHT: {blockheight}")
            print(f"PREVIOUS BLOCK ID/HASH : {self.previousblockhash}")
            print(f"DIFFICULTY: {difficultlyOfBlock}")
            print(f"MERKLE ROOT: {self.merkle}")
            print(f"SIZE OF TXS : {sizeTx}")
            print(f"TXS : {transactions}")
            print(f"MINER: {self.miner}")
            print("----------------------")

    def addBlockToChain(self, blockchainfile):
        # This adds the block to a specific file, blockchainfile

        if not self.blockmined:
            print("Cannot add a unmined block.")
        else:
            file = open(blockchainfile, "a")
            file.write(self.raw)
            file.write("\n")
            file.close()
            print("Successfully added to the blockchain!")

    def createBlockFromRaw(self, raw):
        # This creates a block from the raw block format.

        # Grabbing info from the raw block data
        blockid = raw[0:64]
        nonce = raw[64:80]
        blocktime = raw[80:93]
        blockheight = raw[93:103]
        prevblockid = raw[103:167]
        difficulty = raw[167:263]
        merkle = raw[263:327]
        sizeofTXs = int(raw[327:337], 16)
        transactions = raw[337:337 + sizeofTXs]
        miner = raw[-66:]

        # Parsing the transactions from raw to a transactions array
        index = 0
        self.transactions = []

        while index <= len( transactions ):
            txSize = transactions[0:8]
            txSize = int( txSize, 16 )
            index += 8
            tx = transactions[index:index + txSize]
            if tx == '':
                break
            print(tx)
            txO = Transaction(tx)
            self.transactions.append(txO)
            index += txSize

        # Correlating the current blocks attributes to these variables

        self.blockid = blockid
        self.nonce = int( nonce, 16 )
        self.blocktime = int(blocktime)
        self.height = int(blockheight)
        self.previousblockhash = prevblockid
        self.difficulty = int(difficulty, 16)
        self.merkle = merkle
        self.miner = miner
        self.raw = raw

# -------------------------------------------------- BLOCKCHAIN -------------------------------------------------------

class Blockchain:
    '''
        Here are some parameters:-
        Blocks - is the list of blocks currently in the blockchain file
        The height of blocks, the number of blocks in the blockchain file
        validChain - The validity of the chain, this is used to contribute a new block to the chain
        Difficulty - this parameter is calculated based on the time it took to mine each block
        Reward - this is based on the current supply of tokens, or is a fixed amount
    '''

    def __init__(self, blockchainfile):

        self.blocks = []
        self.height = 0
        self.validChain = False
        self.difficulty = None
        self.reward = None
        self.averageBlockTime = 60

        blockchain = open(blockchainfile, "r")
        for line in blockchain.readlines():
            line = line[:-1]
            block = Block()
            block.createBlockFromRaw(line)
            block.validateBlock()
            self.blocks.append(block)
            self.height += 1

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
        # This finds a blockid in the blockchain and returns raw if found, or returns false if not there.

        for block in self.blocks:
            if block.blockid == blockid:
                print(f"Found {block.blockid}!\nBlock Height: {block.height}")
                print(f"RAW BLOCK: {block.raw}")
                return block.raw

        print("Block Id not Found!")
        return False

    def findTxidsRelatingToKey(self, publicKey):
        # This function searches the blockchain for transactions that are either from the public address
        # or to the public address and will output two lists

        # There are going to be three types of transactions: Inputs, Outputs, and Coinbase
        # Inputs to the address:
        #   - This will be easy as we can just search the blockchain, by checking the scriptPubKey and decrypting
        #     it and seeing if we have a match with our public key
        #   - Then adding this in our input lists
        # Coinbase Transactions:
        #   - We can check if the scriptSig to this account is equal to the hash of coinbase and the
        #     scriptPubKey is the same
        #   - We can also check if the miner of the block is the same pychain address
        #   - Add to inputs List
        # Outputs from the address
        #   - For each transaction find the 'rawtx2' (from 'scriptSigCreator'), then and use the verifySig
        #     with the public keys in 'address'
        #   - If each any of the signature matches then add it on the Outputs list
        # Then display in a nice format and returning all inputs and outputs

        pyAddress = createAddress( publicKey )
        uncompressedAddress = "04 " + str( hex( publicKey[0] )[2:] ) + str( hex( publicKey[1] ) )[2:]
        inputs = []
        outputs = []

        for block in self.blocks:
            for transaction in block.transactions:
                try:
                    if pyAddress in transaction.outputAddress():
                        inputs.append(transaction)
                except IndexError:
                    pass

                for inputTx in inputs:
                    if inputTx.txid in transaction.inputTxids():
                        if inputTx not in outputs:
                            outputs.append(transaction)

        uniqueOutputs = []
        for output in outputs:
            if output not in uniqueOutputs:
                uniqueOutputs.append(output)

        outputs = uniqueOutputs

        print(f"---------INPUTS----------")
        for inputTx in inputs:
            print(inputTx.txid)

        print(f"---------OUTPUTS----------")
        for output in outputs:
            print(output.txid)

    def setReward(self, reward):
        # This sets the reward of each block, currently this has no implementation but could be added here.
        self.reward = reward


    def calculateDifficulty(self):
        # This will calculate the average time of the blocks and move the difficulty up or down by using a multiplier.
        # We get the last ten blocks, find the difference between the last block and the most recent block,
        # and then divide by 60.
        # We need to get this towards 1 so if we multiply by a multiplier that is 60/average this would be the best
        # way to get to 60 average time.

        twentyBlock = self.blocks[-10].blocktime
        currentBlock = self.blocks[-1].blocktime
        difference = currentBlock - twentyBlock
        difficulty = self.blocks[-1].difficulty
        multiplier = 600 / difference
        difficulty *= multiplier
        difficulty = int(difficulty)
        print(f"NEW DIFFICULTY = {difficulty}")
        return difficulty

    def validateChain(self):
        # We need to implement alot of features for a valid chain:
        #   - All blocks need to be in sequential order
        #   - All blocks need to have the correct previous block id
        #   - All blocks need to have a correct id (rehash the details of the block)

        self.validChain = False
        for i in range(len(self.blocks)):
            if len(self.blocks) == 1:
                self.validChain = True

            if i != len(self.blocks) - 1:
                # We are iterating through each block by comparing the nth block to the n+1th block,
                # upto the nth block in the list

                block1 = self.blocks[i]
                block2 = self.blocks[i + 1]

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

    x = Transaction("0101fcef71991fa65b75b67ab8dc7234c8e852b12f0f6f16932e75a592447ffc92c7000100208266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb440100000000000000640021697e66d2a581463fafe887d892fd1d724825bbe214b7b2547639dbc8a87f7cc25d00000000")
    print(x)
    print(x.txid)
    print(x.version)
    print(x.inputcount)
    print(x.outputcount)
    print(x.inputs)
    print(x.outputs)
    print(f"raw = {x.raw}")


if __name__ == "__main__":
    main()
