import time
from blockchain import Blockchain, Block

x = Block()

testchain = Blockchain("testchain.txt")
print(testchain.height)
transactions = []


while True:
    if testchain.height == -1 or testchain.height==0:
        print("Starting Block")
        newHeight = testchain.height + 1
        newDifficulty = 135607040845515931344379931619614108352879381342049336509327220462845952
        previousBlockHash = "7cb95d760cbecec3e8f537d55a307ba8e5598ecce09ece40fcffc50ca7028735"

        newBlock = Block(newHeight, transactions, newDifficulty, previousBlockHash)
    else:
        height = testchain.height+1
        newDifficulty = testchain.calculateDifficulty()
        testchain.difficulty = newDifficulty
        previousBlockHash = testchain.blocks[-1].blockid
        newBlock = Block(height, transactions, newDifficulty, previousBlockHash)

    testchain.height += 1

    newBlock.blockchainfile = "testchain.txt"
    newBlock.mine((2222, 5555), 0)
    testchain.blocks.append(newBlock)
    difference = testchain.blocks[-1].blocktime - testchain.blocks[-2].blocktime
    print(f"Difference in block times = {difference}")
    time.sleep(5)