import socket
import threading
from ..address import ECmultiplication, Gx, Gy
from ..blockchain import Blockchain


# Our blockchain only works if there is a way of distributing the blockchain(s) files,
# there are two main ways to implement this. One way would be through centralization,
# by maintaining the files by an central server, however if this server goes down, there is
# no way to maintain the blockchain, and even so, the server can also make changes to the
# blockchain that are not good to the users. Thus, the main way to do this to maintain the blockchain,
# is through a method of consensus and a peer-to-peer network that regulates the blockchain
# by itself, to do this a peer-to-peer network is essential.

# We will use sockets and threading to do this, and essentially a participant/node on the
# blockchain is basically a server and a client which can talk to other nodes.

PORT = 45569

class Node():
    def __init__(self, blockchainfile, privateKey):
        self.blockchain = Blockchain(blockchainfile)
        self.mempool = []
        self.privateKey = privateKey
        self.publicKey = ECmultiplication(privateKey, Gx, Gy)
        self.peers = []
        self.connectSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peerSocket.bind(("localhost", PORT))
        self.peerSocket.listen(256)

    def acceptPeers(self):
        print("")
        peer_socket, peer_address = self.socket.accept()
        self.peers.append(peer_socket)



