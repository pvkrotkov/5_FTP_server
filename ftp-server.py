import os, shutil, socket

def rename(f_name, conn):
    if "\\" in f_name[1] or len(f_name) > 2:
        sock.sendto(bytes(str(f'invalid input'), encoding='utf-8'), conn)
        return
    else:
        try:
            shutil.move(f_name[0], f_name[1])
        except FileNotFoundError:
            sock.sendto(bytes(str("no such file or directory"), encoding='utf-8'), conn)
        else:
            sock.sendto(bytes(str(f'file {f_name[0]} successfully renamed to {f_name[1]}'), encoding='utf-8'), conn)

def s_f(name, conn):
    try:
        with open(name[0], 'rb') as handle:
            a = handle.read()
        sock.sendto(a + b'fdata' + bytes(f'{name[0]}', encoding='utf-8'), conn)
        sock.sendto(bytes(f'file {name[0]} sended', encoding='utf-8'), conn)
    except:
        sock.sendto(bytes(f'file {name[0]} does not exist!', encoding='utf-8'), conn)

def rf(f_name, conn):
    current = os.getcwd()
    if len(f_name) != 2:
        sock.sendto(bytes(str(f'invalid input'), encoding='utf-8'), conn)
        return
    if f_name[0] == '-file':
        try:
            os.remove(f_name[1])
            sock.sendto(bytes(str(f'file "{f_name[1]}" has been removed'), encoding='utf-8'), conn)
        except FileNotFoundError:
            sock.sendto(bytes(str(f'file "{f_name[1]}" does not exist!'), encoding='utf-8'), conn)
    elif f_name[0] == '-folder':
        try:
            os.chdir(os.getcwd() + "/" + f_name[1])
        except FileNotFoundError:
            sock.sendto(bytes(str(f'the folder "{f_name[1]}" does not exist!'), encoding='utf-8'), conn)
        except IndexError:
            sock.sendto(bytes(str(f'invalid input'), encoding='utf-8'), conn)
        else:
            a = os.listdir()
            os.chdir(current)
            if len(a) != 0:
                while True:
                    sock.sendto(bytes(str(f'{f_name[1]} have {len(a)} objects. Do you want to delete directory and all containing files? Type "y" or "n": '), encoding='utf-8'), conn)
                    a = str(sock.recvfrom(1024)[0].decode('utf-8'))
                    if a == "y" or a == "":
                        shutil.rmtree(f_name[1])
                        sock.sendto(bytes(str(f'directory "{f_name[1]}" deleted with all files'), encoding='utf-8'), conn)
                        break
                    elif a == "n":
                        break
                    else:
                        sock.sendto(bytes(str(f'invalid input'), encoding='utf-8'), conn)
            else:
                sock.sendto(bytes(str(f'directory "{f_name[1]}" deleted'), encoding='utf-8'), conn)
                os.rmdir(f_name[1])

def show(f_name, conn):
    current = os.getcwd()
    a = os.listdir()
    try:
        os.chdir(os.getcwd() + "/" + f_name[0])
    except FileNotFoundError:
        sock.sendto(bytes(str(f'the folder "{f_name[1]}" does not exist!'), encoding='utf-8'), conn)
    except IndexError:
        sock.sendto(bytes(str(f'invalid input'), encoding='utf-8'), conn)
    else:
        sock.sendto(bytes(str(' '.join(os.listdir())), encoding='utf-8'), conn)
        os.chdir(current)

def newfolder(f_name, conn):
    for i in f_name:
        try:
            os.mkdir(i)
            sock.sendto(bytes(str(f'folder "{i}" was created'), encoding='utf-8'), conn)
        except:
            sock.sendto(bytes(str(f'folder "{i}" already exist!'), encoding='utf-8'), conn)

def newfile(f_name, conn):
    a = os.listdir()
    for i in f_name:
        if i in a:
            sock.sendto(bytes(str(f'file "{i}" already exist!'), encoding='utf-8'), conn)
        else:
            new_file = open(i, "w")
            new_file.close()
            sock.sendto(bytes(str(f'the "{i}" file was created'), encoding='utf-8'), conn)
             #recv в threading


func_dict = {'newfile':newfile, 'newfolder':newfolder, 'rf':rf, 'show':show, 'rename':rename, 's_f':s_f}
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(('localhost', 9090))

while True:
    data1 = sock.recvfrom(1024)
    command = (data1[0].decode('utf-8')).split()
    #command = input("> ").split()
    if command[0] == 'quit':
        break
    elif 'fdata' in data1[0].decode('utf-8'):
        with open(data1[0][data1[0].index(b'fdata') + 5::].decode('utf-8'), 'w+') as handle:
            handle.write(data1[0].decode('utf-8')[:data1[0].decode('utf-8').index('fdata'):])
        continue
    elif command[0] in locals() and callable(locals()[command[0]]):
        func_dict[command[0]](command[1::], data1[1])
    else:
        sock.sendto(bytes(str(f'unknown command "{command[0]}"'), encoding='utf-8'), data1[1])
print('break')
sock.close()
