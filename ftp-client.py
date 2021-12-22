import socket
import threading
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
conn = ('localhost', 9090)

sock.connect(conn)

def help():
    print('''
help - получить справку о командах
newfile <имя файла> - создать новый файл
newfolder <имя папки> - создать новую директорию
rf -file <имя файла> - удалить файл
rf -folder <имя папки> - удалить папку
show <имя папки> - показать содержимое папки
rename <текущее имя файла> <новое имя файла> - изменить имя файла
s_f <имя файла> - получить файл с сервера
rec_f <имя файла> - отправить файл на сервер
    ''')

def rec_f(name, conn):
    try:
        with open(name, 'rb') as handle:
            a = handle.read()
        sock.sendto(a + b'fdata' + bytes(f'{name}', encoding='utf-8'), conn)
        print(f'file {name[0]} sended')
    except:
        print(f'file {name} does not exist!')


def sock_recv(sock):
    while True:
        try:
            c_data = sock.recvfrom(1024)
            if 'fdata' in c_data[0].decode('utf-8'):
                with open(c_data[0][c_data[0].index(b'fdata') + 5::].decode('utf-8'), 'w+') as handle:
                    handle.write(c_data[0].decode('utf-8')[:c_data[0].decode('utf-8').index('fdata'):])
            else:
                print(c_data[0].decode('utf-8'))
        except:
            raise SystemExit

a = threading.Thread(target=sock_recv, args=[sock])
a.start()

print('''
help - получить справку о командах
newfile <имя файла> - создать новый файл
newfolder <имя папки> - создать новую директорию
rf -file <имя файла> - удалить файл
rf -folder <имя папки> - удалить папку
show <имя папки> - показать содержимое папки
rename <текущее имя файла> <новое имя файла> - изменить имя файла
s_f <имя файла> - получить файл с сервера
rec_f <имя файла> - отправить файл на сервер
''')

while True:
    command = input("> ")
    if command.split()[0] == 'rec_f':
        rec_f(command.split()[1], conn)
    elif command == 'help':
        help()
    else:
        sock.sendto(bytes(command, encoding='utf-8'), conn)

    if command.split()[0] == 'quit':
        break
sock.close()
