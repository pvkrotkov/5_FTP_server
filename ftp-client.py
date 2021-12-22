import socket

HOST = "127.0.0.1"
PORT = 8080

while True:
    req = input('> ')
    if req == 'exit':
        break
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(req.encode())
    response = sock.recv(1024).decode()
    print(response)
    sock.close()
