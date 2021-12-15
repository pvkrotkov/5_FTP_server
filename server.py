import socket, shutil,os
from pathlib import Path
PORT = 80


def check(req):
    try:
        if ' ' in req:
            comm, *args = req.split()
            return (eval(f'{comm}({args})'))
        else:
            comm = req
            return (eval(f'{comm}()'))
    except Exception as e:
        print(e)
        return 'Нет такой команды'


def touch(names):
    name = Path(names[0])
    if not name.is_file():
        with open(name, 'w') as file:
            file.write(names[1])
    else:
        return "Уже есть такой файл"

def pwd():
    return str(home_dir)

def ls(name=None):
    # if name:
    #     return '; '.join(name.iterdir())
    # return '; '.join(home_dir.iterdir())
    if name:
        return ' '.join(os.listdir(name[0]))
    return ' '.join(os.listdir(home_dir))

def mkdir(names):
    for n in names:
        name = Path(n)
        if not name.is_dir():
            os.mkdir(name)
        else:
            return "Уже есть такая папка"

def rename(names):
    name1 = Path(names[0])
    name2 = Path(names[1])
    if name1.exists():
        os.rename(name1, name2)


def rmdir(names):
    for name in names:
        name = Path(name)
        if name.is_dir():
            shutil.rmtree(name)
        else:
            return 'Такой папки нет'

def rm(names):
    for name in names:
        n = Path(name)
        if n.is_file():
            os.remove(n)
        else:
            return 'Такого файла нет'

def move(source):
    if Path(source[1]).exists() and Path(source[0]).exists():
        shutil.move(source[0], source[1])


def cat(names):
    for name in names:
        n = Path(name)
        if n.is_file():
            return n.read_text()

home_dir = Path(os.getcwd(), 'home')
def main():
    #
    if not home_dir.is_dir():
        os.mkdir(home_dir)
    os.chdir(home_dir)
    #
    with socket.socket() as sock:
        sock.bind(('', PORT))
        sock.listen()
        print("Слушаем порт:", PORT)
        while True:
            conn, addr = sock.accept()
            with conn:
                req = conn.recv(1024).decode()
                if len(req) > 0:
                    print('request: ',req)
                    resp = check(req)
                if resp is None:
                    resp = ''
                conn.send(resp.encode())


if __name__ == '__main__':
    main()