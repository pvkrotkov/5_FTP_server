import socket, os, random, csv, shutil

sock = socket.socket()
main_folder = r'D:\Projects\PycharmProjects\FTP Server\home'

def bind_addres(sock):
    port = 12345
    while True:
        try:
            sock.bind(('127.0.0.1', port))
            print(f"In 127.0.0.1 used port - {port}")
            break
        except OSError:
            port = random.randint(1024, 65535)


def server_listening(sock):
    sock.listen(0)


def accept_connections(sock):
    conn, addr = sock.accept()
    client_connected = f'{addr[1]} connected'
    print(client_connected)
    with open('connects_log.txt', 'a+') as file:
        file.write(client_connected + '\n')
    listening_auth(conn, addr)


def registration(conn, addr):
    conn.send(f'>You first time with us, just sign up. Create your login and password'.encode())
    login = conn.recv(1024).decode()
    with open('registration_base.csv', 'a+') as file:
        read_file = csv.reader(file, delimiter=';')
        data = list(read_file)
    for row in data:
        if row[1] == login:
            conn.send('This login already used'.encode())
        else:
            break

    password = conn.recv(1024).decode()
    conn.send(f'>You welcome {login}!'.encode())
    os.mkdir(fr'{main_folder}\{login}')
    with open('registration_base.csv', 'a+') as file:
        csv.writer(file, delimiter=';', lineterminator='\n').writerow((addr[1], login, password))

    return login, password

def authorization(conn, addr, login,password):
    conn.send(f'Hey, {login}, enter your password, please'.encode())
    password_input = conn.recv(1024).decode()
    if password == password_input:
        conn.send(f'Welcome {login}!'.encode())
        return True
    elif password == 'admin':
        conn.send('You logged in on admin'.encode())
        return True
    else:
        return authorization(conn, addr, login, password)



