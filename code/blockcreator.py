import pickle
import hashlib
import time

"""
block hash 

Height of block
TX merkle tree
Nonce
Difficulty 
Previous block hash

transactions - dividers between blocks and transactions

size of block data

size of transaction data 


1032312312312asd33924939

1

3290w894384f387432g

000003232sdfas

dmasidoj9032938n4f23

TXS

0102ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d600001002046b7ebfe9b9639f6f88f77709b453f89ce380ae192202f1fd913864a4c3144948732d097e715d15e8ddd312749a97572bc97b6f8bc1692f08e82f90d0882258e00010020c2d28ed3a36ca0a8a3076d4c2dfa54c95383deee8ed16b63720f0561a86894650100000000000001f4002676a92169f38a6b51de7e9345992f2161c9c811a8b57cb2c1f31b8f98211b21af61096bd588ac00000000

"""

class Block():
    def __init__(self, height, transactions, difficulty, previousblockhash): 
        self.height = height
        self.transactions = transactions
        merkle = ""
        for x in self.transactions:
            merkle += x
        self.merkle = hashlib.sha256(merkle.encode('utf-8')).hexdigest()
        self.difficulty = difficulty
        self.previousblockhash = previousblockhash
        self.nonce = 0
        self.blockid = 0
        self.blocktime = 0
        self.blockmined = False

    def mine(self):
        timeofmine = int(time.time())
        tobehashed = str(timeofmine) + str(self.height) + self.previousblockhash + str(self.difficulty) + self.merkle
        for x in self.transactions:
            tobehashed += x
            
        print(f"what is to be hashed = {tobehashed}\n")

        while True:
            self.nonce += 1
            tobehashed2 = str(self.nonce) + tobehashed
            #print(f"Hashing ... {tobehashed2}")
            self.blockid = hashlib.sha256(tobehashed2.encode('utf-8')).hexdigest()
            self.blockid = int(self.blockid, 16)
            print(f"Trying Nonce Value = {self.nonce}, hash is {self.blockid}")
            
            if self.blockid < self.difficulty:
                self.blockid = hex(self.blockid)[2:]
                self.blocktime = timeofmine
                print(f"Valid Block Found! NONCE = {self.nonce}, blockid is {self.blockid} at {timeofmine}\n BlockHash is {self.blockid}")
                self.blockmined = True
                break
                
        
    def validateBlock(self):
        checkid = str(self.nonce) + str(self.blocktime) + str(self.height) + self.previousblockhash + str(self.difficulty) + self.merkle
        for x in self.transactions:
            checkid += x
        checkid = hashlib.sha256(checkid.encode('utf-8')).hexdigest()[1:]
        if int(checkid, 16) == int(self.blockid, 16):
            print("Validated Block")
        else:
            print("False!")


def findTXID(txid, blockchainfile):
    txidfound = False
    items = loadblockchain(blockchainfile)
    for x in items:
        for i in x.transactions:
            txTxid = hashlib.sha256(i.encode('utf-8')).hexdigest()
            if txid == txTxid:
                print(f"TXID = {txid}\nMatches RawTX = {i}")
            else:
                print("Invalid")


def loadblockchain(filename):
    with open(filename, "rb") as file:
        while True:
            try: 
                yield pickle.load(file)
            except EOFError:
                break


def main():

    x = Block(1, ["0102ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d600001002046b7ebfe9b9639f6f88f77709b453f89ce380ae192202f1fd913864a4c3144948732d097e715d15e8ddd312749a97572bc97b6f8bc1692f08e82f90d0882258e00010020c2d28ed3a36ca0a8a3076d4c2dfa54c95383deee8ed16b63720f0561a86894650100000000000001f4002676a92169f38a6b51de7e9345992f2161c9c811a8b57cb2c1f31b8f98211b21af61096bd588ac00000000"], 11056817286405912613142410975121469398887965786353467233272752663671322463, "1b7990b9fd11da0d24a0f539e3ed3407285538737785acc6b7dcb602b0a68492")
    #y = Block(2, ["0102ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d600001002046b7ebfe9b9639f6f88f77709b453f89ce380ae192202f1fd913864a4c3144948732d097e715d15e8ddd312749a97572bc97b6f8bc1692f08e82f90d0882258e00010020c2d28ed3a36ca0a8a3076d4c2dfa54c95383deee8ed16b63720f0561a86894650100000000000001f400201b7990b9fd11da0d24a0f539e3ed3407285538737785acc6b7dcb602b0a6849200000000"], 110568172798640591261314241097512146939888796578635346723327275266671322463)
    x.mine()
    x.validateBlock()

    with open("blockchain.pickle", "wb") as file:
        pickle.dump(x, file)


    #findTXID("ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d60", "blockchain.pickle")

if __name__ == "__main__":
    main()




