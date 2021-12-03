import socket
import os
from shutil import rmtree
import pickle
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')

def process(req):
    print("".join((list(req)[:3])))
    if req == 'pwd':
        return dirname
    elif req == 'ls':
        return '; '.join(os.listdir(dirname))
    elif "".join((list(req)[:5])) == "mkdir":
        os.mkdir(os.path.join(dirname, "".join((list(req)[6:]))))
        return f'Created dir: {"".join((list(req)[6:]))}'
    elif "".join((list(req)[:5])) == "rmdir":
        try:
            rmtree(os.path.join(dirname,"".join((list(req)[6:]))))
            return f'Папка {"".join((list(req)[6:]))} удалена'
        except NotADirectoryError:
            return "Это не папка!"
    elif "".join((list(req)[:2])) == "rm":
        try:
            os.remove(os.path.join(dirname,"".join((list(req)[3:]))))
            return f'Файл {"".join((list(req)[3:]))} удален'
        except IsADirectoryError:
            return "Это не файл!"
    elif "".join((list(req)[:3])) == "mv ":
        names = "".join(list(req)[3:]).split(" ")
        os.rename(os.path.join(dirname, names[0]), os.path.join(dirname, names[1]))
        return  "Успешно перемещено"
    elif req[:8] == "download":
        file1 = os.path.join(dirname, req[9:])
        with open(file1, "rb") as file:
            content = file.read(1024)
            conn.send(content)
        return "Файл отправлен"
    elif req[:6] == "upload":
        file1 = os.path.join(dirname, req[7:])
        with open(file1, "wb") as file:
            content = conn.recv(1024)
            file.write(content)
        return "Файл получен"
    else:
        return 'bad request'


PORT = 6666

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(1024).decode()
    print(request)
    
    response = process(request)
    conn.send(response.encode())

conn.close()
