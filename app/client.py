import socket
from time import sleep
import os
import time

def c_register():
    print('Регистрация.')
    login = input('Введите логин: ')
    sock.send(login.encode())
    passw = input('Введите пароль: ')
    sock.send(passw.encode())
    data = sock.recv(1024)
    if 'успешно' in data.decode():
        print('Успешная регистрация!')
        main()
    elif 'занято' in data.decode():
        print('Логин занят. Выберите другой.')
    else:
        print('Что-то пошло не так.')

def c_login():
    print('Авторизация.')
    login = input('Введите логин: ')
    sock.send(login.encode())
    passw = input('Введите пароль: ')
    sock.send(passw.encode())
    data = sock.recv(1024)
    if 'успешно' in data.decode():
        print('Успешная авторизация!')
        main()
    elif 'неправильные данные' in data.decode():
        print('Неверные логин или пароль.')
    else:
        print('Что-то пошло не так.')

def sendfile():
    data = sock.recv(1024)
    filename = data.decode()
    filesize = str(os.path.getsize(filename))
    sock.send(filesize.encode())
    time.sleep(1)
    data = ''
    with open(filename, 'r') as f:
        for line in f:
            data += line
    sock.send(data.encode())
    data = sock.recv(1024)
    print(data.decode())

def receivefile():
    data = sock.recv(1024)
    filename = data.decode()
    data = sock.recv(1024)
    filesize = data.decode()
    data = sock.recv(int(filesize))
    with open(filename, 'w') as f:
        f.write(data.decode())
    print(f'Файл {filename} успешно получен.')

def main():
    data = sock.recv(2048)
    print(data.decode(), end = '\n\n')
    connected = True
    while connected:
        data = sock.recv(1024)
        current_path = data.decode().split('|||')
        command = input(f'FileManager:{current_path[1]}$ ')
        if len(command) == 0:
            sock.send('<empty>'.encode())
            continue
        sock.send(command.encode())
        data = sock.recv(1024)
        if 'exit' in command or 'close' in command:
            quit()
        elif data.decode() == 'ke':
            print('Неправильная команда. Команды можно посмотреть, написав "help".')
        elif data.decode() == 'te':
            print('Неправильный формат ввода.')
        elif data.decode() == 'send':
            sendfile()
        elif data.decode() == 'receive':
            receivefile()
        else:
            print(data.decode())
        print()


if __name__ == '__main__':
    sock = socket.socket()
    sock.setblocking(1)

    #ip = input('Введите имя хоста (IP-adress): ')
    #port = input('Введите порт: ')
    ip = '192.168.1.2'
    port = 9090

    print('Соединение с сервером...')
    sock.connect((ip, int(port)))

    data = sock.recv(1024)
    s = input(data.decode()+' ')
    if 'рег' in s.lower() or 'reg' in s.lower():
        sock.send('r'.encode())
        c_register()
    else:
        sock.send('l'.encode())
        c_login()

    print('Разрыв соединения с сервером...')
    sock.close()

    input()