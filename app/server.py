import socket
import random 
import hashlib
import sys
import os, shutil, subprocess
from options import root_folder, logspath
from threading import Thread
from datetime import datetime
import time

def cdr(*args):
    '''
    Change directory. Смена директории. Можно вводить как абсолютный, так и относительный путь. Для шага вверх по директориям нужно ввести две точки. Для текущей директории одна точка (как и во всех файловых менеджерах.)
    '''
    current_path = args[0]
    conn = args[1]
    args = args[2:]
    if len(args) == 0 or len(args) > 1:
        conn.send('Введите путь, по которому перемещаемся.'.encode())
    else:
        if args[0] == '..':
            if current_path[1] != '/':
                prevdir = current_path[1].rfind('/')
                try:
                    if prevdir == 0:
                        os.chdir(current_path[0])
                        current_path = [current_path[0], '/'+os.getcwd()[len(current_path[0]):].replace('\\', '/')]
                    else:
                        os.chdir(current_path[0]+current_path[1][:prevdir])
                        current_path = [current_path[0], os.getcwd()[len(current_path[0]):].replace('\\', '/')]
                    conn.send(f'Вы поднялись вверх на один уровень.'.encode())
                except PermissionError:
                    conn.send(f'Недостаточно прав.'.encode())
            else:
                conn.send('Вы достигли корневого раздела.'.encode())
        elif args[0] == '.':
            conn.send(f'Вы остались в текущей папке.'.encode)
        elif args[0][0] == '/':
            if os.path.exists(current_path[0]+args[0]):
                try:
                    os.chdir(current_path[0]+args[0])
                    if len(args[0]) == 1:
                        current_path = [current_path[0], '/'+os.getcwd()[len(current_path[0]):].replace('\\', '/')]
                    else:
                        current_path = [current_path[0], os.getcwd()[len(current_path[0]):].replace('\\', '/')]
                    conn.send(f'Вы успешно перешли в другую папку.'.encode())
                except PermissionError:
                    conn.send(f'Недостаточно прав.'.encode())
            else:
                conn.send('Указанной директории не существует.'.encode())
        else:
            if os.path.exists(current_path[0]+current_path[1]+'/'+args[0]):
                try:
                    os.chdir(current_path[0]+current_path[1]+'/'+args[0])
                    current_path = [current_path[0], os.getcwd()[len(current_path[0]):].replace('\\', '/')]
                    conn.send(f'Вы успешно перешли в другую папку.'.encode())
                except PermissionError:
                    conn.send(f'Недостаточно прав.'.encode())
            else:
                conn.send('Указанной директории не существует.'.encode())
    return current_path

def adr(*args):
    '''
    Add directory. Функция создания директории. Можно создать несколько директорий, если ввести несколько аргументов.
    '''
    current_path = args[0]
    conn = args[1]
    args = args[2:]
    if len(args) == 0:
        conn.send('Введите название создаваемой папки.'.encode())
    else:
        if len(args) > 1: 
            conn.send('Вы ввели несколько параметров, введите один чтобы создать папку.'.encode())
        else:
            os.chdir(current_path[0]+current_path[1])
            for name in args:
                try:
                    os.mkdir(name)
                    conn.send(f'Создана папка {name}.'.encode())
                except FileExistsError:
                    conn.send(f'Создаваемая папка уже существует [{name}].'.encode())
                except PermissionError:
                    conn.send(f'Недостаточно прав.'.encode())
    return current_path

def ddr(*args):
    '''
    Delete directory. Удаление директории. Можно удалить несколько папок, если ввести несколько аргументов.
    '''
    current_path = args[0]
    conn = args[1]
    args = args[2:]
    if len(args) == 0:
        conn.send('Введите название удаляемой папки.'.encode())
    else:
        if len(args) > 1: 
            conn.send('Вы ввели несколько параметров, введите один чтобы удалить папку.'.encode())
        else:
            os.chdir(current_path[0]+current_path[1])
            for name in args:
                try:     
                    os.rmdir(name)
                    conn.send(f'Удалена папка {name}.'.encode())
                except FileNotFoundError:
                    conn.send(f'Указанной папки не существует [{name}].'.encode())
                except PermissionError:
                    conn.send(f'Недостаточно прав.'.encode())
    return current_path

