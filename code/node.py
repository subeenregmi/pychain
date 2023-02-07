import socket
import threading
from address import ECmultiplication, Gx, Gy
from blockchain import Blockchain
from transaction import Transaction

# Our blockchain only works if there is a way of distributing the blockchain(s) files,
# there are two main ways to implement this. One way would be through centralization,
# by maintaining the files by a central server, however if this server goes down, there is
# no way to maintain the blockchain, and even so, the server can also make changes to the
# blockchain that are not good to the users. Thus, the main way to do this to maintain the blockchain,
# is through a method of consensus and a peer-to-peer network that regulates the blockchain
# by itself, to do this a peer-to-peer network is essential.

# We will use sockets and threading to do this, and essentially a participant/node on the
# blockchain is basically a server and a client which can talk to other nodes.

SERVER_UDP_SERVER = 60000


class Peer():
    def __init__(self, blockchainfile, host, portMin, portMax, maxPeers, privateKey):
        # We need a mempool, to hold transactions before mining, we need to access the block
        # We also need to create a server socket on the udp port and for that to always listen
        # For now we need to make nodes just talk to create a connection and send data.
        self.host = host
        self.maxpeers = maxPeers
        self.blockchain = Blockchain(blockchainfile)
        self.ports = []

        for i in range(portMin, portMax):
            self.ports.append(i)

        try:
            self.ports.remove(SERVER_UDP_SERVER)
        except:
            pass

        self.publickey = ECmultiplication(privateKey, Gx, Gy)
        self.mempool = []
        self.UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPsocket.bind((self.host, SERVER_UDP_SERVER))
        self.peers = []

    def getFreePort(self):
        # This function returns a free ports from the ports list
        return self.ports.pop()

    def listen(self):
        # This is our listening function that listens for any UDP connection requests, and when one is received it
        # sends a connection to the sender on the port provided.

        # we need to make sure we do not exceed the max peers the node has set.
        while len(self.peers) != self.maxpeers:

            # We make our UDP socket to start to listen for any requests
            print(f"{self.UDPsocket.getsockname()} is listening")
            message, address = self.UDPsocket.recvfrom(256)
            message = message.decode('utf-8')
            print(f"Message received : {message} from {address}")

            # If the message is in the correct format for a peer connection then we can process it.
            if message[0:2] == "CR":

                # We get the port from the message received and pick a port from an unused port in the range
                port = int(message[3:])
                print(f"PORT FROM MESSAGE = {port}")
                tries = 0
                local_port = self.getFreePort()

                # We try and connect five times otherwise we give up
                while tries < 5:
                    try:
                        # We create a socket for every time we try and connect
                        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        connection_socket.bind((self.host, local_port))
                        connection_socket.timeout(30.0)
                        print(f"Trying to connect to {(address[0], port)}")
                        connection_socket.connect((address[0], port))

                        # Once a connection has been established we can add it onto our connected peers
                        self.peers.append(connection_socket)
                        print(f"Connection to {address[0]} established!")
                        break
                    except:
                        print(f"Trying again, tries: {tries}")
                        connection_socket.close()
                        tries += 1

                # If the peer fails to connect in five attempts it stops trying to connect
                if tries == 4:
                    print(f"Connection with {address[0]} unsuccessful!")

            elif message[0:2] == "TX":
                # If the format is in transaction format then we can instantiate

                rawTx = message[3:]
                try:
                    transaction = Transaction(rawTx)
                    self.mempool.append(transaction)
                except:
                    print(f"Raw Transaction in incorrect form!")


            else:
                print("Invalid Message Format CR:{PORT}, TX:{RAWTX}")

    def connectToPeer(self, ip):
        # This creates the message that will be sent in the UDP packet
        port = self.getFreePort()
        message = f"CR:{port}"
        tries = 0
        print(f"Connecting to {ip}")
        print(f"Message: {message}")

        # We send the package 5 times and listen 5 times, if not the connection fails
        while tries != 5:

            # This sends the packet to the server udp socket of who we are trying to connect to
            print(f"Sending {message} to {(ip, SERVER_UDP_SERVER)}")
            self.UDPsocket.sendto(message.encode('utf-8'), (ip, SERVER_UDP_SERVER))

            # This creates a new socket, hosted on the free port, setting us up to receive a connection
            # we also set a timeout for our socket as otherwise we would be forever waiting for a connection
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.bind((self.host, port))
            peer_socket.settimeout(150.0)
            peer_socket.listen()
            print(f"{peer_socket.getsockname()} has been created")

            # We now start listening on our socket for any new connections
            print(f"{peer_socket.getsockname()} is listening")
            connected_peer, connected_address = peer_socket.accept()
            self.peers.append(connected_peer)
            print(f"Connection to {ip} is successful!")
            return True

        print(f"Connection to {ip} is unsuccessful")
        return False

    def sendTransaction(self, rawtx):
        # This sends a transaction to all the connected peers, in the format TX:{rawtx}

        transaction_message = f"TX:{rawtx}"
        print(f"TRANSACTION TO BE SENT: {transaction_message}")
        transaction_message = transaction_message.encode('utf-8')
        for peer in self.peers:
            peer.send(transaction_message)
            print(f"Message sent to {peer.getsockname()}")



def main():
    p1 = Peer("blockchain.txt", "127.0.0.1", 50000, 50500, 10, 8888)
    print(p1.publickey)
    print(p1.blockchain.blocks[0].raw)


if __name__ == "__main__":
    main()
