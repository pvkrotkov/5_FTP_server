"""
Все тесты выполнять под root пользователем с паролем 12345
"""
from unittest import TestCase
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "localhost"
PORT = 9090
class tests(TestCase):
	"""
	Тестовые кейсы.
	"""
	def test_pwd(self, login):
		request = "pwd"
		client.send(request.encode())
		response = client.recv(1024).decode()
		if(login != "root"):
			path = "./home/" + login
			self.assertEqual(response, path)
		elif(login == "root"):
			self.assertEqual(response, "./home/")
	
	def test_ls(self):
		"""
		Ответ стоит поменять, если директории в папке home отличны от моих
		"""
		request = "ls"
		client.send(request.encode())
		response = client.recv(1024).decode()
		self.assertEqual(response, "andrey\ntest\nvlad\n") #Положительный тест-кейс
		# self.assertEqual(response, "andrey\nvlad") #Отрицательный

	def test_cat(self):
		request = "cat test"
		client.send(request.encode())
		response = client.recv(1024).decode()
		self.assertEqual(response, "file from test")

def main():
	try:
		client.connect((HOST, PORT))
	except InterruptedError:
		port = int(input("Введите порт сервера: "))
		client.connect((HOST, port))
	while (True):
		guest = str(input("Вы хотите зарегистрироваться или войти (yes/no): "))
		if(guest == "yes"):
			"""
			Создать нового пользователя
			"""
			while True:
				client.send(guest.encode())
				login = str(input("Введите новый логин: "))
				password = str(input("Введите новый пароль: "))
				client.send(login.encode())
				client.send(password.encode())
				if (client.recv(1024).decode() == "ok"):
					print(f"Добро пожаловать, {login}!")
					break
				else:
					print(f"Пользователь с именем {login} уже существует!")
			break
		elif (guest == "no"):
			"""
			Авторизация старого пользователя
			"""
			client.send(guest.encode())
			while (True):
				login = str(input("Введите логин: "))
				password = str(input("Введите пароль: "))
				client.send(login.encode())
				client.send(password.encode())
				if (client.recv(1024).decode() == "ok"):
					print(f"Здравствуйте, {login}!")
					break
				else:
					print(f"Пользователь {login} не найден! Попробуйте снова!")
			break
		else:
			print("Неверная команда!\nПопробуйте снова!")
			continue
	test = tests()
	test.test_pwd(login)
	test.test_ls()
	test.test_cat()





if __name__ == "__main__":
	main()