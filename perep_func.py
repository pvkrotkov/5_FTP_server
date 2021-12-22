#функции для обмена сообщениями
#шифрование
def shifr(text, k):
    return ''.join(map(chr, [(x + k) % 65535 for x in map(ord, text)]))


def deshifr(text, k):
    return ''.join(map(chr, [(x - k) % 65535 for x in map(ord, text)]))

def calc_key(key_g, key_ab, key_p):
    return key_g ** key_ab % key_p

#отправление сообщений
def send_mas(drkto, msg, key):

    drkto.send(shifr(msg,key).encode('utf-8'))#+'\n'
#получение
def recive(kto, key, razm=2048):#key_full_s - client

            return deshifr(kto.recv(razm).decode('utf-8'),key)

