import socket

def createClient(port):
    client_socket = socket.socket()
    client_socket.bind(("localhost", port))
    client_socket.send(("localhost", 55558))
def sendMessage():
    pass

