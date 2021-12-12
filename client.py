import socket


def main():
    sock = socket.socket()
    sock.connect(('127.0.0.1', 9091))

    while True:
        got = sock.recv(1024*8).decode()
        print(got, end="")
        if "Вы вошли" in got:
            break
        print()
        sent = input('>')
        sock.send(sent.encode())

    while True:
        sent = input()
        sock.send(sent.encode())

        if sent == "exit":
            break

        got = sock.recv(1024*8).decode()
        print(got, end="")

        got = sock.recv(1024*8).decode()
        print(got, end="")
    sock.close()


if __name__ == '__main__':
    main()
