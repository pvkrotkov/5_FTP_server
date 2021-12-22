import socket
import os
import shutil
from pathlib import Path
PORT = 8080
sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
dirname = Path(Path.cwd())
def pwd():
    return str(dirname)
def ls(name=dirname):
    return '\n'.join(os.listdir(name))
def mkdir(name):
    path = pwd() + '/' + name
    os.mkdir(path)
    return f'папка {name} успешно создана'
def touch(name):
    path = Path(name)
    path.touch()
    return 'Файл создан'
def rm(name):
    path = Path(name)
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
    return 'Удалено'
def rename(name1, name2):
    path = Path(name1)
    if path.exists():
        shutil.move(name1, name2)
        return 'Переименован'
    else:
        return 'Ошибка'
def cat(name):
    path = Path(name)
    if path.is_file():
        return path.read_text()
    else:
        return 'Ошибка'
def copy(name, way):
    path = Path(pwd())
    if path.exists():
        shutil.copy(name, way)
        return 'Копирование сделано'
        
    else:
        return 'Ошибка'
def help_com():
    return (
        'ls <dir>            - посмотреть содержимое папки\n'
        'mkdir <dir>         - создать папку\n'
        'touch <file>        - создать файл\n'
        'rm <file/dir>       - удалить файл/папку\n'
        'rename <old> <new>  - переименовать файл\n'
        'cat <file>          - посмотреть содержимое файла\n'
        'copy <file> <dir>   - копировать файл\n'
        'pwd                 - текущий путь\n'
        'help_com            - выводит справку по командам\n'
        'exit                - выход\n'
    )
def process(req):
    command = req.split()[0]
    if command == 'pwd':
        return pwd()
    elif command == 'ls':
        a=req.split()
        if (len(a)>1):
            return ls(req.split()[1])
        else:
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
    elif command == 'rename':
        return rename(req.split()[1], req.split()[2])
    elif command == 'copy':
        return copy(req.split()[1], req.split()[2])
    elif command == 'help_com':
        return help_com()
    else:
        return 'Error'
print(f'Просулшиваем порт {PORT}')
while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    print(request)
    response = process(request)
    conn.send(response.encode())
conn.close()
