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

HOST = "localhost"
PORT = 45569

class Node():
    def __init__(self, blockchainfile, privateKey):

        self.blockchain = Blockchain(blockchainfile)
        self.mempool = []
        self.privateKey = privateKey
        self.publicKey = ECmultiplication(privateKey, Gx, Gy)
        self.peers = []
        self.acceptingPeers = True

        self.serverPeerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientPeerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.serverPeerSocket.bind((HOST, PORT))
        self.clientPeerSocket.bind((HOST, PORT+1))

        self.clientPeerSocket.listen(256)
    def acceptPeers(self):
        print("-----------LISTENING FOR CONNECTIONS--------")
        while self.acceptingPeers:
            peer_socket, peer_address = self.serverPeerSocket.accept()
            self.peers.append(peer_socket)
            print(f"Established Connection with {peer_address}")
        print("---------STOPPED LISTENING FOR CONNECTIONS--------")

    def pingPeers(self):
        self.peerSocket.settimeout(30.0)
        for peer in self.peers:
            peer.send(f"Connection Test from {self.peerSocket.getsockname()}")
            data = self.peerSocket.recv(1024).decode('utf-8')
            if data == f"Test received from {peer.getsockname()}":
                print(f"Connection with {peer.getsockname()} is working!")
            else:
                print(f"{peer.getsockname} seems to be offline, removing from current peers.")
                self.peers.remove(peer)

    def tryToConnect(self, peerIp):
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_socket.bind((HOST, PORT+1))
        try:
            connection_socket.connect(peerIp, PORT)
            print(f"Connection with {peerIp} achieved!")
            self.peers.append(connection_socket)
            return True
        except:
            print(f"Connection with {peerIp} failed! :(")
            return False

