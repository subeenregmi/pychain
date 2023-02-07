import socket

client_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("> ")
    client_UDP.sendto(message.encode('utf-8'), ("10.154.0.2", 60002))
