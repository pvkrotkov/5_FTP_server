import socket
import time


def sign_in():
    sock = socket.socket()
    sock.connect(("127.0.0.1", 9091))
    sock.recv(1024 * 16)
    sock.send("test".encode())
    sock.recv(1024 * 16)
    sock.send("qwerty123".encode())
    sock.recv(1024 * 16)
    main(sock)


def main(sock):
    tests = [("pwd", "\\"),
             ("ls", ""),
             ("mkdir 1", ""),
             ("touch 1", ""),
             ("mv 1.txt 1", ""),
             ("touch 1", ""),
             ("rm 1.txt", ""),
             ("cd 1", ""),
             ("mv 1.txt 2.txt", ""),
             ("write 2.txt qwerty", ""),
             ("cat 2.txt", "qwerty")]
    for index, test in enumerate(tests):
        request = test[0]
        sock.send(request.encode())
        time.sleep(0.1)
        res = sock.recv(1024).decode()
        response = "\n".join(res.split("\n")[:-1])
        print("•" * 50)
        print(f"Тест номер {index + 1}")
        print(f"Введенная команда: {test[0]}")
        print(f"Результат, который мы получили: {response}")
        print(f"Результат, который мы ожидали: {test[1]}")
        print(f"Тест {'' if response == test[1] else 'не'}корректный")
        print("•" * 50 + "\n")


if __name__ == '__main__':
    sign_in()
