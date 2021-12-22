import socket

HOST = "127.0.0.1"
PORT = 8080
print (
        'ls <dir>            - посмотреть содержимое папки\n'
        'mkdir <dir>         - создать папку\n'
        'touch <file> - создать файл\n'
        'rm <file/dir>       - удалить файл/папку\n'
        'rename <old> <new>  - переименовать файл\n'
        'cat <file>          - посмотреть содержимое файла\n'
        'copy <file> <dir>   - копировать файл\n'
        'pwd                 - текущий путь\n'
        'help_com            - выводит справку по командам\n'
        'exit                - выход\n'
    )
while True:
    req = input('> ')
    if req == 'exit':
        break
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(req.encode())
    response = sock.recv(1024).decode()
    print(response)
    sock.close()
