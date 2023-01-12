import socket
import rsa
import threading


public_key, private_key = rsa.newkeys(1024)
public_partner = None

IP = '192.168.100.154'
PORT = 9191
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
client,_=server.accept()
client.send(public_key.save_pkcs1("PEM"))
public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

def send_message(c):
    while True:
        message = input(f'/{client}/~_> ')
        c.send(rsa.encrypt(message.encode(), public_partner))

def receive_message(c):
    while True:
        print(f'\n/{c}/~_> {rsa.decrypt(c.recv(1024), private_key).decode()}')

threading.Thread(target=send_message, args=(client,)).start()
threading.Thread(target=receive_message, args=(client,)).start()