def afl(*args):
    '''
    Add file. Создание файла. Можно создать несколько файлов, если ввести несколько аргументов.
    '''
    current_path = args[0]
    conn = args[1]
    args = args[2:]
    if len(args) == 0:
        conn.send('Введите название создаваемого файла (с расширением).'.encode())
    else:
        if len(args) > 1: 
            conn.send('Вы ввели несколько параметров, введите один чтобы создать файл.'.encode())
        else:
            os.chdir(current_path[0]+current_path[1])
            for name in args:      
                if os.path.exists(current_path[0]+current_path[1]+'/'+name):
                    conn.send(f'Создаваемый файл уже существует [{name}].'.encode())
                else:
                    try:
                        open(name, "w")
                        conn.send(f'Создан файл {name}.'.encode())
                    except PermissionError:
                        conn.send(f'Недостаточно прав.'.encode())
    return current_path

def dfl(*args):
    '''
    Delete file. Удаление файла. Можно удалить несколько файлов, если ввести несколько аргументов.
    '''
    current_path = args[0]
    conn = args[1]
    args = args[2:]
    if len(args) == 0:
        conn.send('Введите название удаляемого файла (с расширением).'.encode())
    else:
        if len(args) > 1: 
            conn.send('Вы ввели несколько параметров, введите один чтобы удалить файл.'.encode())
        else:
            os.chdir(current_path[0]+current_path[1])
            for name in args:
                try:
                    os.remove(name)
                    conn.send(f'Удален файл {name}.'.encode())
                except FileNotFoundError:
                    conn.send(f'Указанного файла не существует [{name}].'.encode())
                except PermissionError:
                    conn.send(f'Недостаточно прав.'.encode())
    return current_path

def rfl(*args):
    '''
    Rename file. Переименовывание указанной директори или указанного файла. Напишите путь к файлу и новый путь к файлу (не новое имя).
    '''
    current_path = args[0]
    conn = args[1]
    args = args[2:]
    if len(args) == 2:
        try:
            os.chdir(current_path[0]+current_path[1])
            if args[0][0] == '/':
                pass
            else:
                os.rename(current_path[0]+current_path[1]+'/'+args[0], current_path[0]+current_path[1]+'/'+args[1])
            conn.send(f'Переименован файл.'.encode())
        except FileNotFoundError:
            conn.send(f'Указанный файл не существует [{args[0]}].'.encode())
        except PermissionError:
            conn.send(f'Недостаточно прав.'.encode())
    else:
        conn.send('Введите текущее имя файла, а также новое имя файла.'.encode())
    return current_path

def sfl(*args):
    '''
    Send file. Послыает указанный файл на сервер.
    '''
    current_path = args[0]
    conn = args[1]
    args = args[2:]
    if len(args) == 1:
        filename = args[0]
        conn.send('send'.encode())
        conn.send(filename.encode())
        data = conn.recv(2048)
        filesize = data.decode()
        data = conn.recv(int(filesize))
        os.chdir(current_path[0]+current_path[1])
        time.sleep(1)
        with open(filename, 'w') as f:
            f.write(data.decode())
    else:
        conn.send('Неправильное количество параметров. Отправьте 1 файл.'.encode())
    return current_path


def dlfl(*args):
    '''
    Download file. Скачивает указанный файл с сервера.
    '''
    current_path = args[0]
    conn = args[1]
    args = args[2:]
    if len(args) == 1:
        filename = args[0]
        conn.send('receive'.encode())
        conn.send(filename.encode())
        filesize = str(os.path.getsize(filename))
        conn.send(filesize.encode())
        data = ''
        with open(filename, 'r') as f:
            for line in f:
                data += line
        conn.send(data.encode())
        conn.send(f'Файл {filename} успешно отправлен на клиент.'.encode())
    else:
        conn.send('Неправильное количество параметров. Выберите 1 файл.'.encode())
    return current_path

def s_register(conn, addr):
    try:
        data = conn.recv(1024)
        login = data.decode()
        data = conn.recv(1024)
        passw = data.decode()
        if login in userinfo:
            conn.send('занято'.encode())
            return

        # хеширование
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
        	'sha256',
        	passw.encode('utf-8'),
        	salt,
        	100000
        )

        userinfo[login] = [addr[0], salt+key]
        conn.send('успешно'.encode())
        os.mkdir(root_folder+'/'+login)
        with open('clients.txt', 'w') as file:
            print(userinfo, file = file)
        logging(f'подключение {addr}')
        main(login, conn, addr)
    except:
        conn.send('что-то пошло не так'.encode())

