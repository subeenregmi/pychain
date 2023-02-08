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
        while self.listening:

            # We make our UDP socket to start to listen for any requests
            print(f"<UDP SOCK> {self.UDPsocket.getsockname()} is listening")
            print("here")
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
                        thread = threading.Thread( target=self.listenOnTCP, args=(connection_socket,), daemon=True )
                        self.threads.append(thread)
                        thread.start()
                        print("here2")
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

            # This is how we will deal with a PLRR from a PLR request we sent
            elif message[:4] == "PLRR":
                # The standard form for a PLRR is:
                # PLRR:([192.0.0.1][12.34.56.78])

                # First we need to check if the PLRR is in the right format, if it not then we cannot go further
                # So first we need to check if the syntax is correct, we can easily do this by iterating through the
                # message and then checking if is an opening or closing bracket, and if it is opening, we push it onto
                # the stack, and if it is closing we pop the top element, and if the brackets match we can just continue
                # This will check for valid parenthesis
                possible_peers = message[5:]
                parenthesis_stack = []
                currentPeers = []
                valid = True

                for char in possible_peers:
                    if char == '(' or char == '[':
                        parenthesis_stack.append( char )
                        continue
                    elif char == ')' or char == ']':

                        try:
                            checkchar = parenthesis_stack.pop()
                        except IndexError:
                            valid = False
                            break

                        if checkchar == '[' and char == ']':
                            continue
                        else:
                            valid = False
                            break
                    else:
                        continue

                # If the parenthesis are valid, then we take out the ips from the PLRR and if the user is already
                # connected to one then we don't try to connect again. Otherwise we try to connect.
                if valid:

                    possible_peers = possible_peers.replace("(", "")
                    possible_peers = possible_peers.replace(")", "")
                    possible_peers = possible_peers.replace("[", "")
                    possible_peers = possible_peers.replace("]", " ")
                    possible_peers = possible_peers.split()
                    print(f"<TCP LISTEN> Possible Peers for PLR: {possible_peers} ")

                    for peer in self.peers:
                        currentPeers.append(peer.getpeername()[0])
                    for possiblePeer in possible_peers:
                        if possiblePeer in currentPeers:
                            continue
                        else:
                            connection_success = self.connectToPeer(possiblePeer)
                            if connection_success:
                                print(f"<TCP LISTEN> Connection with {possiblePeer} is sucessful!")
                            else:
                                print(f"<TCP LISTEN> Connection with {possiblePeer} is unsuccessful.")
                else:
                    print(f"<TCP LISTEN> Parenthesis on PLRR is invalid.")

            # The peer only accepts packets that contain certain starting values.
            else:
                print("<TCP LISTEN> Invalid Format: TX{RAWTX}")

    def connectToPeer(self, ip):
        # This creates the message that will be sent in the UDP packet
        port = self.getFreePort()
        message = f"CR:{port}"
        tries = 0
        print(f"<TCP CONNECT> Connecting to {ip}")
        print(f"<TCP CONNECT> Message: {message}")

        # We send the package 5 times and listen 5 times, if not the connection fails
        while tries != 5:

            # This sends the packet to the server udp socket of who we are trying to connect to
            print(f"<TCP SEND> Sending {message} to {(ip, SERVER_UDP_SERVER)}")
            self.UDPsocket.sendto(message.encode('utf-8'), (ip, SERVER_UDP_SERVER))

            # This creates a new socket, hosted on the free port, setting us up to receive a connection
            # we also set a timeout for our socket as otherwise we would be forever waiting for a connection
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.bind((self.host, port))
            peer_socket.settimeout(150.0)
            peer_socket.listen()
            print(f"<TCP CREATE>{peer_socket.getsockname()} has been created")

            # We now start listening on our socket for any new connections
            print(f"<TCP LISTEN> {peer_socket.getsockname()} is listening")
            connected_peer, connected_address = peer_socket.accept()
            self.peers.append(connected_peer)
            print(f"<TCP CONNECT> Connection to {ip} is successful!")
            return True

        print(f"<TCP CONNECT> Connection to {ip} is unsuccessful")
        return False

    def sendTransaction(self, rawtx):
        # This sends a transaction to all the connected peers, in the format TX:{rawtx}

        transaction_message = f"TX:{rawtx}"
        print(f"<TCP SEND> TRANSACTION TO BE SENT: {transaction_message}")
        transaction_message = transaction_message.encode('utf-8')
        for peer in self.peers:
            peer.send(transaction_message)
            print(f"<TCP SEND> Message sent to {peer.getsockname()}")

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
            print(f"<TCP SEND> PeerListRequest(PLR) sent to {peer.getsockname()}")
            peer.send(peer_list_request)


def main():
    p1 = Peer("blockchain.txt", "192.168.0.111", 50000, 50500, 10, 9999)
    nodeThread = threading.Thread(target=p1.listenOnUDP)
    nodeThread.start()

    p1.connectToPeer("192.168.0.201")

    p1.sendTransaction("0101fcef71991fa65b75b67ab8dc7234c8e852b12f0f6f16932e75a592447ffc92c7000100208266deca6c65b39468e6fb8596869a231b9582ee3818d12ba7240cb126ebfb440100000000000000640021697e66d2a581463fafe887d892fd1d724825bbe214b7b2547639dbc8a87f7cc25d00000000")

    p1.sendPeerListRequest()

if __name__ == "__main__":
    main()
