#!/usr/bin/env python3
from node import Peer
import json

with open('json/currentAccount.json') as user:
    user = json.load(user)
    blockchainfile = user["blockchainfile"]
    host = user["host"]
    portmin = user["portMin"]
    portmax = user["portMax"]
    maxpeers = user["maxPeers"]
    priv = user["privateKey"]

peer = Peer(blockchainfile, host, portmin, portmax, maxpeers, priv)
peer.mining = True
peer.startMine()