import socket
import threading
from address import ECmultiplication, Gx, Gy
from blockchain import Blockchain
from blockcreator import Block
from transaction import Transaction
from scriptsigdecoder import decoder
from scriptSigCreator import createEmptyTxForSign
from spubKeydecoder import breakDownLockScript
from opcodeBlocks import runScript
import queue
import select
import time
import rawtxdecoder

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
        self.blockchainfile = blockchainfile

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
        while self.listening and len(self.peers) <= self.maxpeers:

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
                        thread = threading.Thread(target=self.listenOnTCP, args=(connection_socket,))
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
                    # This is the parsing of the transactions as they now contain a public key, implemented by using a
                    # four-character text buffer.

                    message = message[3:]
                    txlength = message[:4]
                    txlength = int(txlength, 16)
                    transaction = message[4:4 + txlength]
                    public_key = message[4 + txlength:]
                    pubxlength = public_key[:4]
                    pubxlength = int(pubxlength, 16)
                    pubx = public_key[4:4 + pubxlength]
                    pubylength = public_key[4 + pubxlength: 8 + pubxlength]
                    pubylength = int(pubylength, 16)
                    puby = public_key[8 + pubxlength: 8 + pubxlength + pubylength]
                    pubx = int(pubx)
                    puby = int(puby)
                    transaction = Transaction(transaction)

                    # If this is a valid transaction we can add it our mempool and mine it.
                    if self.validateTransaction(transaction, (pubx, puby)):

                        self.mempool.append(transaction)
                        print(f"<TCP LISTEN> Added Transaction to mempool.")

                    else:
                        print("<TCP LISTEN> Invalid Transaction")

                except:
                    # If the raw transaction sent by a peer is invalid, then we reject it and move on
                    print(f"<TCP LISTEN> Transaction not valid")

            # When we receive a PLR from a peer, we need to send them back our list of peers in a Peer List Request
            # Receieved (RPLR) packet
            elif message[:3] == "PLR":
                # The correct format for a PLR request is:
                # "PLR:[192.0.0.0]

                print(f"<TCP LISTEN> Peer List Request from {socket.getpeername()} ")
                peer_list_request_received = "RPLR:("

                # We are putting all the peers ips into the square brackets, but we do not want to send the requesters
                # own ip.
                for peer in self.peers:
                    peerIp = peer.getpeername()[0]
                    if peerIp == socket.getpeername()[0]:
                        continue
                    peer_list_request_received += f"[{peerIp[0]}]"
                peer_list_request_received += ")"

                # This just encodes ands sends the packet back.
                print(f"<TCP SEND> Sending RPLR : {peer_list_request_received} to {socket.getpeername()} ")
                peer_list_request_received = peer_list_request_received.encode('utf-8')
                socket.send(peer_list_request_received)

            # This is how we will deal with a RPLR from a PLR request we sent
            elif message[:4] == "RPLR":
                # The standard form for a RPLR is:
                # RPLR:([192.0.0.1][12.34.56.78])

                # First we need to check if the RPLR is in the right format, if it not then we cannot go further
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
                        parenthesis_stack.append(char)
                        continue
                    elif char == ')' or char == ']':
                        try:
                            checkchar = parenthesis_stack.pop()
                        except IndexError:
                            valid = False
                            break

                        if checkchar == "(" and char == ")":
                            continue

                        if checkchar == '[' and char == ']':
                            continue
                        else:
                            valid = False
                            break
                    else:
                        continue

                # If the parenthesis are valid, then we take out the ips from the RPLR and if the user is already
                # connected to one then we don't try to connect again. Otherwise, we try to connect.
                if valid:

                    possible_peers = possible_peers.replace("(", "")
                    possible_peers = possible_peers.replace(")", "")
                    possible_peers = possible_peers.replace("[", "")
                    possible_peers = possible_peers.replace("]", " ")
                    possible_peers = possible_peers.split()
                    print(f"<TCP LISTEN> Possible Peers from RPLR: {possible_peers} ")

                    if len(possible_peers) == 0:
                        print("<TCP LISTEN> No new peers. ")
                        continue

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
                    print(f"<TCP LISTEN> Parenthesis on RPLR is invalid.")

            elif message[:6] == "RAWBLS":
                # This indicates that a raw block is being sent to the user. Once the block has arrived we instatiate it
                # ,validate the block and add it to our chain.

                rawBlock = message[7:]
                print(f"<TCP LISTEN> Raw Block from {socket.getpeername()[0]} : {rawBlock}")

                try:
                    newBlock = Block()
                    newBlock.createBlockFromRaw(rawBlock)
                    validated = newBlock.validateBlock()
                    if validated:
                        self.blockchain.blocks.append(newBlock)
                        print(f"<TCP LISTEN> Block has been added.")
                        newBlock.addBlockToChain("blockchain.txt")
                        continue
                    else:
                        print(f"<TCP LISTEN> Block is invalid.")
                except:
                    print(f"<TCP LISTEN> Invalid Block.")

            # The peer only accepts packets that contain certain starting values.
            else:
                print("<TCP LISTEN> Invalid Format: TX{RAWTX}")

    def connectToPeer(self, ip):
        # This creates the message that will be sent in the UDP packet
        port = self.getFreePort()
        tries = 0
        print(f"<TCP CONNECT> Connecting to {ip}")

        # We send the package 5 times and listen 5 times, if not the connection fails
        while tries != 5:

            # This creates a new socket, hosted on the free port, setting us up to receive a connection
            # we also set a timeout for our socket as otherwise we would be forever waiting for a connection

            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # This allows us to not run into the PORT IS BEING USED errors, by picking the next available port
            try:
                peer_socket.bind((self.host, port))
            except OSError:
                valid = False
                while not valid:
                    try:
                        new_port = self.getFreePort()
                        peer_socket.bind((self.host, new_port))
                        port = new_port
                        valid = True
                    except OSError:
                        continue

            message = f"CR:{port}"

            peer_socket.settimeout(150.0)
            peer_socket.listen()
            print(f"<TCP CREATE>{peer_socket.getsockname()} has been created")

            # This sends the packet to the server udp socket of who we are trying to connect to
            print(f"<TCP SEND> Sending {message} to {(ip, SERVER_UDP_SERVER)}")
            self.UDPsocket.sendto(message.encode('utf-8'), (ip, SERVER_UDP_SERVER))

            # We now start listening on our socket for any new connections
            print(f"<TCP LISTEN> {peer_socket.getsockname()} is listening")
            connected_peer, connected_address = peer_socket.accept()
            self.peers.append(connected_peer)
            thread = threading.Thread(target=self.listenOnTCP, args=(connected_peer,))
            thread.start()
            self.threads.append(thread)
            print(f"<TCP CONNECT> Connection to {ip} is successful!")
            return True

        print(f"<TCP CONNECT> Connection to {ip} is unsuccessful")
        return False

    def sendTransaction(self, rawtx, pk):
        # This sends a transaction to all the connected peers, in the format TX:{rawtx}
        # Update 10.02.2023: This also need to contain a public key, for sending maybe putting a buffer after the tx,
        # so we know what the public key is.

        public_key_x_length = hex(len(str(pk[0])))[2:].zfill(4)
        public_key_y_length = hex(len(str(pk[1])))[2:].zfill(4)
        transaction_length = hex(len(rawtx))[2:].zfill(4)

        # Below is the pychain standard for transaction transmission
        transaction_message = f"TX:{transaction_length}{rawtx}{public_key_x_length}{pk[0]}{public_key_y_length}{pk[1]}"
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

        print(self.peers)
        for peer in self.peers:
            print(f"<TCP SEND> PeerListRequest(PLR) sent to {peer.getsockname()}")
            peer.send(peer_list_request)

    def sendBlock(self, height, ip=None):
        # This function sends a block to either one person, or to all peers with the prefix "RAWBLS" - which means
        # raw block sent - this is used to send a specific peer or peers a block

        send_block = "RAWBLS:"

        # this checks if we are sending to one person, or all
        if ip is not None:
            peer = self.checkIPisPeer(ip)
            if peer is False:
                print(f"<TCP SEND BLOCK> IP does not correlate to a valid peer.")
                return False
            # we need to try and get the block from our blockchain.txt file, as if we specify a height that is too big
            # the block may not exist
            try:
                raw_block_at_height = self.blockchain.blocks[height].raw
                send_block += raw_block_at_height
                print(f"<TCP SEND BLOCK IP> Sending block at height {height}: {send_block}")
                send_block = send_block.encode('utf-8')
                peer.send(send_block)
                return True
            except IndexError:
                print(f"<TCP SEND BLOCK IP> Block at height: {height} does not exist.")
                return False
        else:
            try:
                raw_block_at_height = self.blockchain.blocks[height].raw
                send_block += raw_block_at_height
                print(f"<TCP SEND BLOCK PEERS> Sending block at height {height}: {send_block}")
                send_block = send_block.encode('utf-8')
                for peer in self.peers:
                    peer.send(send_block)
                return True
            except IndexError:
                print(f"<TCP SEND BLOCK PEERS> Block at height {height} does not exist.")
                return False

    def checkIPisPeer(self, ip):
        # This function checks if the parameter ip is a connected peer, and returns the socket if it is a peer.
        # this returns false if the ip is not a peer, and the socket if the ip is a peer

        if ip == self.host:
            print(f"<IP CHECK> Ip is host.")
            return False
        # we check if the ip is the same our sockets remote address if so that ip is a peer
        for peer in self.peers:
            if peer.getpeername()[0] == ip:
                print(f"<IP CHECK> {ip} is a peer.")
                return peer
        print(f"<IP CHECK> {ip} is NOT a peer.")
        return False

    def validateTransaction(self, transaction, public_key):
        # This function will validate a transaction when we recieve it, and this determines if the transactions reach
        # our mempool, to be mined.
        try:

            # We first decode our raw transaction into a dictionary
            transactionDict = rawtxdecoder.decodeRawTx(transaction.raw)
            inputs = int(transactionDict["InputCount"])
            for i in range(inputs):
                # For each input we get the txid, vout and the sig
                txid = transactionDict[f"txid{i}"]
                vout = transactionDict[f"vout{i}"]
                vout = int(vout, 16)
                sig = transactionDict[f"scriptSig{i}"]

                # We find the transaction that is used for a input and take the scriptPubKey
                previousTransaction = self.blockchain.findTxid(txid)
                previousTransactionDict = rawtxdecoder.decodeRawTx(previousTransaction)
                scriptPubKey = previousTransactionDict[f"scriptPubKey{vout}"]

                script = breakDownLockScript(scriptPubKey)
                sig = decoder(sig)
                stack = [sig, public_key]

                # This creates the hash of the message the signature is used on.
                rawtx2 = createEmptyTxForSign(transactionDict)

                truth = runScript(stack, script, rawtx2)

                if truth == [1]:
                    # We have to check all the signatures with their respective inputs.
                    continue
                else:
                    return False

        except:
            print("<TX VALIDATE> Transaction is invalid.")

        print(f"<TX VALIDATE> Transaction is valid!")
        return True

def main():
    p1 = Peer("blockchain.txt", "192.168.0.201", 50000, 50500, 10, 8888)
    nodeThread = threading.Thread(target=p1.listenOnUDP)
    nodeThread.start()
    p1.connectToPeer("192.168.0.111")
    p1.sendTransaction("01017b6632fce3914fd9b098a10760a995a41dcb260a9a740b7ed6fd0902e2c47ed600000042408b22520c20af4de60e54aa2af78486e661efbffc38286253a54bcf24ab2b79934020d79daebf01adb60a15f87eec4c2f41bf5804eab89a8aa995b6224f15f5782c010000000000000064002676a92169b75cdd59e53f0ced19cbf30efad3ec5ea3026f805d9e1ed6aea18f5a593e29b788ac00000000", (92641855401206585750031304985966472123204240504167073082041014802408154789641, 5320727137213493453320294950656953718594582159943012446202168292331376026727))

if __name__ == "__main__":
    main()
