import socket
import os
import shutil

def size(name):
    path = os.getcwd() + f'/{name}'
    result = 0
    for directory, subdirectory, files in os.walk(path):
        if files:
            for file in files:
                path = directory + f'{file}'
                result += os.path.getsize(path)
    return result


def pwd():
    if name == 'admin':
        return os.getcwd()
    return os.getcwd()[len_home:]


def ls():
    return ' '.join(os.listdir(os.getcwd()))


def cat(name):
    with open(name, 'r') as file:
        return file.read()


def mkdir(name):
    path = os.getcwd() + '/' + name
    os.mkdir(path)
    return f'папка {name} успешно создана'


def rmdir(name):
    path = os.getcwd() + '/' + name
    shutil.rmtree(path)
    return f'папка {name} успешно удалена'


def rm(name):
    path = os.getcwd() + '/' + name
    os.remove(path)
    return f'файл {name} успешно удалён'


def touch(name):
    with open(name, 'w') as file:
        pass
    return f'файл {name} успешно создан'


def cd(path):
    if path == '..':
        if os.getcwd() == home_directory:
            return 'Вы в корневой директории'
        directory = '/'.join(os.getcwd().split('/')[:-1])
    else:
        directory = '/'.join(os.getcwd().split('/')) + '/' + path
    os.chdir(directory)
    return f'Текущая директория {pwd()}'


def rename(name1, name2):
    os.rename(name1, name2)
    return f'файл {name1} успешно переименнован в {name2}'


def send(name, conn, userr):
    length = conn.recv(1024).decode()
    text = conn.recv(int(length)).decode()
    with open(name, 'w') as file:
        file.write(text)
    if userr != 'admin':
        if size(userr) > max_size:
            rm(name)
            return 'Недостаточно места на диске'
    return f'получен файл {name}'


def recv(name, conn):
    with open(name, 'r') as file:
        text = file.read()
    conn.send(str(len(text)).encode())
    conn.send(text.encode())
    return f'отправлен файл {name}'


def new_user(conn, user):
    name = conn.recv(1024).decode()
    if name not in user.keys():
        conn.send('1'.encode())
        password = conn.recv(1024).decode()
        user[name] = user.get(name, password)
        file = home + '/users.txt'
        with open(file, 'w') as users:
            print(user, file=users)
        mkdir(name)
        return name
    else:
        conn.send('0'.encode())
        flag2 = conn.recv(1024).decode()
        if int(flag2):
            # может возвращаться пустое имя
            name = old_user(conn, user)
            return name
        else:
            name = new_user(conn, user)
            return name


def old_user(conn, users):
    name = conn.recv(1024).decode()
    if name in users.keys():
        conn.send('1'.encode())
        passwd = users[name]
        while True:
            password = conn.recv(1024).decode()
            if passwd == password:
                conn.send('0'.encode())
                return name
            else:
                conn.send('1'.encode())
    else:
        conn.send('0'.encode())
        flag2 = conn.recv(1024).decode()
        if int(flag2):
            name = new_user(conn, users)
            return name
        else:
            name = old_user(conn, users)
            return name

def process(req, args=None):
    try:
        f = commands[req]
    except KeyError:
        return f"Команда {req} отсутствует"
    if args:
        return f(*args)
    return f()

commands = {'pwd': pwd, 'ls': ls, 'mkdir': mkdir, 'rmdir': rmdir, 'rm': rm, 'touch': touch, 'rename': rename,
            'send': send, 'recv': recv, 'cat': cat, 'cd': cd}

PORT = 9090

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()

home = os.getcwd()
len_home = len(home)
log = home + '/log.txt'
max_size = 500

with open(log, 'a', encoding="UTF-8") as logs:
    print(f"Слушаем порт {PORT}", file=logs)

user = {'admin': 'root'}
try:
    with open('users.txt', 'r') as users:
        user = eval(users.read())
except FileNotFoundError:
    with open('users.txt', 'w') as users:
        pass
except SyntaxError:
    pass

while True:
    home_directory = home
    conn, addr = sock.accept()
    with open(log, 'a', encoding="UTF-8") as logs:
        print(f"Подключился {addr}", file=logs)

    flag = int(conn.recv(1).decode())
    if flag:
        name = new_user(conn, user)
        with open(log, 'a', encoding="UTF-8") as logs:
            print(f"Зарегистрировался пользователь {name}", file=logs)
    else:
        name = old_user(conn, user)
        with open(log, 'a', encoding="UTF-8") as logs:
            print(f"Вошёл пользователь {name}", file=logs)

    conn.send(f"Hello, {name}".encode())

    if name != "admin":

        home_directory += f'/{name}'
        os.mkdir(home_directory)
    path = '/'.join(home_directory.split('/'))
    os.chdir(path)

    while True:
        request = conn.recv(1024).decode()
        request = request.split()
        if not request:
            break
        func = request[0]
        if len(request) > 0:
            args = request[1:]
        else:
            args = None
        if args:
            if func in ['send', 'recv']:
                args.append(conn)
                if func == 'send':
                    args.append(name)
            response = process(func, args)
        else:
            response = process(func)
        with open(log, 'a', encoding="UTF-8") as logs:
            print(f"Запрос {func} от пользователя {name}", file=logs)
        conn.send(response.encode())
    conn.close()

sock.close()