class command_processing:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

        

    def path_reader(self, path):
        self.path = path
        if password == 'admin':
            self.path = main_folder
            if self.path == fr'{main_folder}\..' or self.path == fr'{main_folder}\..\..' or self.path == fr'{main_folder}\..\..\..':
                return False
            else:
                return True
        else:
            if self.path == main_folder or self.path == fr'{main_folder}\..' or self.path == fr'{main_folder}\..\..' or self.path == fr'{main_folder}\..\..\..':
                self.conn.send('Incorrect folder')
                return False
            else:
                return True

    def menu(self, command):

        self.command = command
        print(self.command)
        self.conn.send("""
        >>>Commands Menu<<<
        ls - look content in folder
        mkdir - create the folder
        rmdir - delete the folder
        remove - delete the file
        ccopy - copy file from server to client
        scopy - copy file from client to server
        exit - exit
        """.encode())
        if self.command[0] == 'ls':
            if command_processing.commands(self.conn, self.addr, self.command).folder_contents():
                self.conn.send('Successful'.encode())
        elif self.command[0] == 'mkdir':
            if command_processing.commands(self.conn, self.addr, self.command).create_folder():
                self.conn.send('Successful'.encode())
        elif self.command[0] == 'rmdir':
            if command_processing.commands(self.conn, self.addr, self.command).delete_folder():
                self.conn.send('Successful'.encode())
        elif self.command[0] == 'remove':
            if command_processing.commands(self.conn, self.addr, self.command).delete_file():
                self.conn.send('Successful'.encode())
        elif self.command[0] == 'ccopy':
            if command_processing.commands(self.conn, self.addr, self.command).copy_file_from_server():
                self.conn.send('Successful'.encode())
        elif self.command[0] == 'scopy':
            if command_processing.commands(self.conn, self.addr, self.command).copy_file_from_client():
                self.conn.send('Successful'.encode())
        elif self.command[0] == 'exit':
            self.conn.close()

    class commands:
        def __init__(self, conn, addr, command):
            self.conn = conn
            self.addr = addr
            self.command = command

        def folder_contents(self):
            if len(self.command) == 1:
                try:
                    result = os.listdir()
                    for i in result:
                        self.conn.send(f'{i} '.encode())
                except FileNotFoundError:
                    self.conn.send('Incorrect folder'.encode())
            elif len(self.command) > 1:
                for i in self.command[1:]:
                    path = os.path.abspath(i)
                    if command_processing(self.conn, self.addr).path_reader(path):
                        try:
                            result = os.listdir(i)
                            for i in result:
                                self.conn.send(f'{i} ')
                        except FileNotFoundError:
                            self.conn.send('Incorrect folder'.encode())
                    else:
                        self.conn.send('Incorrect folder'.encode())
            else:
                self.conn.send('Incorrect folder'.encode())

        def create_folder(self):
            if len(self.command) == 2:
                path = os.path.abspath(self.command[1])
                if command_processing(self.conn, self.addr).path_reader(path):
                    try:
                        os.mkdir(self.command[1])
                        return True
                    except OSError:
                        self.conn.send('Incorrect folder'.encode())
                else:
                    self.conn.send('Incorrect folder'.encode())
            elif len(self.command) > 2:
                for i in self.command[1:]:
                    path = os.path.abspath(i)
                    if command_processing(self.conn, self.addr).path_reader(path):
                        try:
                            os.mkdir(i)
                            return True
                        except OSError:
                            self.conn.send('Incorrect folder'.encode())
            else:
                self.conn.send('Incorrect folder'.encode())

        def delete_folder(self):
            if len(self.command) == 2:
                path = os.path.abspath(self.command[1])
                if command_processing(self.addr, self.conn).path_reader(path):
                    try:
                        os.rmdir(self.command[1])
                        return True
                    except OSError:
                        self.conn.send('Incorrect folder'.encode())
                else:
                    self.conn.send('Incorrect folder'.encode())
            elif len(self.command) > 2:
                for i in self.command[1:]:
                    path = os.path.abspath(i)
                    if command_processing(self.addr, self.conn).path_reader(path):
                        try:
                            os.rmdir(i)
                            return True
                        except OSError:
                            self.conn.send('Incorrect folder'.encode())
                    else:
                        self.conn.send('Incorrect folder'.encode())

            else:
                self.conn.send('Incorrect folder'.encode())

        def delete_file(self):
            if len(self.command) == 2:
                path = os.path.abspath(self.command[1])
                if command_processing(self.addr, self.conn).path_reader(path):
                    try:
                        os.remove(self.command[1])
                        return True
                    except OSError:
                        self.conn.send('Incorrect file'.encode())
                else:
                    self.conn.send('Incorrect file'.encode())
            elif len(self.command) > 2:
                for i in self.command[1:]:
                    path = os.path.abspath(i)
                    if command_processing(self.addr, self.conn).path_reader(path):
                        try:
                            os.remove(i)
                            return True
                        except OSError:
                            self.conn.send('Incorrect file'.encode())
                    else:
                        self.conn.send('Incorrect file'.encode())
            else:
                self.conn.send('Incorrect file'.encode())

        def rename_file(self):
            if len(self.command) == 2:
                path = os.path.abspath(self.command[1])
                if command_processing(self.addr, self.conn).path_reader(path):
                    try:
                        os.rename(self.command[1])
                        return True
                    except FileNotFoundError:
                        self.conn.send('Incorrect file'.encode())
                else:
                    self.conn.send('Incorrect file'.encode())
            elif len(self.command) > 2:
                for i in self.command[1:]:
                    path = os.path.abspath(i)
                    if command_processing(self.addr, self.conn).path_reader(path):
                        try:
                            os.rename(i)
                            return True
                        except FileNotFoundError:
                            self.conn.send('Incorrect file'.encode())
                    else:
                        self.conn.send('Incorrect file'.encode())
            else:
                self.conn.send('Incorrect file'.encode())

        def copy_file_from_client(self):
            if len(self.command) == 3:
                path = os.path.abspath(self.command[1])
                if command_processing(self.addr, self.conn).path_reader(path):
                    try:
                        shutil.copy(self.command[1], r'D:\Projects\PycharmProjects\FTP Server\server')
                        return True
                    except FileNotFoundError:
                        self.conn.send('Incorrect file'.encode())
                else:
                    self.conn.send('Incorrect file'.encode())
            else:
                self.conn.send('Incorrect file'.encode())

        def copy_file_from_server(self):
            if len(self.command) == 3:
                path = os.path.abspath(self.command[1])
                if command_processing(self.addr, self.conn).path_reader(path):
                    try:
                        shutil.copy(fr'D:\Projects\PycharmProjects\FTP Server\server\{self.command[1]}', self.command[2])
                        return True
                    except FileNotFoundError:
                        self.conn.send('Incorrect file'.encode())
                else:
                    self.conn.send('Incorrect file'.encode())
            else:
                self.conn.send('Incorrect file'.encode())

def server_chat(conn, addr):
    while True:
        request = conn.recv(1024).decode()
        print(f'Client{addr[1]}: {request}')
        if not request:
            break
        command_processing(conn, addr).menu(request.split())



def listening_auth(conn, addr):
    global password
    with open('registration_base.csv', 'r') as clients_data:
        clients_data.seek(0)
        read_clients_data = csv.reader(clients_data, delimiter=';')
        data = list(read_clients_data)

    for row in data:
        if row[0] == addr[1]:
            login, password, = row[1], row[2]
            break
        else:
            login, password = registration(conn, addr)



    if authorization(conn, addr, login, password):
        if password == 'admin':
            os.chdir(fr'{main_folder}')
        else:
            os.chdir(fr'{main_folder}\{login}')
        server_chat(conn, addr)
    else:
        print('Authentication failed')
        conn.close()

def main():
    bind_addres(sock)
    server_listening(sock)
    accept_connections(sock)


if __name__ == '__main__':
    main()



