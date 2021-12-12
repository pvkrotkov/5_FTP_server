import os
import shutil
import socket
from datetime import datetime

DELIMITER = os.sep
MAIN_DIRECTORY = os.getcwd() + DELIMITER + "docs"
LOG = MAIN_DIRECTORY + DELIMITER + "log.txt"
USER_DIRECTORY = MAIN_DIRECTORY
PATH = USER_DIRECTORY
LOGIN = " "
ADMIN = "root"
USER_IS_ADMIN = False
MAX_SIZE = 15


def get_directory_size(directory):
    directory_size = 0
    for path, directories, files in os.walk(directory):
        for directory in directories:
            directory_size += get_directory_size(os.path.join(path, directory))
        for file in files:
            directory_size += os.path.getsize(os.path.join(path, file))
    return directory_size


def check_directory_size():
    return get_directory_size(USER_DIRECTORY) > MAX_SIZE


def is_path_correct(path):
    return USER_DIRECTORY in os.path.abspath(path) or USER_IS_ADMIN


def pwd():
    current_path = os.getcwd().replace(USER_DIRECTORY, "")
    if current_path == "":
        current_path = "\\"
    return current_path + "\n"


def ls():
    return "; ".join(os.listdir(PATH)) + "\n"


def cd(path, ignore_limitation=False):
    global PATH
    path = USER_DIRECTORY if path == "~" else path
    if is_path_correct(path) or ignore_limitation is True:
        if os.path.isdir(path):
            os.chdir(path)
            PATH = os.getcwd()
            return "\n"
        else:
            return "Путь неверный\n"
    else:
        return "Путь неверный\n"


def mkdir(path):
    if is_path_correct(path) or USER_IS_ADMIN:
        os.mkdir(path)
        if check_directory_size():
            rm(path)
            return "Не хватает места\n"
        return "\n"
    else:
        return "Путь неверный\n"


def mv(source, destination):
    if os.path.exists(source):
        if is_path_correct(source) and is_path_correct(destination):
            shutil.move(source, destination)
            return "\n"
        else:
            return "Путь неверный\n"
    else:
        return "Путь неверный\n"


def rm(path):
    if is_path_correct(path):
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            return "\n"
        else:
            return "Путь неверный\n"
    else:
        return "Путь неверный\n"


def cat(path):
    if is_path_correct(path):
        if os.path.exists(path):
            with open(path, "r") as file:
                return file.read() + "\n"
        else:
            return "Путь неверный\n"
    else:
        return "Путь неверный\n"


def touch(path):
    if is_path_correct(path):
        if not path.endswith(".txt"):
            path += ".txt"
        with open(path, "a") as file:
            pass
        if check_directory_size():
            rm(path)
            return "Не хватает места\n"
        return "\n"
    else:
        return "Путь неверный\n"


def write(*args):
    path = args[0]
    content = " ".join(args[1:])
    if os.path.isfile(path):
        if is_path_correct(path):
            with open(path, "r") as file:
                temp_text = file.read()
            with open(path, "a") as file:
                file.write(content)
            if check_directory_size():
                with open(path, "w") as file:
                    content = temp_text.replace(content, "", (temp_text.count(content) - 1))
                    file.write(content)
                    return "Не хватает места\n"
            return "\n"
        else:
            return "Путь неверный\n"
    else:
        return "Путь неверный\n"


def memory():
    return f"Всего есть: {MAX_SIZE}\nИз них свободно: {MAX_SIZE - get_directory_size(USER_DIRECTORY)}\n"


def help():
    return "pwd - выводит текущий путь\n" \
           "ls DIRECTORY- выводит содержимое текущего каталога\n" \
           "cd DIRECTORY- изменяет текущий каталог\n" \
           "mkdir DIRECTORY - создает каталог\n" \
           "rm PATH - удаляет файл или каталог\n" \
           "mv SOURCE DESTINATION - перемещает или переименовывает файл\n" \
           "cat FILE - выводит содержимое файла\n" \
           "touch FILE - создает пустой файл\n" \
           "write FILE TEXT - записывает текст в файл\n" \
           "memory - выводит информацию о памяти" \
           "exit - разрыв соединения с сервером\n" \
           "help - выводит справку по командам\n"


