#!/usr/bin/env python3
from node import Peer
import json
from transaction import Transaction

# This opens the json file and adds the specific fields from the wallet client.
with open('json/currentAccount.json') as user:
    user = json.load(user)
    blockchainfile = user["blockchainfile"]
    host = user["host"]
    portmin = user["portMin"]
    portmax = user["portMax"]
    maxpeers = user["maxPeers"]
    priv = user["privateKey"]
    peers = user["peers"]
    mempool = user['mempool']

#  We create another peer object and then connect to the previous peers.
peer = Peer(blockchainfile, host, portmin, portmax, maxpeers, priv)

for transaction in mempool:
    tx = Transaction(transaction)
    print(tx.raw)
    peer.mempool.append(tx)

for peers_ in peers:
    peer.connectToPeer(peers_)

peer.mining = True
peer.startMine()