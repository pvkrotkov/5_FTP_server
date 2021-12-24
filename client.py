import socket

PORT = 9090


def _main():
    print('Чтобы посмотреть список доступных команд, введите help')
    while True:
        request = input('$ ')
        if request == 'exit':
            break
        with socket.socket() as sock:
            sock.connect(('localhost', PORT))
            sock.send(request.encode())
            response = sock.recv(1024).decode()
            if response:
                print(response)


if __name__ == '__main__':
    _main()