import socket

HOST = 'localhost'
PORT = 1899

try:
    os.system('clear')
    os.system('cls')
except:
    pass

while True:
    request = input('>')
    if request == 'exit':
	    print('Клиент закрыт')
	    break
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())
    response = sock.recv(1024).decode()
    print(response)
    sock.close()
