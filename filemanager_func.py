import os
import shutil
import zipfile
#'''
from perep_func import recive, send_mas
#размер папки
def size(path):

    result = 0
    for directory, subdirectory, files in os.walk(path):
        if files:
            for file in files:
                path = directory + '\\'+file
                result += os.path.getsize(path)
    return result
#текущая рабочая директория
def current(dop):
    pathh = os.getcwd()+'\\'+dop[:-1]
    msg= (pathh+'\n')
    pathh = pathh.split('\\')
    return(msg+pathh[len(pathh)-1]+'\n', False)#'''


#'''
def sendd(name, conn, key, userr, max_size, dop):
    length = int(recive(conn, key))#conn.recv(1024).decode()
    text = recive(conn, key, razm=length)#conn.recv(int(length)).decode()
    with open(dop+name) as file:
        file.write(text)
    if max_size and size(userr) > max_size:
        exterminate(name, dop)
        return 'Недостаточно места', False
    return 'получен файл '+name, 'file '+name+' was accepted'


def recvv(name, conn, key, dop):
    with open(dop+name) as file:
        text = file.read()
    send_mas(conn, str(len(text)), key)
    #conn.send(str(len(text)).encode())
    send_mas(conn, text, key)
    #conn.send(text.encode())
    return 'отправлен файл '+name,  'file '+name+' was sent'

def chdirr(dir_name):
    if dir_name != 'back':
        os.chdir(dir_name)
        print(f'Рабочая директория изменена на {dir_name}.')
    else:
        os.chdir('..')
        print('Возврат к предыдущей директории')


#'''

#зазиповать файл
def zip_in(file_name, userr, max_size, dop):
    try:
        if zipfile.is_zipfile(dop+file_name):
            return('Он уже зазипован', False)
        else:
            z = zipfile.ZipFile(dop+file_name.split('.')[0]+'.zip', 'w')
            z.write(dop+file_name)
            z.close()
            if max_size and size(userr) > max_size:
                exterminate(file_name, dop)
            return(file_name+' файл успешно зазипован', file_name+' was zipped')
    except FileNotFoundError:
            return('Не получилось найти файл', False)
#раззиповать
def Unzip (file_name, userr, max_size, dop):
    try:
        if zipfile.is_zipfile(dop+file_name):
            z = zipfile.ZipFile(dop+file_name, 'r')
            z.extractall()
            if max_size and size(userr) > max_size:
                    zip_in(file_name, dop)
                    return 'Недостаточно места', False
            return(file_name+' файл успешно раззипован', file_name+' was dezipped')
        else:
            return('Не, это не зип', False)
    except FileNotFoundError:
            return('Не получилось найти файл', False)

#удалить директорию
def kill_it(dir_name, dop):#zashity ot duraka
    os.rmdir(dop+dir_name)
    return('Директория '+dir_name+' удалена', dir_name+' was delet')
#создать
def mkdir(dir_name, userr, max_size, dop):
    if not os.path.isdir(dop+dir_name):
        os.umask(0)
        os.mkdir(dop+dir_name,0o777)
        #os.chdir('..')
        if max_size and size(userr) > max_size:
                kill_it(dir_name, dop)
                return 'Недостаточно места', False
        return('Директория с именем '+dir_name+' создана', 'dir'+dir_name+' was created')
    else:
        return('Нельзя сотворить две директории с одинаковыми именами!', False)
#содержимое файла
def isDir(dop):
    spicokk = os.listdir(dop)
    msg=''
    for i in (spicokk):
        msg+=str(i)+' '
        print(msg)
    return(msg+'\n', False)
#создание файла
def create(file_name, userr, max_size, dop):
    if not os.path.isfile(dop+file_name):
        text_file = open(dop+file_name, 'w+')
        text_file.write('')
        os.startfile(dop+file_name)
        if max_size and size(userr) > max_size:
            exterminate(file_name, dop)
            return 'Недостаточно места', False
        return('Сделаем!', 'file '+file_name+' was created')
    else:
        return('Здесь нельзя строить!', False)
#'''
def open_file(file_name, dop):
    msg=''
    try:
        os.startfile(dop + file_name)
    except FileNotFoundError:
            return('Не получилось найти файл', False)
            #'''
#переименование
def renamee(old_Fname, new_Fanme, dop):
    try:
        os.rename(dop+old_Fname, dop+new_Fanme)
    except PermissionError:
        return('Неудалось переименовать файл в ' +old_Fname, False)
    except:
        return('Мы не смогли найти '+old_Fname, False)
    else:
        return(old_Fname, 'Был переименован в', new_Fanme)
#удаление файла
def exterminate(file_name, dop):
    os.remove(dop+file_name)
    return('Файл с именем', file_name, 'был удален')
#перемещение файла
def movetoo(file_name, dir_name, dop):
    try:
        os.replace(dop+file_name, dop+dir_name+'/'+file_name)
    except FileNotFoundError:
        try:
            os.replace(dop+file_name, dop[:dop.find('/')]+dir_name+'/'+file_name)
        except FileNotFoundError:
            return('Не получилось найти файл', False)
    return('Файл '+file_name+' был перемещён в директорию '+dir_name)
#копирование
def copy_file(file_name, second_file, userr, max_size, dop):
    try:
        shutil.copyfile(dop+file_name, dop+second_file)
    except FileNotFoundError:
            return('Не получилось найти файл', False)
    if max_size and size(userr) > max_size:
            exterminate(second_file, dop)
            return 'Недостаточно места', False
    return('Файл '+file_name+' скопирован', 'file '+file_name+' like '+second_file)

def copy_folder(file_name, dir_name, userr, max_size, dop):
    if os.path.isdir(dop+dir_name):
        try:
            if max_size and size(userr)+os.path.getsize(dop+file_name) > max_size:
                return 'Недостаточно места', False
        except FileNotFoundError:
            return('Не получилось найти файл', False)
        try:
            shutil.copy(dop+file_name, dop+dir_name)
        except FileNotFoundError:
            try:
                shutil.copy(dop+file_name, dop[:dop.find('/')]+dir_name)
            except FileNotFoundError:
                return('Не получилось найти файл', False)
        return('Файл '+file_name+' был скопирован в директорию '+dir_name)
    else:
        return('Не получилось найти директорию', False)
def analiz(cell, home, put,dop):

    put = put[:-2].split('\\')
    cell = cell.split('\\')
    if  len(put)<len(home):

        return(False)
    #el
    if cell[0] != home[0] and (cell[-1][-1] == ":"):
        return(False)
    else:#'''
        #cel =
        k=0
        for i in home:
            #print(i, cel[k])
            if i != put[k]:
                return(False)
            k +=1
    dop=dop.split('\\')
    for i in cell:
        if i in home and (i in dop)==False:
            return(False)
    return(True)#'''
