import socket

HOST = 'localhost'
PORT = 9090

print('введите "help", чтобы увидеть справку по командам')
def _main():
    while True:
        request = input('$ ')
        if request == 'exit':
            break
        with socket.socket() as sock:
            sock.connect((HOST, PORT))
            sock.send(request.encode())
            response = sock.recv(1024).decode()
            if response:
                print(response)


if __name__ == '__main__':
    _main()
