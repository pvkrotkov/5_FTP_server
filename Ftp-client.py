import socket


ip = 'localhost'
PORT = 1111


print('Для того, чтобы узнать список доступных команд введите help')


while True:
    request = input('Ваша команда: ')
    if request == 'exit':
        break
    with socket.socket() as sock:
        sock.connect((ip, PORT))
        sock.send(request.encode())
        response = sock.recv(1024).decode()
        if response:
            print(response)
