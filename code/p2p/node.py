import socket
import threading


# Our blockchain only works if there is a way of distributing the blockchain(s) files,
# there are two main ways to implement this. One way would be through centralization,
# by maintaining the files by an central server, however if this server goes down, there is
# no way to maintain the blockchain, and even so, the server can also make changes to the
# blockchain that are not good to the users. Thus, the main way to do this to maintain the blockchain,
# is through a method of consensus and a peer-to-peer network that regulates the blockchain
# by itself, to do this a peer-to-peer network is essential.

# We will use sockets and threading to do this, and essentially a participant/node on the
# blockchain is basically a server and a client which can talk to other nodes.

SERVER_UDP_SERVER = 50001
class Peer():
    def __init__(self, host, portMin, portMax, maxPeers):
        # We need a mempool, to hold transactions before mining, we need to access the block
        # We also need to create a server socket on the udp port and for that to always listen
        # For now we need to make nodes just talk to create a connection and send data.
        self.host = host
        self.maxpeers = maxPeers

        self.ports = []

        for i in range( portMin, portMax ):
            self.ports.append(i)

        try:
            self.ports.remove(SERVER_UDP_SERVER)
        except:
            pass

        self.mempool = []
        self.UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPsocket.bind((self.host, SERVER_UDP_SERVER))
        self.peers = []

    def getFreePort(self):
        # This function returns a free ports from the ports list
        return self.ports.pop()

    def connectToPeer(self, ip):
        # This creates the message that will be sent in the UDP packet
        port = self.getFreePort()
        message = f"CR:{port}"
        tries = 0
        print(f"Connecting to {ip}")
        print(f"Message: {message}")

        # We send the package 5 times and listen 5 times, if not the connection fails
        while tries != 5:

            # this sends the packet to the server udp socket of who we are trying to connect to
            self.UDPsocket.sendto(message.encode('utf-8'), (ip, SERVER_UDP_SERVER))

            # this creates a new socket, hosted on the free port, setting us up to receive a connection
            # we also set a timeout for our socket as otherwise we would be forever waiting for a connection
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.bind((self.host, port))
            peer_socket.settimeout(30.0)
            peer_socket.listen(1)
            print(f"{peer_socket.getsockname()} has been created")

            # We now start listening on our socket for any new connections
            print(f"{peer_socket.getsockname()} is listening")
            connected_peer, connected_address = peer_socket.accept()
            self.peers.append(connected_peer)
            print(f"Connection to {ip} is successful!")
            return True

        print(f"Connection to {ip} is unsuccessful")
        return False

    def listenForPeers(self):
        # This is our listening function that listens for any UDP connection requests, and when one is received it
        # sends a connection to the sender on the port provided.

        # we need to make sure we do not exceed the max peers the node has set.
        while len(self.peers) != self.maxpeers:

            # We make our UDP socket to start to listen for any requests
            print(f"{self.UDPsocket.getsockname()} is listening")
            message, address = self.UDPsocket.recvfrom(1024)
            message = message.decode('utf-8')
            print(f"Message received : {message} from {address}")

            # If the message is in the correct format then we can process it otherwise the packet is disregarded.
            if message[0:2] == "CR":

                # We get the port from the message received and pick a port from an unused port in the range
                port = int(message[3:])
                print(f"PORT FROM MESSAGE = {port}")
                tries = 0
                local_port = self.getFreePort()

                # We try and connect five times otherwise we give up
                while tries <= 5:
                    try:
                        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        connection_socket.bind((self.host, local_port))
                        print(f"Trying to connect to {(address[0], port)}")
                        connection_socket.connect((address[0], port))

                        # Once a connection has been established we can add it onto our connected peers
                        self.peers.append(connection_socket)
                        print(f"Connection to {address[0]} established!")
                        return True
                    except:
                        tries += 1
                        pass

                # If the peer fails to connect in five attempts it stops try to connect
                print(f"Connection with {address[0]} unsuccessful!")
                return False

            else:
                print("Invalid Message Format CR:{PORT}")
                continue



def main():
    p1 = Peer("localhost", 50002, 50500, 10)
    p2 = Peer("localhost", 60000, 60500, 10)

    # P1 CONNECTS TO P2, P2 is listening, and p2 initiates by sending the udp packet
    # p1s free port, 50001, udp port 50000
    # p2s free port, 60001, udpport 60000

    # listenThread = threading.Thread(target=p2.listenForPeers, daemon=True)
    #
    # connectingThread = threading.Thread(target=p1.connectToPeer, args=("localhost",))
    #
    # listenThread.start()
    # connectingThread.start()

mainThread = threading.Thread(target=main())
mainThread.start()
