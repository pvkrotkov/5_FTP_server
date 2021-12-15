import os
import pickle
import shutil
import logging
import json

# from settings import PATH

# PATH = os.path.join(os.getcwd(), 'docs')
# os.chdir("/docs")
logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', filename="logs/ftp-server.log", level=logging.DEBUG)
log = logging.getLogger("immortal-qQ 's SERVER")
PATH = os.getcwd()
print(PATH)


def get_curr_path(username):
    with open("users.json", "r") as f:
        temp = json.load(f)
        return temp["users"][username]["path"]


def set_curr_path(username, path):
    with open("users.json", "r") as f:
        js_file = json.load(f)

    target = js_file["users"][username]
    # if path == "..":
    #
    target["path"] = username + "/" + path

    with open("users.json", "w") as file:
        json.dump(js_file, file, indent=4)


def copy_file(name):
    return pickle.dumps(name)


# def files_in_curr_directory():
#     file_list = '; '.join(os.listdir())
#     if file_list == "":
#         return "Папка пуста"
#     else:
#         return file_list


def files_in_curr_directory(username):
    file_list = '; '.join(os.listdir("docs/" + get_curr_path(username)))
    if file_list == "":
        return "Папка пуста"
    else:
        return file_list


# def current_dir():
#     return os.getcwd().replace("D:\Programming\Python\pi195-workshoppython-Amikuto\\7-Task", "/")
#
#
# def create_new_user_folder(username):
#     os.mkdir("D:\Programming\Python\pi195-workshoppython-Amikuto\\7-Task\docs\\" + username)


def create_folder(username, name):
    """
    создает папку в текущей директории
    :param name:
    :return:
    """
    try:
        path = "docs/" + get_curr_path(username) + "/"
        os.mkdir(path + name)
        log.info(f"Пользователь {username} создал папку {name} в директории: {path}")
        return f"Папка {name} создана!"
    except OSError:
        logging.warning("Ошибка в создании папки!")
        return "Папку создать не удалось!"


def delete_folder(username, name):
    """
    удаляет папку в текущей директории
    :param name:
    :return:
    """
    print(name)
    try:
        os.rmdir("docs/" + get_curr_path(username) + "/" + name)
        return f"Папка {name} удалена!"
    except OSError:
        logging.warning("Ошибка в удалении папки!")
        return "Удалить папку не удалось!"


def change_dir(path):
    """
    изменяет текущую директорию
    :param path:
    :return:
    """
    global curr_path

    if os.getcwd().split("\\")[-1] == "2-Task" and path == "..":
        return "Ошибка! Выход за пределы директории"
    else:
        try:
            if path == "..":
                x = os.getcwd().split("\\")
                os.chdir(path)
                curr_path = curr_path.replace("\\" + x[-1], "")
                return "Текущая директория -", curr_path
            else:
                os.chdir(path)
                x = os.getcwd().split("\\")
                curr_path = curr_path + "\\" + x[-1]

                return "Текущая директория - ", curr_path
        except FileNotFoundError:
            logging.warning("Ошибка в изменении текущей директории!")
            return "Ошибка! Либо папка указана неверно, либо такой папки не существует"


def create_file(username, file_name):
    """
    создает новый файл
    :param username:
    :param file_name:
    :return:
    """
    try:
        open("docs/" + username + "/" + file_name, "w", encoding="UTF-8").close()
        return f"Файл {file_name} создан!"
    except Exception:
        logging.warning("Ошибка в создании нового файла!")
    # my_file.close()


def add_text_to_file(file_name, text):
    """
    добавляет текст в конец файла
    :param file_name:
    :param text:
    :return:
    """
    try:
        with open(file_name, "a") as f:
            data = text + "\n"
            f.write(data)
    except IOError:
        logging.warning(f"Ошибка в добавлении текста в файл {file_name}!")
        return "Возникла ошибка IOError!"


def show_text(username, file_name):
    """
    показывает содержимое файла
    :param username:
    :param file_name:
    :return:
    """
    try:
        with open("docs/" + username + "/" + file_name, "r") as f:
            text = f.read()
            return text
    except IOError:
        logging.warning(f"Ошибка в выводе содержимого файла {file_name}!")
        return "Возникла ошибка IOError!"


def remove_file(username, file_name):
    """
    удаляет файл в текущей директории
    :param username:
    :param file_name:
    :return:
    """
    try:
        os.remove("docs/" + get_curr_path(username) + "/" + file_name)
        return f"Файл {file_name} удалена!"
    except OSError:
        logging.warning(f"Ошибка в удалении файла {file_name}!")
        return f"Удалить папку с названием {file_name} не удалось!"


def copy_file(file_name, new_file_name):
    """
    копирует файлы
    :param file_name: название текущего файла
    :param new_file_name: название нового файла
    :return:
    """
    path = curr_path + "\\" + new_file_name
    shutil.copyfile(file_name, path)


def move_file(file_name, path):
    """
    Перемещает файл в новую директорию
    :param file_name:
    :param path:
    :return:
    """
    new_dir = os.path.join(curr_path, path)
    check_path(new_dir)
    shutil.move(file_name, path)
    logging.info("Файл перемещен!")


def rename_file(username, file_name, new_file_name):
    """
    Изменяет название файла
    :param username:
    :param file_name:
    :param new_file_name:
    :return:
    """
    try:
        os.rename("docs/" + get_curr_path(username) + "/" + file_name, new_file_name)
        return f"Файл {file_name} изменен на {new_file_name}"
    except Exception:
        return f"Удалить файл не удалось!"


def check_path(path) -> bool:
    if path not in PATH:
        return True
    else:
        return False
