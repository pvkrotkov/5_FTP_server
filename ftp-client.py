import socket

HOST = 'localhost'
PORT = 6666

while True:
    try:
        request = input('>')
    except Exception:
        break
    sock = socket.socket()
    try:
        sock.connect((HOST, PORT))
    except Exception:
        break
    sock.send(request.encode())
    try:
        response = sock.recv(1024).decode()
    except Exception:
        break
    if response == 'exit' or response == 'break':
        break
    print(response)

    sock.close()