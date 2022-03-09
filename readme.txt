'''
blockchain in python

so first we need to establish some transactions

Subeen --> John 50 Tokens
Sathyam --> Adam 75 Tokens
Ayush --> Subeen 20 Tokens

we should create a block system to record these transactions

A block should have

Previous block hash
Block Height (to order chain)
Transactions
Nonce

We also need a mempool for pending transactions
--> Therefore we need to order this in some way (tx fee)

We also would need to send this transaction set to all the other nodes connected to this computer

we need to make a system where the chain with the biggest block wins and is the best chain and therefore everyone else
would need to update their chain

we need a way to include transactions in a block for an address way

we need to assign users with this blockchain a unique address and a password so others cannot hack into

we also need to assign a difficult nonce so therefore its not easy to hack


'''

# we are first going to setup address's


