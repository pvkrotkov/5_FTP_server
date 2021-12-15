import socket
PORT = 80
HOST = 'localhost'

def main():
    print(f"Присоединились к {HOST} {PORT}")
    while True:
        req = input('alexa@alexa$')
        if req == 'quit':
            break
        with socket.socket() as sock:
            sock.connect((HOST, PORT))

            sock.send(req.encode())
            response = sock.recv(1024).decode()
            if response:
                print(response)


if __name__ == '__main__':
    main()