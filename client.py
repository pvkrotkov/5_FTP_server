import socket
import threading

sock = socket.socket()

def connect_to_server(sock):
    while True:
        try:
            port = int(input('Write the port: '))
            # break
        except ValueError:
            print('>You entered somethings wrong. Try again ')
            continue
        try:
            sock.connect(('127.0.0.1', port))
            print("Connected!")
            break
        except OSError:
            print('Oops, we cant find this port\nTry again')


def sign_in(sock):
    while True:
        password = input()
        sock.send(password.encode())
        message = sock.recv(1024).decode()
        print(message)
        if 'Welcome' in message:
            break

def sign_up(sock):
    global login
    while True:
        login = input('Write your login: ')
        password = input('Write your password: ')
        if login == '' or password == '':
            print('>You entered somethings wrong. Try again ')
            continue
        sock.send(login.encode())
        sock.send(password.encode())
        message = sock.recv(1024).decode()
        print(message)
        if 'login' in message:
            continue
        elif 'welcome' in message:
            break

def listening(sock):
    while True:
        message = sock.recv(1024).decode()
        print(message)
        print('\r\r'+f'>{message}'+'\n'+f'{login}${login}: ', end='')


def auth(sock):
    message = sock.recv(1024).decode()
    print(message)
    if 'enter' in message:
        sign_in(sock)
    elif 'sign up' in message:
        sign_up(sock)

    threading.Thread(target=listening, args=(sock,), daemon=True).start()
    while True:
        requeset = input()
        sock.send(requeset.encode())


def main():
    connect_to_server(sock)
    auth(sock)

if __name__ == "__main__":
    main()