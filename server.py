from pathlib import Path
import socket
import shutil
import os
PORT = 1111
HOME = Path(Path.cwd(), 'home')





def pwd():
    return str(HOME)

def mkdir(path):
    path = Path(path)
    rm(path)
    path.mkdir(parents=True)

def touch(path, text=''):
    path = Path(path)
    path.touch()
    path.write_text(text)

def ls(path=None):
    if path:
        return '; '.join(os.listdir(path))
    return '; '.join(os.listdir(HOME))

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




def handle(conn):
    with conn:
        request = conn.recv(1024).decode()
        print(request)
        response = process(request)
        if response is None:
            response = ''
        conn.send(response.encode())

def process(request):
    command, *args = request.split()
    commands = {'ls': ls, 'pwd': pwd, 'mkdir': mkdir, 'touch': touch, 'rm': rm, 'mv': mv, 'cat': cat, 'help': help}
    try:
        return commands[command](*args)
    except (TypeError, KeyError):
        return 'Bad request'
def help():
    return 'ls - Посмотреть содержимое папки\n' \
           'pwd - вывести путь текущего каталога\n' \
           'mkdir name - создает каталог\n' \
           'touch file text - создает пустой файл или файл с текстом\n' \
           'rm file - удаляет файл\n' \
           'mv from to - перемещает (переименовывает файл)\n' \
           'cat file - выводит содержимое файла\n' \
           'help - вывести сообщение с командами\n' \
           'exit - выход'

if not HOME.is_dir():
    mkdir(HOME)
os.chdir(HOME)
with socket.socket() as sock:
    sock.bind(('', PORT))
    sock.listen()
    print("Прослушиваем порт", PORT)

    while True:
        conn, addr = sock.accept()
        handle(conn)