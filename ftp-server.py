import socket
import os
import shutil
from pathlib import Path


dirname = Path(Path.cwd())  # Метод Path.cwd() вернет новый объект пути path, представляющий текущий каталог

PORT = 8080
sock = socket.socket()
sock.bind(('', PORT))
sock.listen()


# Посмотреть содержимое папки
def ls():
    return '\n'.join(os.listdir(dirname))


# Создать папку
def mkdir(name):
    path = Path(name)
    if path.is_dir():
        shutil.rmtree(path)
    path.mkdir(parents=True)


# Создать файл
def touch(name, text=''):
    path = Path(name)
    path.touch()
    path.write_text(text)


# Удалить папку/файл
def rm(name):
    path = Path(name)
    if path.is_file():
        path.unlink()  # Метод Path.unlink() удаляет файл или символическую ссылку, указанную в пути path
    elif path.is_dir():
        shutil.rmtree(path)  # Функция rmtree() модуля shutil рекурсивно удаляет все дерево каталогов по указанному пути


# Переименовать файл
def rename(name1, name2):
    path = Path(name1)
    if path.exists():
        shutil.move(name1, name2)
    else:
        print('Error')


# Определить текущий путь
def pwd():
    return str(dirname)


# Прочитать содержимое файла
def cat(name):
    path = Path(name)
    if path.is_file():
        return path.read_text()
    else:
        print('Error')


# Копирование
def copying(name, way):
    path = Path(pwd())
    if path.exists():
        shutil.copy(name, way)
    else:
        print('Error')


# Функция вывода справочника
def help_():
    return(
        'ls <dir>            - посмотреть содержимое папки\n'
        'mkdir <dir>         - создать папку\n'
        'touch <file> <text> - создать файл\n'
        'rm <file/dir>       - удалить файл/папку\n'
        'rename <old> <new>  - переименовать файл\n'
        'cat <file>          - посмотреть содержимое файла\n'
        'copy <file> <dir>   - копировать файл\n'
        'pwd                 - текущий путь\n'
        'help                - выводит справку по командам\n'
        'exit                - выход\n'
    )


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
    elif command == 'rename':
        return rename(req.split()[1], req.split()[2])
    elif command == 'copy':
        return copying(req.split()[1], req.split()[2])
    elif command == 'help':
        return help_()
    else:
        print('Error')



while True:
    conn, addr = sock.accept()
    os.chdir(dirname)
    req = conn.recv(1024).decode()
    print(req)
    response = process(req)
    if response is None:
        conn.send('Done'.encode())
    else:
        conn.send(response.encode())

conn.close()
