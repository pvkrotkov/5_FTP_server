import socket
from os.path import getsize


def authorization():
    login = input("Введите логин")
    password = input("Введите пароль")
    sock.send((login+"\n"+password).encode())
    response = sock.recv(1024)
    return response != "AUTHORIZATION_ERROR"
    


HOST = 'localhost'
PORT = 6666

while True:
    request = input('>')

    sock = socket.socket()
    sock.connect((HOST, PORT))
    if request[:6] != "upload":
        sock.send((request).encode())
    else:
        sock.send((request+"\n").encode())
    if request[:8] == "download":
        content = sock.recv(1024)
        with open(request[9:], "wb") as file:
            file.write(content)
    if request[:6] == "upload":
        with open(request[7:], "rb") as file:
            content = file.read(1024)
            sock.send(content)
    if request == "mkuser":
        login = input("Введите логин")
        password = input("Введите пароль")
        sock.send(login+"\n"+password)
    response = sock.recv(1024).decode()
    print(response)
    if response == "Работа завершена":
        break
sock.close()
