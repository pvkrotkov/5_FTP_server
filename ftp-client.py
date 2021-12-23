import socket

HOST = 'localhost'
PORT = 9109

def main():
    print(f"Подключение к {HOST} {PORT}")
    print('help - список команд, exit - выход')
    while True:
        request = input('>')
        if request == 'exit':
            break
        with socket.socket() as sock:
            sock.connect((HOST, PORT))

            sock.send(request.encode())
            response = sock.recv(1024).decode()
            if response:
                print('response:',response)


if __name__ == '__main__':
    main() 
