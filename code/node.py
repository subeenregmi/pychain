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


class Peer:
    def __init__(self, blockchainfile, host, portMin, portMax, maxPeers, privateKey):
        # We need a mempool, to hold transactions before mining, we need to access the block
        # We also need to create a server socket on the udp port and for that to always listen
        # For now we need to make nodes just talk to create a connection and send data.
        self.miningBlock = None
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
        self.mining = False
        self.recentlyAddedBlocks = []

    def getFreePort(self):
        # This function returns a free ports from the ports list
        return self.ports.pop()

    def listenOnUDP(self):
        # This is our listening function that listens for any UDP connection requests, and when one is received it
        # sends a connection to the sender on the port provided. It also creates a thread for listening onto that
        # connection.

        # We need to make sure we do not exceed the max peers, and we are in listening mode.
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

            elif message == "ping":
                # If the UDP socket receives a ping, we will also send back a pong.
                message = "pong"
                message = message.encode('utf-8')
                self.UDPsocket.sendto(message, address)

            elif message == "pong":
                # If we receive a pong then we know that the host is alive
                print(f"<UDP PONG RECEIVE> {address} is alive!")

            else:
                print("<UDP SOCK> Invalid Message Format CR:{PORT}, or ping/pong.")

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
                        print(f"<TCP SEND> Transaction sent to peers.")
                        self.sendTransaction(transaction.raw, (pubx, puby), socket)

                    else:
                        print("<TCP LISTEN> Invalid Transaction")

                except:
                    # If the raw transaction sent by a peer is invalid, then we reject it and move on
                    print(f"<TCP LISTEN> Transaction not valid")

            # A Peer List Request (PLR) packets is used to request the peers of a peer. To respond back a Received Peer
            # List Request (RPLR) packet is sent back and this contains a list of connected peers.

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
                    newBlock = Block(self.blockchainfile)
                    newBlock.createBlockFromRaw(rawBlock)
                    validated = newBlock.validateBlock()

                    if self.validateBlockDifficulty(newBlock) is False:
                        print(f"<TCP LISTEN> Block has incorrect difficulty.")
                        break

                    if validated:
                        if newBlock not in self.blockchain.blocks:

                            self.blockchain.height += 1
                            self.blockchain.blocks.append(newBlock)
                            newBlock.addBlockToChain()
                            self.sendBlock(self.blockchain.height)
                            self.recentlyAddedBlocks.append(newBlock)
                            print(f"<TCP LISTEN> Block has been added.")
                            continue

                        else:
                            print(f"<TCP LISTEN> Block is already in chain.")
                    else:
                        print(f"<TCP LISTEN> Block is invalid.")
                except:
                    print(f"<TCP LISTEN> Invalid Block.")

            elif message[:3] == "RBC":
                # If we receive a Request Block Count packet, we will send back another Received Request Block Count
                # (RRBC) which contains the amount of blocks that we contain. We should also check the number of blocks
                # that came attached and see if we need to request any blocks.
                print(f"<REQUEST BLOCK COUNT> Request sent from {socket.getpeername()}")
                block_count = len(self.blockchain.blocks)
                try:
                    peer_block_count = int(message[4:])
                except ValueError:
                    print(f"<TCP LISTEN> Invalid Request Block Count packet.")
                    continue

                # Before anything, we should send back a RRBC packet.
                message = f"RRBC:{block_count}"
                message = message.encode('utf-8')
                socket.send(message)

                # If the peer has more packets that us we need to send a request block packet.
                if peer_block_count > block_count:
                    # We need to work what blocks need to be sent to us
                    for i in range(block_count+1, peer_block_count+1):
                        self.sendBlocksRequest(i, socket)
                else:
                    print(f"<REQUEST BLOCK COUNT> No new blocks to add.")
                    print(f"<RECEIVED REQUEST BLOCK COUNT> Sent to {socket.getpeername()}")

            elif message[:4] == "RRBC":
                # The Received Request Block Count packet, is in response to the Request Block Count packet, this always
                # has a number which indicates how many blocks the receiver has.
                block_count = len(self.blockchain.blocks)
                print(f"<RECEIVED REQUEST BLOCK COUNT> Sent from {socket.getpeername()}")

                try:
                    peer_block_count = int(message[5:])
                except ValueError:
                    print(f"<TCP LISTEN> Invalid Received Request Block Count format.")
                    continue

                # Here we are making a list of blocks that we need.
                blocks_list = []
                if peer_block_count > block_count:
                    for i in range(block_count+1, peer_block_count+1):
                        blocks_list.append(i)
                else:
                    print(f"<RECEIVED REQUEST BLOCK COUNT> No new blocks to add.")

                self.sendBlocksRequest(blocks_list, socket)

            elif message[:2] == "RB":
                # This is the request block packet, if we get a RB packet, we should send that block in our blockchain
                # We need to try to send as there is a bug when sending, packets arrive at the same time, so it forms a
                # single message that contains all the RB packets.

                print(f"<TCP LISTEN> Request Block packet from {socket.getpeername()}")
                try:
                    index = int(message[3:])
                    self.sendBlock(index, socket.getpeername()[0])

                # This is our exception handling, if the messages arrive all at once into one message
                except ValueError:
                    # We split the message up into just the indexes.

                    blocks = message.split('RB:')
                    for index in blocks:
                        if index == '':
                            continue
                        try:
                            index = int(index)
                            # This sleep is pivotal as mentioned previously the raw blocks will be sent all at once.
                            time.sleep(1)
                            self.sendBlock(index, socket.getpeername()[0])
                        except:
                            print(f"<ERROr>")

            elif message == "ping":
                # If we receive a ping message, we need to send a pong back. This is the conformation that this host is
                # alive. This is relating to the TCP Ping service.
                message = "pong"
                message = message.encode('utf-8')
                socket.send(message)

            elif message == "pong":
                print(f"<PONG RECEIVED> {socket.getpeername()} is alive!")


            # The peer only accepts packets that contain certain starting values.
            else:
                print(message)
                print("<TCP LISTEN> Invalid Format: TX{RAWTX}")

    def connectToPeer(self, ip):
        # This creates the message that will be sent in the UDP packet
        port = self.getFreePort()
        tries = 0
        print(f"<TCP CONNECT> Connecting to {ip}")

        # We send the package 5 times and listen 5 times, if not the connection fails
        while tries < 5:

            # This creates a new socket, hosted on the free port, setting us up to receive a connection
            # we also set a timeout for our socket as otherwise we would be forever waiting for a connection
            tries += 1
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

            peer_socket.settimeout(10)
            peer_socket.listen()
            print(f"<TCP CREATE>{peer_socket.getsockname()} has been created")

            # This sends the packet to the server udp socket of who we are trying to connect to
            print(f"<TCP SEND> Sending {message} to {(ip, SERVER_UDP_SERVER)}")
            self.UDPsocket.sendto(message.encode('utf-8'), (ip, SERVER_UDP_SERVER))

            # We now start listening on our socket for any new connections
            print(f"<TCP LISTEN> {peer_socket.getsockname()} is listening")
            try:
                connected_peer, connected_address = peer_socket.accept()
            except TimeoutError:
                print("Unsuccessful connection")
                if tries == 5:
                    break
                continue
            if tries == 5:
                break
            self.peers.append(connected_peer)
            thread = threading.Thread(target=self.listenOnTCP, args=(connected_peer,))
            thread.start()
            self.threads.append(thread)
            print(f"<TCP CONNECT> Connection to {ip} is successful!")
            return True

        print(f"<TCP CONNECT> Connection to {ip} is unsuccessful")
        return False

    def sendTransaction(self, rawtx, pk, sender=None):
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
            if sender is not None:
                if peer == sender:
                   continue
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
            # we need to try and get the block from our pychain.txt file, as if we specify a height that is too big
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

    def RequestBlockCount(self):
        # This function will send a block count request, that asks how much blocks a peer has, attached to this request
        # is the amount of blocks that the requester has. This way they can make the comparison locally and request
        # blocks.
        block_amount = len(self.blockchain.blocks)
        message = f"RBC:{block_amount}"
        message = message.encode('utf-8')

        for peer in self.peers:
            peer.send(message)
            print(f"<RBC SENT> Request Block Count sent to {peer.getpeername()}")

    def sendBlocksRequest(self, height_list, peerSocket=None):
        # This function is used to send a Request Block packet, which request for a singular block, the receiver should
        # either send the raw block or False.
        for height in height_list:

            message = f"RB:{height-1}"
            message = message.encode('utf-8')

            # If a peer is not specified we send the request to all connected peers.
            if peerSocket is None:
                for peer in self.peers:
                    peer.sendall(message)
                    print(f"<BLOCK REQUEST> Requesting Block {height} from {peer.getpeername()}")
            else:
                try:
                    peerSocket.sendall(message)
                    print(f"<BLOCK REQUEST> Requesting Block {height} from {peerSocket.getpeername()} only!")
                except:
                    print(f"<BLOCK REQUEST> Peer specified is invalid.")

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
        # This function will validate a transaction when we receive it, and this determines if the transactions reach
        # our mempool, to be mined.
        # Update: Transactions have to be checked that no two transactions have the same input and same vout. This
        # easily prevents double spending, we also need to check that this transaction is not a used as an input for
        # transactions in the mempool
        total_value = 0

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

                # This checks each transaction in the blockchain to see if the same txid and vout is already mentioned
                for block in self.blockchain.blocks:
                    for tx in block.transactions:
                        decodedtx = rawtxdecoder.decodeRawTx(tx.raw)
                        inputs = int(decodedtx["InputCount"])
                        for z in range(inputs):
                            if decodedtx[f"txid{z}"] == txid and int(decodedtx[f"vout{z}"], 16) == vout:
                                return False

                # This checks if the transactions txid and vout is already in the mempool
                for tx in self.mempool:
                    decodedtx = rawtxdecoder.decodeRawTx(tx.raw)
                    inputs = int(decodedtx["InputCount"])
                    for z in range(inputs):
                        if decodedtx[f"txid{z}"] == txid and int(decodedtx[f"vout{z}"], 16) == vout:
                            return False

                # We find the transaction that is used for an input and take the scriptPubKey
                previousTransaction = self.blockchain.findTxid(txid)
                previousTransactionDict = rawtxdecoder.decodeRawTx(previousTransaction)

                # Finding the values of the previous transaction totalled
                previous_value = previousTransactionDict[f"value{vout}"]
                previous_value = int(previous_value, 16)
                total_value += previous_value

                # This picks the specific locking script that the vout refers to
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

        print(transaction)
        transaction_value = transaction.findTotalValueSent()
        if transaction_value > total_value:
            print(f"<TX VALIDATE> Transaction is invalid.")
            return False

        print(f"<TX VALIDATE> Transaction is valid!")
        return True

    def validateBlockDifficulty(self, block):
        # This is used to validate that a given block has the correct difficulty, and thus validating it again.
        # This returns true if valid and false if invalid.

        calculatedDifficulty = self.blockchain.calculateDifficulty()
        if block.difficulty == calculatedDifficulty:
            print(f"<VALIDATE DIFFICULTY> Difficulty is validated.")
            return True
        else:
            print(f"<VALIDATE DIFFICULTY> Difficulty is invalid.")
            return False

    def sendPingTCP(self, ip):
        # This function only serves to test that a communication is alive, by sending a ping request, if a ping request
        # is received and a host is alive it will send a pong, as a confirmation.

        ipsocket = self.checkIPisPeer(ip)
        if ipsocket is not False:
            message = "ping"
            message = message.encode('utf-8')
            ipsocket.send(message)

    def sendPingUDP(self, ip):
        # This function is used to send a ping to the UDP server socket, this way we can establish if a client/host is
        # alive.
        message = "ping"
        message = message.encode('utf-8')
        self.UDPsocket.sendto(message, (ip, SERVER_UDP_SERVER))

    def startMine(self):
        # This function will continuously mine blocks in the mempool, this works even if there are no transactions it
        # will continue mine. This function is also responsible to update the difficulty and add to the blockchain. Gas
        # fees will be calculated as the discrepancy for the total sent to the total input in, and this will be added
        # onto the reward: this seems too hard as
        while True:

            if self.mining is False:
                break

            # So as the difficulty is calculated based on the time difference between of the last two blocks, we need
            # to hard set the difficulty and the previous block id.
            if self.blockchain.height == -1 or self.blockchain.height == 0:
                current_height = self.blockchain.height + 1
                current_difficulty = 13560704084551531344379931619614108352879381342049336509327224628459529

                try:
                    previous_block_hash = self.blockchain.blocks[-1].blockid
                except IndexError:
                    previous_block_hash = "7cb95d760cbecec3e8f537d55a307ba8e5598ecce09ece40fcffc50ca7028735"#Hash of pycharm

                self.blockchain.difficulty = current_difficulty

            else:
                current_height = self.blockchain.height + 1
                current_difficulty = self.blockchain.calculateDifficulty()
                previous_block_hash = self.blockchain.blocks[-1].blockid
                self.blockchain.difficulty = current_difficulty

            current_transactions = []
            total_in = 0
            total_output = 0

            # Here we add all the transactions in the mempool if the mempool isn't empty.
            if self.mempool is not []:
                for transaction in self.mempool:
                    current_transactions.append(transaction)

                    # Here we will calculate the total input to the total output and whatever discrepancy there is we
                    # will use this as an additional fee for the miners.

                    for i in range(int(transaction['InputCount'])):
                        txid = transaction[f'txid{0}']
                        vout = transaction[f'vout{0}']
                        previous_transaction_raw = self.blockchain.findTxid(txid)
                        previous_transaction_dict = rawtxdecoder.decodeRawTx(previous_transaction_raw)
                        total_in += previous_transaction_dict[f'value{int(vout, 16)}']

                    # We also need to calculate total value of the outputs
                    for i in range(int(transaction['OutputCount'])):
                        total_output += transaction[f'value{i}']

                fee = total_in - total_output

            else:
                fee = 0

            # We mine construct and mine our new block
            print(f"CurrentHeight = {current_height}")
            print(f"CurrentDifficulty = {current_difficulty}")
            print(f"prevBlockId = {previous_block_hash}")
            self.miningBlock = Block(self.blockchainfile, current_height, current_transactions, current_difficulty, previous_block_hash)
            self.miningBlock.mine(self.publickey, fee)

            # Check if any blocks have been recently mined by anyone else before our block has been mined.
            recentlyMinedBlock = False
            for block in self.recentlyAddedBlocks:
                if self.miningBlock.height == block.height:
                    # A block has been mined before ours, so we don't keep our block we just mined.
                    recentlyMinedBlock = True
                    self.recentlyAddedBlocks.remove(block)

            if recentlyMinedBlock:
                print(f"Disregarding mined block")
                continue
            else:
                # After successfully mining we need to add the blocks to our blockchain and increment our
                # blockchains height
                self.miningBlock.addBlockToChain()
                self.blockchain.blocks.append(self.miningBlock)
                self.blockchain.height += 1
                self.sendBlock(current_height)
                print(f"<MINER> Block {current_height} has been successfully mined!")
def main():

    p1 = Peer("blockchains/testchain.txt", "192.168.0.111", 50000, 50500, 10, 8888)

    for block in p1.blockchain.blocks:
        print(block.height)

if __name__ == "__main__":
    main()
