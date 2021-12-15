import os
import subprocess
import socket
import logging
import errno
import random
from threading import Thread

"""
Пароль для root: 12345
"""

HOST = "localhost"
PORT = 9090
users = {}

logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w", encoding="UTF-8")

def start_server():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		server.bind((HOST, PORT))
		logging.info(f"Адрес хоста: {HOST}\n Порт хоста: {PORT}")
		print(f"Используемый порт: {PORT}")
	except socket.error as err:
		if(err.errno == errno.EADDRINUSE):
			print("Этот порт уже используется!")
			while True:
				try:
					port = random.randint(0, 65535)
					server.bind((HOST, port))
					logging.info(f"Адрес хоста: {HOST}\n Порт хоста: {port}")
					print(f"Новый порт: {port}")
					break
				except:
					continue
	server.listen()
	return server

def allowed_users():
	with open("users.txt", "r") as file:
		for line in file:
			login, password = line.rstrip("\n").split(";")
			users[login] = password
	print(users)

class FTP_server(Thread):
	"""
	Класс, реализующтий работу FTP сервера.
	"""
	def __init__(self, conn, addr):
		Thread.__init__(self)
		self.__conn = conn
		self.__login = ""

	def __user_add(self):
		self.__login = self.__conn.recv(1024).decode()
		password = self.__conn.recv(1024).decode()
		if(self.__login in users.keys()):
			self.__conn.send("no".encode())
		users[self.__login] = password
		with open("users.txt", "w") as file:
			for data in users.items():
				line = data[0] + ";" + data[1] + "\n"
				file.write(line)
		logging.info(f"Добавлен новый пользователь: {self.__login}")
		path = "./home/" + self.__login
		try:
			os.mkdir(path)
			self.__conn.send("ok".encode())
		except OSError:
			self.__conn.send("no".encode())

	def __user_authorization(self):
		while True:
			self.__login = self.__conn.recv(1024).decode()
			password = self.__conn.recv(1024).decode()
			if (self.__login == "root" and password == "12345"):
				logging.info(f"Пользователь {self.__login} авторизировался!")
				self.__login = ""
				self.__conn.send("ok".encode())
				return
			for data in users.items():
				if(data[0] == self.__login and data[1] == password):
					self.__conn.send("ok".encode())
					logging.info(f"Пользователь {self.__login} авторизировался!")
					return
			self.__conn.send("no".encode())

	def run(self):
		request = self.__conn.recv(1024).decode()
		if(request == "yes"):
			self.__user_add()
		elif(request == "no"):
			self.__user_authorization()
		path = "./home/" + self.__login
		while True:
			request = self.__conn.recv(1024).decode()
			logging.info(f"Пользователь {self.__login} ввел команду: {request}")
			request = request.split()
			if(request == []):
				return 0
			if(request[0] == "pwd"):
				self.__conn.send(path.encode())
			elif(request[0] == "ls"):
				if(len(request) == 1):
					try:
						path = "./home/" + self.__login
						answer = subprocess.check_output(["ls", path]).decode()
						if(answer == ""):
							self.__conn.send("\n".encode())
						self.__conn.send(answer.encode())
					except subprocess.CalledProcessError:
						self.__conn.send("Директория пуста!".encode())
				elif(len(request) == 2):
					try:
						path = "./home/" + self.__login + "/" + request[1]
						answer = subprocess.check_output(["ls", path]).decode()
						self.__conn.send(answer.encode())
					except subprocess.CalledProcessError:
						self.__conn.send("Такой директории не существует!".encode())
			elif(request[0] == "mkdir" or request[0] == "rm"):
				path = "./home/" + self.__login + "/" + request[1]
				answer = subprocess.check_output([request[0], path]).decode()
			elif(request[0] == "cat"):
				path = "./home/" + self.__login + "/" + request[1]
				answer = subprocess.check_output([request[0], path]).decode()
				self.__conn.send(answer.encode())
			elif(request[0] == "help"):
				answer = """
						ls [DIRECTORY]- выводит содержимое каталога
						pwd - выводит путь текущего каталога
						mkdir DIRECTORY - создает каталог
						touch FILE [TEXT] - создает пустой файл или файл с текстом
						rm FILE - удаляет файл
						mv SOURCE DESTINATION - перемещает (переименовывает файл)
						cat FILE - выводит содержимое файла
						help - выводит справку по командам
						exit - разрыв соединения с сервером"""
				self.__conn.send(answer.encode())
			elif(request[0] == "touch"):
				if(len(request) == 2):
					path = "./home/" + self.__login + "/" + request[1]
					answer = subprocess.check_output([request[0], path]).decode()
					with open(path, "a", encoding='utf-8') as file:
						file.write(request[2])
				elif(len(request) == 1):
					path = "./home/" + self.__login + "/" + request[1]
					answer = subprocess.check_output([request[0], path]).decode()
			elif(request[0] == "mv"):
				path = "./home/" + self.__login + "/" + request[1]
				final_path = "./home/" + self.__login + "/" + request[2]
				answer = subprocess.check_output([request[0], path, final_path]).decode()
			elif(request[0] == "exit"):
				answer = "exit"
				self.__conn.send(answer.encode())
			else:
				self.__conn.send("Такой команды не существует!".encode())
			
def main():
	allowed_users()
	sock = start_server()
	while (True):
		conn, addr = sock.accept()
		newClient = FTP_server(conn, addr).start()

if __name__ == "__main__":
	main()