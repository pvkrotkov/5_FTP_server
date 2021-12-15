import socket

HOST = "localhost"
PORT = 9090

def main():
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
	while True:
		request = input('>')
		client.send(request.encode())
		if(request.split()[0] != "mkdir" and request.split()[0] != "rm" 
			and request.split()[0] != "touch" and request.split()[0] != "mv"):
			response = client.recv(1024).decode()
			if(response == "exit"):
				break
			print(response)
		
	client.close()

if __name__ == "__main__":
	main()