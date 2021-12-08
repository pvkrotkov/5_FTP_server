import sys, os, shutil
from pathlib import Path
import socket

port=9090
home_path=Path(Path.cwd(), 'home')

def show_dir():
    #dirlist=''
    #for filename in os.listdir(home_path):
        #dirlist+=filename
    return '; '.join(os.listdir(home_path))

def create_dir(name):
    try:
        os.mkdir(name)
    except:
        return(f'Невозможно создать файл, так как он уже существует: {name}')

def create_file(name, text=None):
    with open(name, 'w',encoding='utf-8') as file:
        if text:
            file.write(text)

def delete_dir(name):
    try:
        if os.path.isdir(name):
            os.rmdir(name)
    except OSError:
        return('папка должна быть пустой')

def delete_file(name):
    try:
        os.remove(name)
    except:
        return('Невозможно удалить папку этой командой')

def renamer(name,new_name):
    try:
        os.rename(name,new_name)
    except:
        return(f'Невозможно создать файл, так как он уже существует: {name} -> {new_name}')

def move_file(path,new_path):
    try:
        shutil.move(path,new_path)
    except:
        return("can't move")

def path():
    print(os.getcwd())
    res=os.getcwd()
    return res


def write_help():
    return ("1. show_dir - показать список файлов \
    2. create_dir - создать директорию  \
    3. delete_dir - удаление директории \
    4. move_file- перемещение файла\
    5. delete_file - удаляет файл\
    6. path - показать текущий путь \
    7. renamer - переименовать файл \
    8. create_file - создаёт файл \
    9. write_help - вызвать справку")


def process(request):
    command, *args = request.split()
    commands = {
        'show_dir': show_dir,
        'create_dir': create_dir,
        'delete_dir': delete_dir,
        'move_file': move_file,
        'delete_file': delete_file,
        'path': path,
        'renamer': renamer,
        'create_file': create_file,
        'write_help': write_help #присваиваем командам функции
    }
    try:
        return commands[command](*args)
    except (TypeError, KeyError):
        return 'Bad request'

def manager(conn):
    with conn:
        request = conn.recv(1024).decode()  # принимаем команду
        print(request)
        response = process(request)
        if response is None:
            response = ''
        conn.send(response.encode())


def ftp_server():
    if not home_path.is_dir():
        create_dir(home_path)
    os.chdir(home_path) #смена директории на домашнюю
    with socket.socket() as sock:
        sock.bind(('', port))
        sock.listen()
        print("Прослушиваем порт", port)

        while True:
            conn, addr = sock.accept()
            manager(conn)

print(ftp_server())