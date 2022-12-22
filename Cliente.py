from socket import *
from ProtocolCCC import *

host = "127.0.0.1"
port = 40000

ip_port = (host, port)

client = socket(AF_INET, SOCK_STREAM)
client.connect(ip_port)


def receive_message():
    msg_serv = client.recv(1024).decode() # 
    print(msg_serv)
    return msg_serv
    
def send_message():
    
    letra = input().lower().rstrip()
    
    while len(letra)>1:
        letra = input("Digite apenas UMA letra: ").lower().rstrip()
        
    msg_cliente = 'POST ' + letra
    
    client.send(msg_cliente.encode())

receive_message()

if __name__ == "__main__":

    while True:

        msg_serv = receive_message() # Recebe a mensagem de enviar letra

        if msg_serv == '[C-WIN]':
            print(msg_success.get(msg_serv))
            break
        
        elif msg_serv == '[C-SENT]':
            print(msg_success.get(msg_serv))
        
        elif msg_serv == "[C-INSERT]":
            print(msg_game.get(msg_serv))
            send_message()
            
        elif msg_serv == '[C-INVALID]':
            print(msg_error.get(msg_serv))
            
        elif msg_serv == '[C-NONEXISTENT]':
            print(msg_error.get(msg_serv))
        
        elif msg_serv == '[C-LOSE]':
            print(msg_error.get(msg_serv))
            break