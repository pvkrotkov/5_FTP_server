#Админские права - имя admin пароль 123
import os

import filemanager_func as f
import socket
from bcrypt import checkpw, hashpw, gensalt
import threading
from contextlib import closing
from perep_func import recive, send_mas, calc_key#, Number_To_Fraze
from random import randint
from datetime import datetime
from time import sleep
#запись логов
def logging (sob):
    file = open(log_nam, 'a')
    file.write(str(datetime.now())+' '+sob+'\n')
    file.close()
#поиск свободного порта
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
#на случай если потребуется добавить ввод адреса сервера в ручную. Сейчас скорее баласт (при шлифовке или допилю до нормальной работы, или уже вырежу наконец-то)
def input_data (maks, chto, ymol):
        while True:
                chis = "ymol"#снять комментарий чтобы получить возможность вводить свой адресс сервера
                #chis = input("Введите " +chto+ " или ymol для значения по умолчанию = "+str(ymol)+ ": ")
                if chis.isdigit(): #нуля до 65535
                        chis = int(chis)
                        if chis > -1 and chis < maks+1:
                                return (chis)
                        else:
                            print("введите число от 0 до " + str(maks))
                elif chis == "ymol":
                        return(ymol)
                else:
                        print("нужно ввести целое число")
    
#обмен необходимой информацией для генерации ключа шифра (доп протоколов шифрования)
def generation(conn, key_prim, key_publ_m):
    key_publ_s = conn.recv(1024)
    sleep(0.2)
    conn.send(str(key_publ_m).encode('utf-8'))
    key_part_s = int(conn.recv(1024))
    key_part_m = calc_key(int(key_publ_s), key_prim, key_publ_m)
    sleep(0.2)
    conn.send(str(key_part_m).encode('utf-8'))
    return calc_key(key_part_s, key_prim, key_publ_m)
#админские команды (тестировались плохо)
def showlog(conn):
    msg=''
    with open(log_nam, 'r') as file:
        for i in file:
            msg +=i
    send_mas(conn, msg)

def clearlog(conn):
    with open(log_nam, 'w') as file:
        file.write('logs clear\n')
def exites(conn):
    global work
    work = False
    for line in connect:#В отдельный поток?
        send_mas(line.conn, 'Сервер был выключен')
    logging('end of work')
    sock.close()
def pause(conn):
    global work
    if work:
        work = False
        send_mas(conn, 'Для продолжения работы введите pause повторно')
        for line in connect:
            send_mas(line.conn, 'Сервер поставлен на паузу. ')
        logging('server on pause')
    else:
        work = True
        for line in connect:
            send_mas(line.conn, 'Сервер снят с паузы.')
        logging('end of pause')

