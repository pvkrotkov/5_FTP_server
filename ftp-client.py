# Импортировать пакет сокета
import socket, shutil, os, sys

HOST = ''
PORT = 9090

def start_client():
    while True:
        data = input('>')
        if data == 'exit':
            print('Клиент закрыт')
            break
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            sock.send(data.encode())

            resp = sock.recv(1024).decode()
            print(resp)

            sock.close()

if __name__=='__main__':
    #home = input('Необходимо установить сначала домашнюю папку (DIR/default) ')
    start_client()


