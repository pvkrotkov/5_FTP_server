import socket
import os
import shutil
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
rmdir <directoryname> - удаление директории
mkdir <directoryname> - создание директории
create <filename> - создание файла
rename <filename> - переименование файла
remove <filename> - удаление пути к файлу
copy <filename> <newfilename> - копирование файла
'''

dirname = os.path.join(os.getcwd(), 'docs')
def process(req): #Функция обработки запроса
    rq =req.split()
    if req == 'pwd': #Вывод названия рабочей директории
        return dirname
    elif req == 'ls': #Вывод содержимого текущей директории
        return '; '.join(os.listdir(dirname))
    elif req[:3] == 'cat': #Отправка содержимого файла
        path = os.path.join(os.getcwd(), 'docs', req[4::])
        if os.path.exists(path):
            with open(path, 'r+') as f:
                line = ''
                for l in f:
                    line+=l
            return line
        else:
            return 'Файл отсутствует'
    elif req[:5] == 'rmdir': #Удаление директории
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        if os.path.exists(path):
            shutil.rmtree(os.path.join(os.getcwd(), 'docs', req[6::]))
            return f'Папка удалена'
        else:
            return 'Папка отсутствует'    
    elif req[:5] == 'mkdir': #Создание директории
        path = os.path.join(os.getcwd(), 'docs', req[6::])
        if not os.path.exists(path):
            os.makedirs(path)
            return f'Папка создана'
        else: 
            return 'Данная папка уже существует'
    elif req[:6]  == 'create': #Создание файла
        open(os.path.join(os.getcwd(), 'docs', req[7:]), 'tw', encoding='utf-8').close()
        return f'Файл создан'
    elif req[:6]  == 'rename': #Переименование файла
        req = req.split(' ')
        os.rename(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
        return 'Файл переименован'
    elif req[:6]  == 'remove': #Удаление пути к файлу
        os.remove(os.path.join(os.getcwd(), 'docs', req[7:]))
        return f'Файл удален'
    elif req[:4]  == 'copy': #Копирование файла
        req = req.split(' ')
        shutil.copyfile(os.path.join(os.getcwd(), 'docs', req[1]), os.path.join(os.getcwd(), 'docs', req[2]))
        return 'Файл скопирован'
    return 'bad request'

PORT = 1899 #Создание сервера

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
