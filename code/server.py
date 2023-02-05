import socket
import threading

clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("localhost", 55558))

server_socket.listen(3)


def handleClient():
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print(f"{client_address} has joined!")
        thread = threading.Thread(target=recieveMessage(client_socket))
        thread.start()
        thread.join()
        if len(clients) == 0:
            break
def recieveMessage(socket):
    while True:
        data = socket.recv(1024).decode('utf-8')
        for client in clients:
            if client == socket:
                continue
            socket.send(data.encode('utf-8'))
        if data == "":
            clients.remove(socket)
            break

def main():
    thread1 = threading.Thread(target=handleClient())
    thread1.start()
    thread1.join()

main()