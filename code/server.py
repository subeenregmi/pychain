import socket

s = socket.socket()

print("Socket Created")

s.bind(("localhost", 9999))

s.listen(3)
print("Waiting for connections")

while True:

    c, addr = s.accept()
     
    name = c.recv(1024).decode()

    print(f"Connected with {addr}, {name}")

    c.send(bytes(f"Welcome {name}!", "utf-8"))

    c.close()