import errno
import socket
import os
import threading
import utils
import logging
import json
import binascii
import hashlib

'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''
logging.basicConfig(filename="log.log", level=logging.INFO)
log = logging.getLogger("immortal-qQ 's SERVER")


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def add_new_user(address, passwd, name):
    with open("users.json", "r") as f:
        js_file = json.load(f)

    target = js_file["users"]
    user_info = {name: {'password': hash_password(passwd), 'address': address, 'path': name}}
    target.update(user_info)

    with open("users.json", "w") as file:
        json.dump(js_file, file, indent=4)

    os.mkdir("docs/" + name)


def check_if_exist(name):
    with open("users.json", "r") as f:
        temp = json.load(f)
        if temp["users"][name]:
            return True
        else:
            return False


def getpass(name):
    with open("users.json", "r") as f:
        temp = json.load(f)
        passwd = temp["users"][name]["password"]
    return passwd


def register_and_login(conn, addr):
    text = "Введите логин: "
    conn.send(text.encode())
    login = conn.recv(1024).decode()
    conn.send(f"Ваш логин {login}... Теперь введите пароль: ".encode())
    password = conn.recv(1024).decode()

    try:
        if check_if_exist(login):
            while True:
                if verify_password(getpass(login), password):
                    conn.send("Вход успешно выполнен. Теперь сервер будет отвечать на ваши сообщения!".encode())
                    break
                else:
                    conn.send("Пароль неверен, введите его заново: ".encode())
                    password = conn.recv(1024).decode()
    except KeyError:
        conn.send("Увы, такого пользователя нет в базе. Добавление по введенному логину и паролю...".encode())
        add_new_user(addr[0], password, login)
    return login


def accept_client():
    while True:
        conn, addr = sock.accept()
        login = register_and_login(conn, addr)
        CONNECTION_LIST.append((login, conn))
        print(f"{login} is now connected")
        thread_client = threading.Thread(target=broadcast_usr, args=[login, conn])
        thread_client.start()


def broadcast_usr(username, conn):
    while True:
        try:
            request = conn.recv(1024).decode()
            if request:
                response = process(request, username)
                conn.send(response.encode())
        except Exception as ex:
            print(ex)
            break


def process(req, username):
    req_list = req.split(" ")
    req = req_list[0]
    if req == 'pwd':
        return utils.get_curr_path(username)
    elif req == 'ls':
        return utils.files_in_curr_directory(username)
    elif req == 'cat':
        return utils.show_text(username, req_list[-1])
    elif req == 'mkdir':
        return utils.create_folder(username, req_list[-1])
    elif req == 'rmdir':
        return utils.delete_folder(username, req_list[-1])
    elif req == 'touch':
        return utils.create_file(username, req_list[-1])
    elif req == 'rmfile':
        return utils.remove_file(username, req_list[-1])
    elif req == 'mv':
        return utils.rename_file(username, req_list[-2], req_list[-1])
    elif req == 'cd':
        return utils.set_curr_path(username, req_list[-1])
    elif req == 'disconnect':
        pass
    return 'bad request'


CONNECTION_LIST = []
PORT = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if __name__ == "__main__":
    while True:
        try:
            sock.bind(('', PORT))
            print("Сервер запущен на порту -", PORT)
            break
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                print("Порт уже занят!")
                PORT += 1
            else:
                print("Ошибка в подключении! ", e)

    sock.listen()

    thread = threading.Thread(target=accept_client())
    thread.start()
