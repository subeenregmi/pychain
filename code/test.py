import time
from blockchain import Blockchain, Block

x = Block()

testchain = Blockchain("testchain.txt")
transactions = []


while True:
    if testchain.height == -1:
        print("Starting Block")
        newHeight = testchain.height + 1
        newDifficulty = 1030624440214420915914968798513281085745555590620308304445850822681559040
        previousBlockHash = "7cb95d760cbecec3e8f537d55a307ba8e5598ecce09ece40fcffc50ca7028735"

        newBlock = Block(newHeight, transactions, newDifficulty, previousBlockHash)
    else:
        height = testchain.height+1
        newDifficulty = testchain.calculateDifficulty()
        testchain.difficulty = newDifficulty
        previousBlockHash = testchain.blocks[-1].blockid
        newBlock = Block(height, transactions, newDifficulty, previousBlockHash)

    testchain.height += 1

    newBlock.mine((2222, 5555), 0)
    testchain.blocks.append(newBlock)
    newBlock.addBlockToChain("testchain.txt")
    difference = testchain.blocks[-1].blocktime - testchain.blocks[-2].blocktime
    print(f"Difference in block times = {difference}")
    time.sleep(5)