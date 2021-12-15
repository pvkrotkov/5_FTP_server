import os
import sys
from shutil import copy
import config


def help():
    info = """              \t\t\t\t\tФАЙЛОВЫЙ МЕНЕДЖЕР\n\n

        \t\t\t\t\tДоступныe команды:        \n

    \t dir -- Просмотр содержимого директории. Введите без аргументов для просмотра текущей. (Аналог ls)
    \t fv -- Перемещение между папками. После имени команды укажите директорию для перемещения. (Аналог cd)
    \t crfol -- Создание папки. Через пробел запишите произвольное число имён папок.
    \t rmfol -- Удаление папки. Через пробел напишите какие папки нужно удалить.
    \t crfil -- Создание файла. Через пробел запишите произвольное число имён файлов.
    \t rmfil -- Удаление файлов. Через пробел укажите файлы для удаления.
    \t record -- Запись текста в файл. После имени команды передайте текст для записи, а после - имя файла.
    \t show -- Вывод содержимого файла. В качестве параметров передайте имя файлов, текст из которых нужно вывести.
    \t dupl -- Дублирование файла. Передайте имена файлов, дубликат которых нужно получить.
    \t copy -- Копирование файла. Передайте имена файлов, которые нужно скопировать. Последний аргумент - папка назначения.
    \t move -- Перемещение файла. Сначала укажите файлы, а последним аргументом директорию, в которую их нужно перенести.
    \t rename --  Переименование файла. Первый аргумент - текущее имя файла, второй - новое.
    \t exit -- Выход.
    \t """

    return info


def get_delimiter():
    platform = sys.platform
    if platform.startswith('win'):
        delimiter = '\\'
    else:
        delimiter = '/'
    return delimiter


def crfol(*args):
    folder_names = args
    for name in folder_names:
        if not os.path.isdir(name):
            os.mkdir(name)

    return 'Операция создания успешно выполнена.'


def rmfol(*args):
    folder_names = args
    for name in folder_names:
        if os.path.isdir(name):
            os.rmdir(name)
    return 'Операция удаления успешно выполнена.'


def fv(path='.'):
    cur_dir = os.getcwd()
    try:
        os.chdir(path)
    except:
        return 'Указанный путь не найден.'
    if config.work_dir[1:] in os.getcwd():
        return 'Переход выполнен.'
    else:
        os.chdir(cur_dir)
        return f'Переход вне рабочей дириктории <{config.work_dir}> невозможен!'


def crfil(*args):
    file_names = args
    for name in file_names:
        try:
            open(name, 'x')
        except FileExistsError:
            return f'Файл {name} уже существует.'

    return 'Операция создания успешно выполнена.'


def record(*args):
    try:
        file = args[-1]
        content = ' '.join(args[:-1])
    except IndexError:
        return 'Аргументы для записи не переданы.'
    else:
        with open(file, 'a') as f:
            f.write(content)
    return 'Операция записи успешно выполнена.'


def show(*args):
    file_names = args
    for name in file_names:
        try:
            with open(name, 'r') as file:
                content = f'Содержимое файла {name}: \n {file.read()}'
                return content
        except FileNotFoundError:
            return f'Файл {name} не найден.'
        except IsADirectoryError:
            return f'Ошибка: {name} является директорией, а не файлом.'


def rmfil(*args):
    file_names = args
    for name in file_names:
        try:
            os.remove(name)
        except FileNotFoundError:
            return f'Файл {name} не существует.'

    return 'Операция удаления успешно выполнена.'


def dupl(*args):
    file_names = args
    for name in file_names:
        try:
            with open(name, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            return f'Файл {name} не найден.'

        name_array = name.split('.')
        if len(name_array) > 1:
            new_name = '.'.join(name_array[:-1]) + '-копия.' + name_array[-1]
        else:
            new_name = name_array[-1] + '-копия'
        with open(new_name, 'w') as copy_file:
            copy_file.write(content)

    return 'Операция дублирования успешно выполнена.'


def move(*args):
    # абсолютный путь - начало с /config.work_dir
    # относительный - {a-z}

    delimiter = get_delimiter() # определяем разделитель
    try:
        file_names = args[:-1]
        destination = args[-1]
    except:
        return 'Требуется файлы для перемещения и папка назначения.'
    full_workdir = os.getcwd()[:os.getcwd().index(config.work_dir[1:])]
    for name in file_names:
        try:
            onlyfile_name = name.split(delimiter)[-1] # краткое имя файла
            if (name[:len(config.work_dir)-1] == config.work_dir[1:]):
                name = full_workdir+delimiter+name # полное имя для файла
            else:
                name = os.getcwd() + delimiter + name
            if destination[:len(config.work_dir)-1] == config.work_dir[1:]: # абсолютный путь назначения
                os.replace(name, full_workdir+destination+delimiter+onlyfile_name)
            elif destination == '.':
                os.replace(name, os.getcwd()+delimiter+onlyfile_name)
            elif destination == '..':
                os.replace(name, delimiter.join(os.getcwd().split(delimiter)[:-1])+delimiter+onlyfile_name)
            else:
                os.replace(name, os.getcwd()+delimiter+destination+delimiter+onlyfile_name)
        except FileNotFoundError as e:
            return 'Файл не найден: перемещение в рамках рабочей папки не выполнено.'
    return 'Операция перемещения успешно выполнена.'


def rename(*args):
    try:
        old_name = args[-2]
        new_name = args[-1]
    except IndexError:
        return 'Требуется передать текущее и новое имя файла.'
    else:
        os.replace(old_name, new_name)
    return 'Операция переименования успешно выполнена.'


def cp(*args):
    try:
        file_names = args[:-1]
        destination = args[-1]
    except:
        return 'Требуются файлы для копирования и папка назначения.'
    for name in file_names:
        try:
            copy(name, destination)
        except:
            return f'Файл {name} не был скопирован.'
    return 'Операция копирования успешно выполнена.'


def dir(path='.'):
    content = ' :: '.join(os.listdir(path))
    print(content)
    return content


def loc():
    path = os.getcwd()
    root = config.work_dir[1:]+''.join(path.split(config.work_dir[1:])[1:])
    return root


def exit():
    return '0'
