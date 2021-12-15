import socket

HOST = 'localhost'
PORT = 6666

    
sock = socket.socket()
sock.connect((HOST, PORT))
print(sock.recv(1024).decode())
login = input('>')
sock.send(login.encode())
print(sock.recv(1024).decode())
password = input('>')
sock.send(password.encode())
print(sock.recv(1024).decode())

while True:
    request = input('>')
    sock.send(request.encode())
    if request == 'exit':
        sock.close()
        break
    
    response = sock.recv(1024).decode()
    print(response)
