import socket
import threading
from address import ECmultiplication, Gx, Gy
from blockchain import Blockchain
from transaction import Transaction
import queue
import select
import time

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
        except ValueError:
            pass

        self.publickey = ECmultiplication(privateKey, Gx, Gy)
        self.mempool = []
        self.UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPsocket.bind((self.host, SERVER_UDP_SERVER))
        self.peers = []
        self.threads = []
        self.listening = True

    def getFreePort(self):
        # This function returns a free ports from the ports list
        return self.ports.pop()

    def listenOnUDP(self):
        # This is our listening function that listens for any UDP connection requests, and when one is received it
        # sends a connection to the sender on the port provided. It also creates a thread for listening onto that
        # connection.

        # We need to make sure we do not exceed the maxpeers and we are in listening mode.
        while len(self.peers) != self.maxpeers and self.listening:

            # We make our UDP socket to start to listen for any requests
            print(f"<UDP SOCK> {self.UDPsocket.getsockname()} is listening")
            message, address = self.UDPsocket.recvfrom(1024)
            message = message.decode('utf-8')
            print(f"<UDP SOCK> Message received : {message} from {address}")

            # If the message is in the correct format for a peer connection then we can process it.
            if message[0:2] == "CR":

                # We get the port from the message received and pick a port from the unused ports.
                port = int(message[3:])
                print(f"<UDP SOCK> PORT FROM MESSAGE = {port}")
                tries = 1
                local_port = self.getFreePort()

                # We try and connect five times
                while tries < 6:
                    try:
                        # We create a socket for every time we try and connect
                        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        connection_socket.bind((self.host, local_port))
                        connection_socket.settimeout(30.0)
                        print(f"<UDP SOCK> Trying to connect to {(address[0], port)}")
                        connection_socket.connect((address[0], port))

                        # Once a connection has been established we can add it onto our connected peers
                        self.peers.append(connection_socket)
                        print(f"<UDP SOCK> Connection to {address[0]} established!")

                        # We are also going to create a thread that listens on the TCP socket
                        thread = threading.Thread( target=self.listenOnTCP, args=(connection_socket,) )
                        self.threads.append(thread)
                        thread.start()
                        break

                    except:
                        print(f"<UDP SOCK> Trying again, tries: {tries}")
                        tries += 1

                # If the peer fails to connect in five attempts it stops trying to connect
                if tries == 5:
                    print(f"<UDP SOCK> Connection with {address[0]} unsuccessful!")

            else:
                print("<UDP SOCK> Invalid Message Format CR:{PORT}")

    def listenOnTCP(self, socket):
        # We need to also start listening to the peer-to-peer connections for transactions and peer list requests.

        # By not using "while True", we choose when to listen
        print(f"<TCP LISTEN> Listening on {socket.getpeername()}...")
        socket.settimeout(None)
        while self.listening:

            message = socket.recv(1024)
            message = message.decode('utf-8')

            # If a peer disconnects then we can get out of this and no longer listen on this connection
            if message == "":
                self.peers.remove(socket)
                print(f"<TCP LISTEN> Peer {socket.getpeername()} disconnected")
                break

            # When we receive a message we check if it is in TX format, so we can create the transaction object
            # and store it onto our mempool
            if message[:2] == "TX":

                print(f"<TCP LISTEN> Transaction received from {socket.getpeername()}")

                try:
                    raw_transaction = message[3:]
                    print(raw_transaction)
                    transaction = Transaction(raw_transaction)
                    self.mempool.append(transaction)
                    print(f"<TCP LISTEN> Added Transaction to mempool")
                    print(f"<TCP LISTEN> Mempool = {self.mempool}")

                except:
                    # If the raw transaction sent by a peer is invalid, then we reject it and move on
                    print(f"<TCP LISTEN> Transaction not valid")

            # When we receive a PLR from a peer, we need to send them back our list of peers in a Peer List Request
            # Receieved (PLRR) packet
            elif message[:3] == "PLR":
                # The correct format for a PLR request is:
                # "PLR:[192.0.0.0]

                print(f"<TCP LISTEN> Peer List Request from {socket.getpeername()} ")
                peer_list_request_received = "PLRR:("

                # We are putting all the peers ips into the square brackets, but we do not want to send the requesters
                # own ip.
                for peer in self.peers:
                    peerIp = peer.getpeername()
                    if peerIp == socket.getpeername:
                        continue
                    peer_list_request_received += f"[{peerIp}]"
                peer_list_request_received += ")"

                # This just encodes ands sends the packet back.
                print(f"<TCP LISTEN> PLRR : {peer_list_request_received} to {socket.getpeername()} ")
                peer_list_request_received.encode('utf-8')
                socket.send(peer_list_request_received)

            # This is only used if the
            elif message[:4] == "PLRR":
                pass



            # The peer only accepts packets that contain certain starting values.
            else:
                print("<TCP LISTEN> Invalid Format: TX{RAWTX}")

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

    def sendPeerListRequest(self):
        # A peer list request is a request to a peer to send its peers it connected to.
        # It works as follows, our PLR request is made up of the "PLR:" tag and the [host ip], the idea is that a node
        # that receives a PLR request, sends all their connected peers back to the PLR requester via their UDPsocket
        # however the node also sends the PLR request to their connected peers. Then the cycle repeats.
        # The PLR requester now has a list of peers, but their may be some duplicates, so it removes duplicates from the
        # possible peers list, after doing so, it trys to connect to the peers from that list.

        peer_list_request = f"PLR:[{self.host}]"
        peer_list_request = peer_list_request.encode('utf-8')

        for peer in self.peers:
            print(f"PeerListRequest(PLR) sent to {peer.getsockname()}")
            peer.send(peer_list_request)


def main():
    p1 = Peer("blockchain.txt", "192.168.0.201", 50000, 50500, 10, 8888)
    nodeThread = threading.Thread(target=p1.listenOnUDP)
    nodeThread.start()




if __name__ == "__main__":
    main()
