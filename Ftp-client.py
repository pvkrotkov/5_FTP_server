import socket

HOST = "127.0.0.1"
PORT = 8090

while True:
    req = input('>>> ')
    if req == 'exit':
        sock = socket.socket()
        sock.connect((HOST, PORT))
        sock.send("exit".encode())
        sock.close()
        break
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(req.encode())
    response = sock.recv(1024).decode()
    print(response)
    sock.close()