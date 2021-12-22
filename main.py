import socket
import os
import shutil



def listtostr(lst):
    sp = ''
    for i in lst:
        sp += i
        sp += '  '
    return sp




dirname = os.path.join('/Users/Aram/Downloads/fileman')


def process(req):
    if req == 'pwd':
        return dirname

    elif req == 'ls':
        return listtostr(os.listdir(dirname))

    elif req[:5] == 'mkdir':
        name = req[6:]
        new_path = dirname + os.sep + name
        os.mkdir(new_path)
        return 'Готово!'

    elif req[:5] == 'rmdir':
        name = req[6:]
        dirrr = dirname + os.sep + name
        shutil.rmtree(dirrr)
        return 'Готово!'

    elif req[:6] == 'remove':
        name = req[7:]
        dirrr = dirname + os.sep + name
        os.remove(dirrr)
        return 'Готово!'

    elif req[:6] == 'rename':
        new_sp = req.split(' ')
        naming = new_sp[1]
        new_name = new_sp[2]
        os.rename(dirname + os.sep + naming, dirname + os.sep + new_name)
        return 'Переименовано!'

    elif req == 'exit':

        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        return 'Closed'




    return 'bad request'


PORT = 6702


sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

while True:


    conn, addr = sock.accept()

    request = conn.recv(1024).decode()
    print(request)
    if request != 'exit':

        response = process(request)
        conn.send(response.encode())

    else:
        response = 'Отключён'
        conn.send(response.encode())
        break



conn.close()