COMMANDS = {
    "pwd": pwd,
    "ls": ls,
    "cd": cd,
    "mkdir": mkdir,
    "rm": rm,
    "mv": mv,
    "cat": cat,
    "touch": touch,
    "write": write,
    "memory": memory,
    "help": help
}


def process(request):
    command, *args = request.split(" ")
    add_log(f"От пользователя {LOGIN} получено '{request}'")
    try:
        response = COMMANDS[command](*args)
    except:
        response = "incorrect request\n"
    add_log(f"Пользователю {LOGIN} отправлено '{response}'")
    return response


def read_logins(currentPath=os.getcwd()):
    os.chdir(MAIN_DIRECTORY)
    with open(MAIN_DIRECTORY + DELIMITER + "logins.txt", "r") as file:
        logins = dict()
        for row in file:
            login = row.split(":")[0]
            password = ":".join(row.split(":")[1:])[:-1]
            logins.update(dict([(login, password)]))
    os.chdir(currentPath)
    return logins


def add_logins(logins, path=os.getcwd()):
    os.chdir(MAIN_DIRECTORY)
    with open("logins.txt", "a") as file:
        for login, password in logins.items():
            file.write(f"{login}:{password}\n")
    os.chdir(path)


def add_log(log):
    with open(MAIN_DIRECTORY + DELIMITER + "log.txt", "a") as file:
        file.write(f"•••••••••••••••••••••••••\n")
        file.write(f"{datetime.now()}:\n{log}\n")


def create_user_directory(login):
    global USER_DIRECTORY, DELIMITER, PATH
    if not (os.path.exists(USER_DIRECTORY + DELIMITER + login) and os.path.isdir(USER_DIRECTORY + DELIMITER + login)):
        os.mkdir(login)
    USER_DIRECTORY = USER_DIRECTORY + DELIMITER + login
    PATH = USER_DIRECTORY
    cd(login, True)


def handle(sock, conn):
    global USER_IS_ADMIN, LOGIN, USER_DIRECTORY, PATH
    USER_IS_ADMIN = LOGIN == ADMIN
    if LOGIN == ADMIN:
        LOGIN += "#"
    conn.send(("Вы вошли" + "\n" + LOGIN + "; path: " + pwd()[:-1] + ">>").encode())
    add_log(f"Пользователь {LOGIN} авторизовался")
    while True:
        try:
            request = conn.recv(1024).decode()
            if request == "exit":
                conn.close()
            response = process(request)
            conn.send(response.encode())
            conn.send((LOGIN + "; path:" + pwd()[:-1] + ">>").encode())
        except:
            break
    os.chdir(MAIN_DIRECTORY)
    USER_DIRECTORY = MAIN_DIRECTORY
    PATH = USER_DIRECTORY
    conn.close()
    accept_connection(sock)


def get_password(sock, conn, correctPassword):
    conn.send("Введите пароль:".encode())
    password = conn.recv(1024).decode()
    if password == correctPassword:
        handle(sock, conn)
    else:
        get_password(sock, conn, correctPassword)


def get_new_password(sock, conn, login):
    conn.send("Введите новый пароль:".encode())
    new_password = conn.recv(1024).decode()
    add_logins(dict([(login, new_password)]), path=os.getcwd())
    handle(sock, conn)


def get_login_and_password(sock, conn):
    global LOGIN
    logins = read_logins(os.getcwd())
    conn.send("Логин:".encode())
    login = conn.recv(1024).decode()
    create_user_directory(login)
    LOGIN = login
    if login in logins.keys():
        get_password(sock, conn, logins[login])
    else:
        get_new_password(sock, conn, login)


def accept_connection(sock):
    while True:
        try:
            conn, (addr, port) = sock.accept()
            add_log(f"Соединено с {addr}, {port}")
            get_login_and_password(sock, conn)
        except:
            continue


def main():
    read_logins(MAIN_DIRECTORY)
    cd(USER_DIRECTORY, ignore_limitation=True)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 9091))
    sock.listen(1)
    accept_connection(sock)


if __name__ == '__main__':
    main()
