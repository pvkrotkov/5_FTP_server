import socket
import os
import config
from commands import *

commands = {
    'crfol': crfol, # создание папки с указанием имени
    'rmfol': rmfol, # удаление папки
    'fv': fv, # перемещение между папками
    'crfil': crfil, # создание пустых файлов с указанием имени
    'record': record, # запись текста в файл
    'show': show, # просмотр содержимого файла
    'rmfil': rmfil, # удаление файла по имени
    'copy': cp, # копирование файлов из одной папки в другую
    'dupl': dupl, # дублирование файлов
    'move': move, # перемещение файлов
    'rename': rename, # переименование файлов
    'dir': dir, # просмотр содержимого директории
    'loc': loc, # где находится пользователь сейчас
    'help': help, # справка
    'exit': exit,
    }

def process(cmd):
    try:
        cmd = cmd.split()
        command, args = cmd[0], cmd[1:]
    except:
        return f'Команда {cmd} не распознана.'

    try:
        return commands[command](*args)
    except KeyError:
        return f'Команда {command} не найдена.'



PORT = 6666
sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
crfol(config.work_dir)
os.chdir(config.work_dir)
print('Выполнен переход в рабочую папку.')
print("Прослушиваем порт", PORT)


while True:
    conn, addr = sock.accept()

    request = conn.recv(8192).decode()
    print(request)

    response = process(request)
    conn.send(response.encode())

conn.close()
