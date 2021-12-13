import socket
import shutil
import os
from pathlib import Path
PORT = 8083
HOME = Path(Path.cwd(), 'home')

def ls(path=None):
    if path:
        return '; '.join(os.listdir(path)) #список файлов и директорий в папке HOME
    return '; '.join(os.listdir(HOME))

def pwd():
    return str(HOME) #отображает текущую директорию

def mkdir(path):
    path = Path(path)
    rm(path)
    path.mkdir(parents=True) #создаём директорию

def touch(path, text=''):
    path = Path(path)
    path.touch()
    path.write_text(text)  #создаем текстовый файл

def rm(path):
    path = Path(path)
    if path.is_dir():
        shutil.rmtree(path) #удаляем текущую директорию и все поддиректории
    elif path.is_file():
        path.unlink() #удаляем файл

def mv(src_path, dst_path):
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    if src_path.exists():
        shutil.move(str(src_path), str(dst_path)) #рекурсивно перемещаем файл
    else:
        shutil.move(str(dst_path), str(src_path))

def cat(path):
    path = Path(path)
    if path.is_file():
        return path.read_text()  #вовзращаем содержимое файла в виде строки

def help(): #выводим доступные команды
    return 'ls [DIRECTORY]- выводит содержимое каталога\n' \
           'pwd - выводит путь текущего каталога\n' \
           'mkdir DIRECTORY - создает каталог\n' \
           'touch FILE [TEXT] - создает пустой файл или файл с текстом\n' \
           'rm FILE - удаляет файл\n' \
           'mv SOURCE DESTINATION - перемещает (переименовывает файл)\n' \
           'cat FILE - выводит содержимое файла\n' \
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
        'help': help #присваиваем командам функции
    }
    try:
        return commands[command](*args)
    except (TypeError, KeyError):
        return 'Bad request'

def handle(conn):
    with conn:
        request = conn.recv(1024).decode() #принимаем команду
        print(request)
        response = process(request)
        if response is None:
            response = ''
        conn.send(response.encode())

def func2():
    if not HOME.is_dir():
        mkdir(HOME)
    os.chdir(HOME) #смена директории на домашнюю
    with socket.socket() as sock:
        sock.bind(('', PORT))
        sock.listen()
        print("Прослушиваем порт", PORT)

        while True:
            conn, addr = sock.accept()
            handle(conn)

print(func2())
