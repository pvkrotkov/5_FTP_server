import socket

HOST = 'localhost'
PORT = 6666
print('Введите help чтобы увидеть список команд')
while True:
    request = input('Введите команду:')
    if request == 'exit':
        break
    with socket.socket() as sock:
        sock.connect((HOST, PORT))
        sock.send(request.encode())
        response = sock.recv(1024).decode()
        if response:
            print(response)
