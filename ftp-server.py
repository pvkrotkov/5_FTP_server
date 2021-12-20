import socket
import os
from pathlib import Path
import shutil
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''
PORT = 6666
PATH = Path(Path.cwd(), 'home')

def pwd():
    return str(PATH)



def touch(path, text=''):
    path = Path(path)
    path.touch()
    path.write_text(text)

def ls(path=None):
    if path:
        return '; '.join(os.listdir(path))
    return '; '.join(os.listdir(PATH))

def mkdir(path):
    path = Path(path)
    rm(path)
    path.mkdir(parents=True)


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
        response = main(request)
        if response is None:
            response = ''
        conn.send(response.encode())

def main(request):
    command, *args = request.split()
    commands = {'ls': ls, 'pwd': pwd, 'mkdir': mkdir, 'touch': touch, 'rm': rm, 'mv': mv, 'cat': cat, 'help': help}
    try:
        return commands[command](*args)
    except (TypeError, KeyError):
        return 'Error'

def help():

    return 'ls - Посмотреть содержимое папки\n' \
           'pwd - вывести путь текущего каталога\n' \
           'mkdir name - создает каталог\n' \
           'touch - создает пустой файл или файл с текстом\n' \
           'rm - удаляет файл\n' \
           'mv - перемещает (переименовывает файл)\n' \
           'cat - выводит содержимое файла\n' \
           'help - вывести список доступных команд\n' \
           'exit - выход'
if not PATH.is_dir():
    mkdir(PATH)
os.chdir(PATH)

with socket.socket() as sock:
    sock.bind(('', PORT))
    sock.listen()
    print("Прослушиваю порт -", PORT)

    while True:
        conn, addr = sock.accept()
        handle(conn)
