import socket


def send_file(name, sock):
    sock.send(f'send {name}'.encode())
    with open(name, 'r') as file:
        text = file.read()
    sock.send(str(len(text)).encode())
    sock.send(text.encode())
    return


def new_user(name, sock):
    sock.send(name.encode())
    flag = sock.recv(1024).decode()
    if int(flag):
        password = '12345'
        sock.send(password.encode())
    else:
        flag2 = 1
        sock.send(str(flag2).encode())
        old_user(name, sock)


def old_user(name, sock):
    sock.send(name.encode())
    # Если 1 - имя есть, если 0 - это имя ещё не зарегестрированно
    flag = sock.recv(1024).decode()
    if int(flag):
        password = '12345'
        sock.send(password.encode())
        flag = sock.recv(1024).decode()


def login(sock):
    sock.send('1'.encode())
    new_user('Test', sock)


def testing():
    HOST = '127.0.0.1'
    PORT = 9090

    sock = socket.socket()
    sock.connect((HOST, PORT))
    print(f"Подключение к {HOST} {PORT}")

    login(sock)
    data = (sock.recv(1024).decode())
    if data != 'test':
        return "Ошибка в создании нового пользователя"

    # pwd
    request = 'pwd'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "/test":
        return "Ошибка в pwd"

    # mkdir
    request = 'mkdir test'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "папка test успешно создана":
        return "Ошибка в mkdir"

    # ls
    request = 'ls'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "test":
        return "Ошибка в ls"

    # cd
    request = 'cd test'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "Текущая директория /test/test":
        return "Ошибка в cd"
    request = 'pwd'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "/test/test":
        return "Ошибка в cd"

    # send
    request = 'send main.txt'
    send_file(request.split()[1], sock)
    answer = sock.recv(1024).decode()
    if answer != "получен файл main.txt":
        return "Ошибка в send"

    # size
    request = 'send main2.txt'
    send_file(request.split()[1], sock)
    answer = sock.recv(1024).decode()
    if answer != "Недостаточно места на диске":
        return "Ошибка в выделении места на диске"

    # cd ..
    request = 'cd ..'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "Текущая директория /test":
        print(answer)
        return "Ошибка в cd.."

    # rmdir
    request = 'rmdir test'
    sock.send(request.encode())
    answer = sock.recv(1024).decode()
    if answer != "папка test успешно удалена":
        return "Ошибка в rmdir"

    # exit
    sock.close()
    return "Пока!"


print(testing())