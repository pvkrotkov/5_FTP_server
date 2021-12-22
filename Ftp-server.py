import socket
import os
import shutil
import sys



#Функции менеджера

def Path(path = ""):
    if path == "":
        cf(pwd())
    else:
        cf(path)


def initial_func():
    OS = sys.platform
    if OS == 'darwin':
        symbol_l = '/'

    elif OS == 'cygwin' or OS == 'win32' :
        symbol_l = "\\"

    else:
        symbol_l = "/"


    tr = os.getcwd()
    tr = tr.split(symbol_l)
    tr = tr[:-1:]
    tr_len = len(tr)

    return tr_len




def mkfold(folder_name):
    os.mkdir(folder_name)
    return "папка " + folder_name + " создана"

def rmfold(folder_name):
    shutil.rmtree(folder_name)
    return "папка " + folder_name + " удалена"

def cf(path):
    try:
        OS = sys.platform
        if OS == 'darwin':
            symbol = '/'

        elif OS == 'cygwin' or OS == 'win32' :
            symbol = "\\"

        else:
            symbol = "/"

        if path == "-":

            p = str(os.getcwd())
            p = p.split(symbol)
            p[0] = ""
            p[-1] = ""

            #if len(p)-1 > initial_func():

            sum = ""
            for i in range(len(p)):
                sum = sum + symbol + p[i]
            sum = sum[1::]

            os.chdir(sum)
            #else:
                #print('Дальше нельзя')

        elif  "."+symbol in path:
            p = str(os.getcwd())+symbol+path[2::]
            os.chdir(p)


        else:
            os.chdir(path)
        return "вы переместились"
    
    except:
        return "что-то пошло не так"

def list():
    return str((os.listdir()))

def pwd():
    return str((os.getcwd()))

def create(file_name):
    file = open(file_name, "w+")
    file.close()
    a = "Создан файл " + file_name
    return str(a)

def rmv(file_name):
    try:
        os.remove(file_name)
        a = "Удален файл " + file_name
        return str(a) 
    except:
        a = 'Что-то пошло не так'
        return str(a)
    

def cet(file_name):
    try:
        file = open(file_name, "r")
        a = file.read()
        file.close()
        if a == "":
            return " "
        else:
            return str(a)
    except:
        return ('Что-то пошло не так')

def rewrite(file_name, content):
    try:
        file = open(file_name, "w")
        file.write(content)
        return "Успешно записано в " + file_name
    except:
        return ('Что-то пошло не так')

def add(file_name, content):
    file = open(file_name, "a")
    file.write(content)
    file.close()
    return "Успешно добавлено в " + file_name

def rename(first_name, second_name):
    try:
        os.rename(first_name,second_name)
        return "Файл " + first_name + " переименован в " + second_name
    except:
        return ('Что-то пошло не так')

def copy(first_name, second_name):
    try:
        shutil.copy(first_name,second_name)
        return "Файл скопирован"
    except:
        return 'Что-то пошло не так'

def move(first_name, second_name):
    try:
        shutil.move(first_name,second_name)
        return "Файл перемещен"
    except:
        return 'Что-то пошло не так'

def help():
    return ("""    Создание папки [команда имя] - mkfold
    Удаление папки по имени [команда имя] - rmfold
    
    Перемещение между папками (в пределах рабочей папки) - заход в папку по имени, выход на уровень вверх [команда путь]- cf
    Переход на 1 папку вверх - "cf -"
    Относительный переход к папке от текущей - "./[путь] или .\\[путь]"
    
    Создание пустых файлов с указанием имени [команда имя] - create
    Запись текста в файл с заменой текста [команда имя текст] - rewrite
    Дозапись текста в файл [команда имя текст] - add
    Просмотр содержимого текстового файла [команда имя] - cet
    Удаление файлов по имени [команда имя] - rmv
    Копирование файлов из одной папки в другую [команда путь1 путь2] - copy
    Перемещение файлов [команда путь1 путь2] - move
    Переименование файлов [команда СтароеИмя НовоеИмя] - rename
    Показать все файлы директории [команда] - list
    Просмотреть текущий путь [команда]- pwd
    Помощь [команда] - help
    Выход [команда] - exit """)



#Здесь нужно указать рабочую директорию(если ничего не указать будет выставлена директория файла). 
# Формат str например: '/Users/olgalengauer/Artem/VScode/Python/Unix'
Path()


#создаем и биндим сокет
PORT=8090
sock=socket.socket()
sock.bind(('', PORT))
sock.listen()

while True:
    print("Слушаем порт", PORT)
    conn, addr=sock.accept()
    print(addr)
    
    request=conn.recv(1024).decode()
    print(request)

    request = request.split()

    #список
    if request[0] == "list":
        otv = list()

    #текущий путь
    elif request[0] == "pwd":
        otv = pwd()
    
    #создание файла
    elif request[0] == "create":
        otv = create(request[-1])
    
    #удалить файл
    elif request[0] == 'rmv':
        otv = rmv(request[-1])
    
    #вызвать помощь
    elif request[0] == 'help':
        otv = help()

    #просмотреть содержимое файла
    elif request[0] == 'cet':
        otv = cet(request[-1])

    #переименовать
    elif request[0] == 'rename':
        otv = rename(request[1],request[-1])

    #записать в файл
    elif request[0] == 'rewrite':
        sum = ""
        for i in range(len(request)):
            if i > 1:
                sum = sum +" "+ request[i]
        otv = rewrite(request[1], sum)

    #дозаписать в файл   
    elif request[0] == 'add':
        sum = ""
        for i in range(len(request)):
            if i > 1:
                sum = sum +" "+ request[i]
        otv = add(request[1], sum)
    
    #перейти в другую папку
    elif request[0] == 'cf':
        otv = cf(request[-1])

    #создание папки
    elif request[0] == 'mkfold':
        otv = mkfold(request[-1])

    #удаление папки
    elif request[0] == 'rmfold':
        otv = rmfold(request[-1])
    
    #копирование файла
    elif request[0] == 'copy':
        otv = copy(request[1], request[-1])

    #передвинуть файлы
    elif request[0] == 'move':
        otv = move(request[1], request[-1])
    
    #выход
    elif request[0] == 'exit':
        sock.close()

    else:
        otv = "Команда введена не правильно"

    conn.send(otv.encode())

    
    
