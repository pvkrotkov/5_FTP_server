import socket, shutil, os
from pathlib import Path

host = ''
port = 9090

def ls(path=None):
    if path:
        try:
            return '/'.join(os.listdir(path))
        except FileNotFoundError:
            return 'Такой директории не существует!'
    else:
        #содержимое текущей папки
        return os.listdir(os.getcwd())

def pwd():
     return str(os.getcwd())

def mkdir(path):
    rezz = 0#не получилось создать файl
    if os.path.dirname(path)!='':
        path = Path(path)
        path.mkdir(parents=True)
        rezz = 1
    else: 
        path = Path(os.getcwd(),path) 
        path.mkdir(parents=True)
        rezz = 1
    return rezz

def touch(path, text=None):
    rezz = 0 #не получилось создать файл

    try:
        if text: text = text
        else: text = ""

        if os.path.dirname(path)!='':
            path = Path(path)
            path.touch()
            path.write_text(text)
            rezz = 1
        else:
            path = Path(os.getcwd(),path) 
            path.touch()
            path.write_text(text)
            rezz = 1
        return rezz
    except FileExistsError:
        return "Файл уже существует!"
         
def rm(path):
    rezz = 0#не получилось удалить файл 

    if os.path.dirname(path)!='':
        path = Path(path)
        if path.is_dir():
            shutil.rmtree(path) #удаление каталога рекурсивно (все содержимое)
        elif path.is_file():
            path.unlink() #удаление файла
        rezz = 1
    else:
        path = Path(os.getcwd(),path) 
        if path.is_dir():
                shutil.rmtree(path) #удаление каталога рекурсивно (все содержимое)
        elif path.is_file():
                path.unlink() #удаление файла
        rezz = 1
    return rezz

def cd(path):
    rezz = 0
    try:
        if path!='..':
            if os.path.dirname(path)!='':
                    os.chdir(path)
                    rezz = 1
            else:
                os.chdir(f'{os.getcwd()}/{path}')
                rezz = 1
        else:
            os.chdir(os.path.dirname(os.getcwd()))
            rezz = 1
        return rezz
    except  FileNotFoundError:
        return 'Такой директории не существует!'

def mv(source, destination):
    rezz = 0
    source = Path(source)
    destination = Path(destination)
    if source.exists():
        shutil.move(str(source), str(destination))
        rezz = 1
    else:
        shutil.move(str(destination), str(source))
        rezz = 1
    return rezz

def cat(path):
    path = Path(path)
    if path.is_file():
        return path.read_text()
    else: return "Ошибка! Не является файлом"

def help_():
    return '''Справка:
        1. ls [DIRECTORY]- выводит содержимое каталога 
        2. pwd - выводит путь текущего каталога 
        3. mkdir DIRECTORY - создает каталог 
        4. touch FILE [TEXT] - создает пустой файл или файл с текстом 
        5. rm FILE - удаляет файл 
        6. mv SOURCE DESTINATION - перемещает (переименовывает файл) 
        7. cat FILE - выводит содержимое файла 
        8. help - выводит справку по командам 
        9. exit - разрыв соединения с сервером 
        '''


def process(req):
    command, *args = req.split()
    #req = req.split()
    #command, *args = req[0], req[1:]
    #if command == 'home_dir': home_dir(req[1])
    #elif command == 'ls': ls(req[1])
    #elif command == 'pwd': pwd()
    #elif command == 'mkdir': 
     #   if len(req[1:]) == 2: mkdir(req[1], req[:-1])
     #   else: mkdir(req)
    commands = {
        'ls': ls,
        'pwd': pwd,
        'mkdir': mkdir,
        'touch': touch,
        'rm': rm,
        'mv': mv,
        'cat': cat,
        'help': help_
    }
    try:
        r = commands[command](*args)
        return r
    except (TypeError, KeyError):
         return 'Bad request'

#принимаем и обрабатываем/посылаем информацию от клиента
def server_func(client):
    response = None
    with client:
        request = client.recv(1024).decode()
        print(request)

        response = process(request)

        if response == '1':
            response = "Успешно"
        elif response == '0':
            response = 'Ошибка! Невозможно произвести действие'
        client.send(response.encode())

#запуск сервера
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((host, port))
    server.listen()
    print('Прослушивание порта', port)

    while True:
        client, addr = server.accept()
        server_func(client)


if __name__ == '__main__':
    start_server()
