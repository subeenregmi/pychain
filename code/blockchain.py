# This will be the blockchain class that will regulate the rewards for the blocks, blockheight and difficulty,
# This will also parse the blockchain into blocks, for easy searching of transactions, this will also
# act as the distribution of the blockchain files. 

# Properties in a blockchain
# - Reward Mechanism
# - Difficulty Mechanism
# - Dictionary of TXIDs for specific address
# - TXID Search
# - Blockchain parsing into Blocks

class Blockchain():
    def __init__(self, blockchainfile):
        self.blocks = []
        self.blockheight
        
        try: 
            with open(blockchainfile, "a+w") as blockchain:
                
            