def s_login(conn, addr):
    try:
        data = conn.recv(1024)
        login = data.decode()
        data = conn.recv(1024)
        passw = data.decode()

		# проверка пароля по ключу и хешу
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            passw.encode('utf-8'),
			userinfo[login][1][:32],
			100000
		)

        if new_key == userinfo[login][1][32:]:
            conn.send('успешно'.encode())
            logging(f'подключение {addr}')
            main(login, conn, addr)
        else:
            conn.send('неправильные данные'.encode())
    except:
        conn.send('что-то пошло не так'.encode())

def c(*args):
    current_path = args[0]
    conn = args[1]
    args = args[2:]
    if sys.platform == 'win32': 
        result = subprocess.check_output('dir /X /OG /A',shell=True, text = True)
        result = result.split('\n')
        result = result[5:-3]
        result = '\n'.join(result)
        conn.send(result.encode())
    else:
        result = subprocess.check_output('ls -l',shell=True, text = True)
        conn.send(result.encode())
    return current_path

def print_help(conn):
	conn.send('''
c - Вывести текущее расположение (посмотреть содержимое текущей папки)
cdr [folder_path] - Перемещение между папками (в пределах рабочей папки) - заход в папку по имени, выход на уровень вверх;
adr [folder_path] - Создание папки (с указанием имени);
ddr [folder_path] - Удаление папки по имени;
afl [file_path] - Создание пустых файлов с указанием имени;
dfl [file_path] - Удаление файлов по имени;
rfl [file_path] [new_file_path] - Переименование файлов.

sfl [file_path] - Отправить файл на сервер;
dlfl [file_path] - Скачать файл с сервера;

напишите exit или close, чтобы выйти из программы'''.encode())

def main(login, conn, addr):
    global isshutdown
    print(f'Клиент {addr} успешно подключился.')
    connected = True
    current_path = [root_folder+'/'+login]
    os.chdir(current_path[0])
    current_path.append('/'+os.getcwd()[len(root_folder+'/'+login):].replace('\\', '/'))
    print_help(conn)
    while connected and not isshutdown:
        conn.send('|||'.join(current_path).encode())
        data = conn.recv(1024)
        command = data.decode().split()
        comforlog = ' '.join(command)
        logging(f'сообщение от {addr[0]}: {comforlog}')
        if len(command) != 0:
            if command[0] == '<empty>':
                pass
            elif command[0] == 'exit' or command[0] == 'close':
                conn.send('exit'.encode)
            elif command[0] == 'help':
                print_help(conn)
            elif login == 'admin' and command[0] == 'shutdown':
                isshutdown = True
                logging('остановка сервера')
            else:
                try:
                    current_path = commands[command[0]](current_path, conn, *command[1:])
                except KeyError:
                    conn.send('ke'.encode())
                except TypeError:
                    conn.send('te'.encode())
		
def logging(msg):
    f = open(logspath, 'a')
    f.write(f'[{str(datetime.now())[:-7]}] - {msg} \n')
    f.close()

def working_with_clients(conn, addr):
    try:
        conn.send('Регистрация или логин?'.encode())
        data = conn.recv(1024)
        if data.decode() == 'l':
            s_login(conn, addr)
        else:
            s_register(conn, addr)
        print(f'Отключение клиента {addr}...')
        logging(f'отключение {addr}')
    except:
        print(f'Экстренное отключение клиента {addr}...')

def waiting_for_client():
    try:
        while True:
            conn, addr = sock.accept()
            print(f'Подключение клиента {addr}...')
            Thread(target=working_with_clients, args=[conn,addr]).start()		
    except: 
        print('Остановка сервера...')  
        logging('остановка сервера')
        conn.close()

if __name__ == '__main__':
    logs = {}
    isshutdown = False
    commands = {'c': c, 'adr': adr, 'ddr': ddr, 'cdr': cdr, 'afl': afl, 'dfl': dfl, 'rfl': rfl, 'sfl': sfl, 'dlfl': dlfl}
    userinfo = {}
    with open('clients.txt', 'r') as file:
        for line in file.readlines():
            userinfo = eval(line)

    sock = socket.socket()
    print('Запуск сервера...')
    logging('запуск сервера')
    port = 9090
    ready = False
    while not ready:
        try:
            sock.bind(('', port))
            ready = True
        except:
            pport = port
            port = random.randint(1000, 9999)
    print(f'Прослушивание порта {port}...')
    sock.listen(0)
    Thread(target=waiting_for_client, daemon = True).start()
    while not isshutdown:
        time.sleep(1)
    time.sleep(2)