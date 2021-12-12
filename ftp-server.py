import socket
import os
import shutil
from pathlib import Path


dirname = Path(Path.cwd(), 'docs')


def ls():
    return '; '.join(os.listdir(dirname))


def pwd():
    return str(dirname)


def rm(name):
    path = Path(name)
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def mkdir(name):
    path = Path(name)
    if path.is_dir():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def touch(name, text=''):
    path = Path(name)
    path.touch()
    path.write_text(text)


def cat(name):
    path = Path(name)
    if path.is_file():
        return path.read_text()
    return 'Вы ввели некорректный файл'


def mv(name, destination):
    path = Path(name)
    if path.exists():
        shutil.move(name, destination)


def help_():
    text_help = [
        'ls [DIRECTORY]- выводит содержимое каталога',
        'pwd - выводит путь текущего каталога',
        'mkdir DIRECTORY - создает каталог',
        'touch FILE [TEXT] - создает пустой файл или файл с текстом',
        'rm FILE - удаляет файл',
        'mv SOURCE DESTINATION - перемещает (переименовывает файл)',
        'cat FILE - выводит содержимое файла',
        'help - выводит справку по командам',
        'exit - разрыв соединения с сервером'
        ]
    return '\n'.join(text_help)


def process(req):
    command = req.split()[0]
    if command == 'pwd':
        return pwd()
    elif command == 'ls':
        return ls()
    elif command == 'rm':
        return rm(req.split()[1])
    elif command == 'mkdir':
        return mkdir(req.split()[1])
    elif command == 'touch':
        if len(req.split()) > 2:
            return touch(req.split()[1], ' '.join(req.split()[2:]))
        return touch(req.split()[1])
    elif command == 'cat':
        return cat(req.split()[1])
    elif command == 'mv':
        return mv(req.split()[1], req.split()[2])
    elif command == 'help':
        return help_()
    return 'bad request'


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    os.chdir(dirname)
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    if response is None: 
        conn.send('Выполнено!'.encode())
    else:  
        conn.send(response.encode())

conn.close()
