import socket
port = 9090
def ftp_start():
    print('Чтобы вызвать справку, введите команду write_help')
    while True:
        request = input('~ ')
        if request == 'exit': #выход по запросу пользователя
            break
        with socket.socket() as sock:
            sock.connect(('localhost', port))
            sock.send(request.encode())  #отправляем на сервер команду
            response = sock.recv(1024).decode()
            if response:
                print(response)
print(ftp_start())