class ConnectionThread(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self.connected = False#подкллючён ли пользователь
        self.whoisit = ''#логин
        self.dop = ''#адресс текущей рабочей папки пользователя (у )
        self.size_max=size_max#Макс доступный объём
        self.size='0'#текущий объём папки
        self.key_full_m=None#ключ шифрования
        self.home=None#адрес домашней папки
        self.loginnnim()#запуск рабочих функций. пришлось переделать в такой вид из-за внезапно вылазящего бага
        self.runnest()
 
    def loginnnim(self):
            self.key_full_m = int(generation(self.conn, randint(128, 1024), randint(128, 1024)))
            send_mas(self.conn, 'Здравствуйте. Представьтесь, пожалуйста', self.key_full_m)
            name = recive(self.conn, self.key_full_m)
            try:#известен ли логин
                file = open(cd+'pas'+name+'.bin', "rb")
                key = file.read()
                file.close()
            except FileNotFoundError:#новый пользователь
                send_mas(self.conn, "Здравствуйте, мы ещё не знакомы. Введите ваш пароль", self.key_full_m)
                key = recive(self.conn, self.key_full_m)
                key = hashpw(bytes(key, encoding='utf-8'), gensalt())#сохранение пароля
                with open(cd+"pas"+str(name)+".bin", "wb") as file:
                    file.write(key)
                key=''
                self.home = (f.os.getcwd()+'\\'+name).split('\\')
                f.mkdir(("\ "[:-1]).join(self.home), '', False, self.dop)
                self.dop = name+'\\'
                logging('new user '+name+' enter the conf from '+str(self.addr))
            else:#пользователь уже известен
                while True:
                    send_mas(self.conn, 'Здравствуйте, '+name+'. Введите ваш пароль', self.key_full_m)
                    msg = recive(self.conn, self.key_full_m)
                    file = open('pas'+name+'.bin', "rb")
                    key = file.read()
                    file.close()
                    if checkpw(bytes(msg, encoding='utf-8'), key):
                        del(key)
                        del(msg)
                        send_mas(self.conn, 'Пароль принят', self.key_full_m)
                        if name == 'admin':
                            self.home = f.os.getcwd().split('\\')
                            logging(name+' enter the from '+str(self.addr))
                            self.size_max=False
                        else:
                            self.home = (f.os.getcwd()+'\\'+name).split('\\')#переписать??
                            self.dop =name+'\\'
                            logging('user '+name+' enter the conf from '+str(self.addr))
                        break
                    else:
                        del(key)
                        send_mas(self.conn, 'Неверный пароль', self.key_full_m)
            home=("\ "[:-1]).join(self.home)
            self.connected = True
            connect.append(self.conn)
            self.whoisit = name
            self.size=str(f.size(home))

    def runnest(self):
        answ=''
        while True:

            while self.connected and (work or self.whoisit=='admin'):
                    if self.whoisit=='admin':#команды для админа. Тестировались плохо, так что скорее всего у админа будет лишь доступ ко всем папкам пользователей (буду тестировать дальше)
                        send_mas(self.conn, self.key_full_m)
                        send_mas(self.conn, "Админские команды: exites - Отключение сервера, pause - остановка прослушивание порта, showlog - Показ логов, clearlog - Очистка логов: ", self.key_full_m)
                    else:#showstor - история сообщений, #, killusers - удалить пароли#openn {name} - содержимое текста; 
                        send_mas(self.conn, "В именах файлов надо писать .txt или проч.\nexitt - выход; pwdd - текущая директория; lss - все папки из в директории; zipuy {name} - зазиповать; dezip {name} - раззиповать; chdirr {name/back} - изменить рабочую директорию; mkdirr {name} - создать директорию; remdirr {name} - удалить директорию; dell {name} - удалить файл; movetoo {name1} {name2} - перенести в указанную директорию; renamee {name1} {name2} - переименовать; copyfilee {name1} {name2} - копировать файл внутри директории; copytoo {name1} {name2} - копировать в другую директорию;", self.key_full_m)
                        send_mas(self.conn, 'Доступно: '+str(self.size)+"/"+str(self.size_max), self.key_full_m)
                    #openn {file_name} - содержимое текста;  copyCS {file_name} - скопировать с клиента на сервер; copySC {file_name} - скопировать с сервера на клиент; touchh {name} - создать файл; 
                    #recive(self.conn, "Доступно: "+str(f.size(self.home))+"/"+str(self.size_max))
                    put = f.os.getcwd()+'\\'+self.dop[:-1] + ': '#получить рабочую директорию
                    send_mas(self.conn, str(put), self.key_full_m)
                    send_mas(self.conn, answ, self.key_full_m)
                    msg = recive(self.conn, self.key_full_m).split(' ')
                    if len(msg) > 0:
                        args = msg[1:]
                    else:
                        args = None
                    msg=msg[0]#команда принятая от пользователя
                    log=False
                    if self.whoisit=='admin' and msg in adminsignal:
                        try:
                            deff=adminsignal[msg]
                        except KeyError:
                            send_mas(self.conn, 'Невыполнимое требование. Проверьте корректность запроса', self.key_full_m)
                            msg, log = deff()
                        if log:
                            logging(self.whoisit+': '+log)
                    elif msg == 'exitt':
                        self.connected = False
                        connect.remove(self.conn)
                        logging('user '+str(self.whoisit)+' exit')
                    elif work:
                        try:
                            deff=signal[msg]
                            if args:#проверка не выходит ли адрес за рамки папки пользователя
                                if False in ([f.analiz(i, self.home, put,self.dop) for i in args]):#не забыть переписать по возможности
                                    answ='Не выходить за пределы папки'
                                elif msg=='chdirr' and len(args)==1:#изменение рабочей директории
                                    #print('chd')
                                    #chdirr {name} - изменить рабочую директорию; mkdirr {name} - создать директорию; remdirr {name} - удалить директорию; touchh {name} - создать файл; dell {name} - удалить файл; movetoo {name1} {name2} - перенести в указанную директорию; renamee {name1} {name2} - переименовать; copyfilee {name1} {name2} - копировать файл внутри директории; copytoo {name1} {name2} - копировать в другую директорию;", self.key_full_m)
                                    #self.dop
                                    if ("\ "[:-1]).join(self.home) == ("\ "[:-1]).join(args[0][:-2].split("\\")):
                                        answ='Не выходить за пределы папки'
                                    elif args[0] != 'back':
                                        self.dop +=args[0]+'\\'
                                        put=f.os.getcwd()+'\\'+self.dop[:-1]
                                        answ='Рабочая директория изменена на '+put
                                        log='new dir'+put
                                    elif self.dop[:-self.dop[::-1][1:].find('\\')-1] != '' or self.whoisit=='admin':
                                        #if self.dop.find('\\') Протестировать
                                        self.dop=self.dop[:-self.dop[::-1][1:].find('\\')-1]
                                        
                                        answ='Возврат к предыдущей директории'
                                        log='new dir'+f.os.getcwd()+'\\'+self.dop[:-1]
                                    else:
                                        answ='Не выходи из папки'
                                else:
                                    if msg in ['copyCS', 'copySC']:#добавление служебных данных для функций
                                        args.append(self.key_full_m)
                                    if msg in ['copyCS', 'dezip', 'mkdirr', 'touchh', 'copyfilee', 'copytoo', 'zipuy']:
                                        args.append(("\ "[:-1]).join(self.home))
                                        args.append(self.size_max)
                                    args.append(self.dop)
                                    answ, log = deff(*args)
                            else:
                                answ, log = deff(self.dop)
                        except TypeError:
                            answ='Неверное количество аргументов'
                        except FileNotFoundError:
                            answ='Требуемый объект не обнаружен'
                        except PermissionError:
                            answ='Доступ запрещён'
                        except KeyError:
                            answ='Невыполнимое требование. Проверьте корректность запроса'
                        except:
                            answ='Невыполнимое требование. Проверьте корректность запроса'
                        if msg in ['copyCS', 'dezip', 'mkdirr', 'touchh', 'copyfilee', 'copytoo', 'remdirr', 'dell', 'zipuy'] and self.whoisit != 'admin':
                            self.size=f.size(("\ "[:-1]).join(self.home))
                        if log:
                            logging(str(self.whoisit)+': '+log)
#список команд для админов и пользователей
signal={'chdirr':f.chdirr,'copyCS': f.sendd, 'copySC': f.recvv, 'openn': f.open_file, 'pwdd': f.current, 'lss': f.isDir, 'mkdirr': f.mkdir, 'remdirr': f.kill_it, 'touchh': f.create, 'dell': f.exterminate, 'zipuy': f.zip_in, 'dezip': f.Unzip, 'movetoo': f.movetoo, 'renamee': f.renamee, 'copyfilee': f.copy_file, 'copytoo': f.copy_folder}
adminsignal={'exites': exites, 'showlog': showlog, 'clearlog': clearlog, 'pause': pause}
try:
    file = open("adress_coda.txt", "r")
    cd = file.read().split('\n')
    file.close()
except FileNotFoundError:
    cd = ''
    cd2 = ''    
else:
    try:
        cd2 = cd[1]
    except IndexError:
        cd2 = ''
    try:
        cd=cd[0]
    except IndexError:
        cd = ''
import sys
sys.path.insert(0, cd)
connect=[]
size_max=1023
sock = socket.socket()
nom = input_data(65535, "vash port", 53480)
try:
    sock.bind(('', nom))
except OSError:
    nom = find_free_port()
    print('Ошибка. Выбранный вами код сервера уже занят, код сервера будет изменён автоматически. Новый код: ', nom)
    sock.bind(('', nom))
log_nam = str(f.os.getcwd())+'\\'+'log_server'+str(nom)+'.txt'
file=open(log_nam, 'w')
file.write('Server activate\nyour port server - '+str(nom)+ '\n')
file.close()
sock.listen(4)
work=True
print("server active")
while work:
        try:
            potok = ConnectionThread(*sock.accept())
            potok.start()
            connect.append(potok)
        except OSError:
            break
