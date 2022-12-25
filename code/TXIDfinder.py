import pickle
import gzip

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
                print(f"Valid Block Found! NONCE = {self.nonce}, blockid is {self.blockid} at {timeofmine}\n")
                self.blockmined = True
                break

def findTXID(blockchainfile):
    txidfound = False
    items = loadblockchain(blockchainfile)
    for x in items:
        print(x)

def loadblockchain(filename):
    with open(filename, "rb") as file:
        while True:
            try: 
                yield pickle.load(file)
            except EOFError:
                break
    

findTXID(r'E:\python\pychain\pychain\code\blockchain.pickle')