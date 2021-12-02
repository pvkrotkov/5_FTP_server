import socket, shutil,os
from pathlib import Path
PORT = 9090


def check_command(req):
    comm, *args = req.split()
    try:
        if comm =='ls':
            return ls(*args)
        elif comm =='pwd':
            return pwd(*args)
        elif comm == 'mkdir':
            return mkdir(*args)
        elif comm =='touch':
            return touch(*args)
        elif comm =='rmdir':
            return rmdir(*args)
        elif comm =='rename':
            return rename(*args)
        elif comm =='rm':
            return rm(*args)
        elif comm =='move':
            return move(*args)
        elif comm =='cat':
            return cat(*args)
        elif comm =='help':
            return help(*args)

    except Exception as e:
        return 'Нет такой команды'


def touch(name, text=''):
    name = Path(name)
    if not name.is_file():
        with open(name, 'w') as file:
            file.write(text)
    else:
        return "Уже есть такой файл"
def pwd():
    return str(home_dir)
def ls(name=None):
    # if name:
    #     return '; '.join(name.iterdir())
    # return '; '.join(home_dir.iterdir())
    if name:
        return '; '.join(os.listdir(name))
    return '; '.join(os.listdir(home_dir))

def mkdir(name):
    name = Path(name)
    if not name.is_dir():
        os.mkdir(name)
    else:
        return "Уже есть такая папка"

def rename(name1, name2):
    name1 = Path(name1)
    name2 = Path(name2)
    if name1.exists():
        os.rename(name1, name2)


def rmdir(name):
    name = Path(name)
    if name.is_dir():
        shutil.rmtree(name)
    else:
        return 'Вы ввели имя не папки'
def rm(name):
    name = Path(name)
    if name.is_file():
        os.remove(name)
    else:
        return 'Вы ввели имя не файла'

def move(src, dst):
    src = Path(src)
    dst = Path(dst)
    if src.exists():
        shutil.move(src, dst)


def cat(name):
    name = Path(name)
    if name.is_file():
        return name.read_text()


def help():
    return 'pwd - вернёт название рабочей директории\n' \
           'ls - вернёт список файлов в рабочей директории\n' \
           'mkdir -  создаёт директорию с указанным именем\n' \
           'rmdir -  удаляет директорию с указанным именем\n' \
           'touch -  создаёт файл с указанным именем\n' \
           'rm -  удаляет файл с указанным именем\n' \
           'move -  перемещает файл/директорию в другую директорию\n' \
           'rename -  переименновывает файл с указанным именем \n' \
           'cat -  вернёт содержимое файла\n' \
           'help - выводит справку по командам\n' \
           'exit - выход из системы'

#
home_dir = Path(os.getcwd(), 'system_home')
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
                    resp= check_command(req)
                if resp is None:
                    resp = ''
                conn.send(resp.encode())


if __name__ == '__main__':
    main()