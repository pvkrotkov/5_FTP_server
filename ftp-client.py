import socket

HOST = 'localhost'
PORT = 6666

cmd_cnt = 0
while True:
    if not cmd_cnt:
        print('\nВыполнен переход в рабочую папку.')
        print('Для получения справки по менеджеру введите help.\n')
    request = input('>')

    sock = socket.socket()
    sock.connect((HOST, PORT))

    sock.send(request.encode())

    response = sock.recv(8192).decode()
    cmd_cnt += 1
    if response == '0':
        print('Выход из файлового менеджера...')
        break

    print(response)
    sock.close()
