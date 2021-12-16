import socket
import shutil
import os
from pathlib import Path
PORT = 8083
HOME = Path(Path.cwd(), 'home dir')

#выводит содержимое каталога
def ls(path=None):
    if path:
        return '; '.join(os.listdir(path))
    return '; '.join(os.listdir(HOME))

#выводит путь текущего каталога
def pwd():
    return str(HOME)

#создает каталог
def mkdir(path):
    path = Path(path)
    rm(path)
    path.mkdir(parents=True)

#создает пустой файл или файл с текстом
def touch(path, text=''):
    path = Path(path)
    path.touch()
    path.write_text(text)

#удаляет файл
def rm(path):
    path = Path(path)
    if path.is_dir():
        shutil.rmtree(path)
    elif path.is_file():
        path.unlink()

def mv(src_path, dst_path):
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    if src_path.exists():
        shutil.move(src_path, dst_path)

def cat(path):
    path = Path(path)
    if path.is_file():
        return path.read_text()

def help():
    return 'ls (название директории)- выводит содержимое каталога\n' \
           'pwd - выводит путь текущего каталога\n' \
           'mkdir (название директории) - создает каталог\n' \
           'touch (название файла) (текст) - создает пустой файл или файл с текстом\n' \
           'rm (название файла) - удаляет файл\n' \
           'mv (название файла) (название директории или файла) - перемещает (переименовывает файл)\n' \
           'cat (название файла) - выводит содержимое файла\n' \
           'help - выводит справку по командам\n' \
           'exit - разрыв соединения с сервером'

def process(request):
    command, *args = request.split()
    commands = {
        'ls': ls,
        'pwd': pwd,
        'mkdir': mkdir,
        'touch': touch,
        'rm': rm,
        'mv': mv,
        'cat': cat,
        'help': help
    }
    try:
        return commands[command](*args)
    except (TypeError, KeyError):
        return 'Неверный ввод'

def handle(conn):
    with conn:
        request = conn.recv(1024).decode()
        print(request)
        response = process(request)
        if response is None:
            response = ''
        conn.send(response.encode())

def func2():
    if not HOME.is_dir():
        mkdir(HOME)
    os.chdir(HOME)
    with socket.socket() as sock:
        sock.bind(('', PORT))
        sock.listen()
        print("Слушаем порт", PORT)

        while True:
            conn, addr = sock.accept()
            handle(conn)

print(func2())
