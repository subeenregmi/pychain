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
    def __init__(self, height=None, transactions=None, difficulty=None, previousblockhash=None): 
        self.height = height
        self.transactions = transactions
        merkle = ""
        if self.transactions != None:
            for x in self.transactions:
                merkle += x
        self.merkle = hashlib.sha256(merkle.encode('utf-8')).hexdigest()
        self.difficulty = difficulty
        self.previousblockhash = previousblockhash
        self.nonce = 0
        self.blockid = 0
        self.blocktime = 0
        self.blockmined = False
        self.raw = ""        

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
            #self.blockid = int(self.blockid, 16)
            print(f"Trying Nonce Value = {self.nonce}, hash is {self.blockid}")
            
            if int(self.blockid, 16) < self.difficulty:
                #self.blockid = hex(self.blockid)[2:]
                self.blocktime = timeofmine
                print(f"Valid Block Found! NONCE = {self.nonce}, blockid is {self.blockid} at {timeofmine}\n BlockHash is {self.blockid}")
                self.blockmined = True
                self.calculateRaw()
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

    def calculateRaw(self):
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
            for x in self.transactions:
                TxLength = str(hex(len(x))[2:]).zfill(8)
                transactions += TxLength
                transactions += x
            sizeTx = hex(len(transactions))[2:]
            sizeTx = sizeTx.zfill(10)
            raw = self.blockid + nonce + blocktime + blockheight + self.previousblockhash + difficultlyOfBlock + self.merkle + sizeTx + transactions
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
            print("----------------------")
            self.addBlockToChain()
    
    def addBlockToChain(self):
        if self.blockmined == False:
            print("Cannot add a unmined block.")
        else: 
            file = open("blockchain.txt", "a")
            file.write(self.raw)
            file.write("\n\n")
            file.close()
            print("Success")
    
    def createBlockFromRaw(self, raw):
        #Grabbing info from the raw block data

        blockid = raw[0:64]
        print(f"BlockIdFromRaw: {blockid}")
        nonce = raw[64:80]
        print(f"Nonce: {nonce}")
        blocktime = raw[80:93]
        blockheight = raw[93:103]
        prevblockid = raw[103:167]
        difficulty = raw[167:263]
        merkle = raw[263:327]
        sizeofTXs = int(raw[327:337], 16)
        transactions = raw[337:337+sizeofTXs]
        index = 337
        
        while True:
            size = transactions[0:8]
            index2 += int(size, 16)


        #Correlating the current blocks attributes to these variables
        self.blockid = blockid
        self.nonce = int(nonce, 16)
        self.blocktime = int(blocktime, 16)
        self.height = int(blockheight, 16)
        self.previousblockhash = prevblockid
        self.difficulty = int(difficulty, 16)
        self.merkle = merkle


        



def main():

    x = Block(1, ["0102ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d600001002046b7ebfe9b9639f6f88f77709b453f89ce380ae192202f1fd913864a4c3144948732d097e715d15e8ddd312749a97572bc97b6f8bc1692f08e82f90d0882258e00010020c2d28ed3a36ca0a8a3076d4c2dfa54c95383deee8ed16b63720f0561a86894650100000000000001f4002676a92169f38a6b51de7e9345992f2161c9c811a8b57cb2c1f31b8f98211b21af61096bd588ac00000000"], 110568172840591261314241097251219333984481879657863353467234327275223423263, "1b7990b9fd11da0d24a0f539e3ed3407285538737785acc6b7dcb602b0a68492")
    # # #y = Block(2, ["0102ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d600001002046b7ebfe9b9639f6f88f77709b453f89ce380ae192202f1fd913864a4c3144948732d097e715d15e8ddd312749a97572bc97b6f8bc1692f08e82f90d0882258e00010020c2d28ed3a36ca0a8a3076d4c2dfa54c95383deee8ed16b63720f0561a86894650100000000000001f400201b7990b9fd11da0d24a0f539e3ed3407285538737785acc6b7dcb602b0a6849200000000"], 110568172798640591261314241097512146939888796578635346723327275266671322463)
    x.mine()
    print(x.raw)

    v = Block()
    v.createBlockFromRaw(x.raw)

    


    #findTXID("ab696a951348d80c9360d0de0733eef12c6cd64e7bbaaf658acee42a61d32d60", "blockchain.pickle")

if __name__ == "__main__":
    main()




