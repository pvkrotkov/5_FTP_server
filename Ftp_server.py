import socket
from File_manager_test import *
import os

sock = socket.socket()
sock.bind(('', 9091))
sock.listen(2)

msg = ''

def user_creation(User_name,passwd):
	if User_name not in F_list(''):
		mkdir_py(User_name+'_dir')
		touch(User_name+'.txt')
		edit_file(User_name + '.txt', passwd)
	elif User_name in F_list(''):
		if passwd in User_name+'.txt':
			chdir(User_name+'_dir')
		else:
			resp = 'Incorrect password'
			return resp

while msg != "exit":

	conn, addr = sock.accept()
	print("Connected: ", addr)
	msg = ''
	flag = False
	while True:
		data = conn.recv(1024)
		if not data:
			break
		msg += data.decode()+' '
		request = data.decode().split(' ')

		if flag == False:
			user_creation(request[0], request[1])
			flag = True

		elif request[0] == 'mkdir':
			mkdir_py(request[1])
		elif request[0] == 'remdir':
			dir_rem(request[1])
		elif request[0] == 'touch':
			touch(request[1])
		elif request[0] == 'rm':
			rm(request[1])
		elif request[0] == 'cd':
			chdir(request[1])
		elif request[0] == 'ls':
			List = F_list('')
			data = str(List).encode()
			request = []
		elif request[0] == 'pwd':
			data = cur_dir().encode()
			request = []
		elif request[0] == 'cat':
			data = open_file(request[1]).encode()
			request = []
		elif request[0] == 'copyto':
			copy_folder(request[1],request[2])

		elif request[0] == 'nano':
			file_content = request[2]
			edit_file(request[1],file_content)

		print(request)
		conn.send(data)
	print(msg)

conn.close()