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
PORT = 50001
UDP_SERVER_PORT = 50000
MAXPEERS = 10

class Peer():
    def __init__(self):
        # We need a mempool, to hold transactions before mining, we need to access the block
        # We also need to create a server socket on the udp port and for that to always listen
        # For now we need to make nodes just talk to create a connection and send data.

        self.mempool = []
        self.UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPsocket.bind((HOST, UDP_SERVER_PORT))
        self.UDPsocket.listen(MAXPEERS)
        self.peers = []

    def connectToPeer(self, ip):
        message = f"CR:{HOST},{PORT}"
        tries = 0
        while tries != 5:
            try:
                self.UDPsocket.sendto(message.encode('utf-8'), (ip, UDP_SERVER_PORT))
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.bind((HOST, PORT))
                peer_socket.settimeout(30.0)
                connected_peer, connected_address = peer_socket.accept()
                self.peers.append(connected_peer)
                print(f"Connection to {ip} is successful!")
                return True
            except:
                tries += 1
                continue

        print(f"Connection to {ip} is unsuccessful")
        return False

    def listenForPeers(self):
        while len(self.peers) != MAXPEERS:
            message, address = self.UDPsocket.recvfrom(1024)
            message.decode('utf-8')
            if message[0:2] == "CR":
                IpInfo = message[3:]

            else:
                continue

