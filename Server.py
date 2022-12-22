import threading
from socket import *
import time
from Game import *

game_started = False # Faz o controle do inicio do jogo
players = {} # guarda os jogadores conectados
mutex_letra = threading.Semaphore(1)  # semaforo do tipo mutex
canPlay = False # Faz o controle de quem pode jogar caso tenha mais players
letter = '' # guarda a letra

# Quantidade de jogadores que irão se conectar e Jogadores conectados
amount_players = int(input("Digite a quantidade de jogadores: "))
connected_players = 0

# Variavel recebendo as palavras que estão em um dicionário
getWordOfGame = Game.getPalavra()
# Separando a palavra da dica
word = getWordOfGame[0] 
tip = getWordOfGame[1]

# Instanciando o objeto game
game = Game(word, tip)

# Enviando mensagem para o cliente
def send_msg(client_socket, msg):
    client_socket.send(bytes(msg, "utf-8"))
    
# Recebendo mensagem do cliente
def receive_msg(con):
    msg = con.recv(1024).decode("utf-8")
    comando, letter = msg.split()
    
    # Mensagem que é enviada pelo o cliente com a letra inserida
    if comando.upper() == "POST":
        return letter
    
    else:
        print("Comando inválido")


# Método que envia mensagens do servidor para todos os clientes conectados
def send_msg_to_all(msg):
    for jogador in players.values():
        jogador.send(bytes(msg, "utf-8"))


# Manipula os cliente
def handlerClient(con, cliente):
    send_msg(con, "Aguarde o jogo começar") # esperando todos os jogadores conectarem

    while not game_started: # enquanto o jogo não começa, o server espera
        time.sleep(1)
    
    while game_started: # chama o change letra
        changeLetra(con)

# Método que recebe jogadores
def get_jogadores(sock):
    global connected_players, amount_players

    print("\nAguardando jogadores...")
    
    # Enquanto a quantidade de jogadores pré-definidas não for a quantidade que tem conectada, o jogo não inicia
    while connected_players != amount_players: # Enquanto o número de jogadores não for igual ao número de jogadores específicados
        client_socket, cliente_adr = sock.accept() # Ele continua aceitando as conexões
        # Ele vai pegar um objeto e esperar uma conexão, assim que o cliente for aceito na conexão, ele irá se conectar. Ele retornará um array, primeiro índice = objeto socket do cliente que se conectou, e o segundo o endereço que ele se conectou 
        
        players[connected_players] = client_socket # o jogador recebendo a permissão
        connected_players += 1 # contando a quantidade de jogadores conectados
        thread = threading.Thread(target=handlerClient, args=(client_socket, cliente_adr)) # Cada cliente vai com uma thread, para que no futuro possamos manusear ela como bem entendermos. 
        thread.start() # Iniciando a thread
        print(f"\n{cliente_adr} conectado... restam {amount_players - connected_players} jogadores para iniciar o jogo.")

# Método que começad o jogo
def showGame():
    global canPlay, game_started, players, mutex_letra
    
    print("\nJogo iniciado...")
    game_started = True
    
    # Mandando informações para todos os clientes
    print(game.getInformations())
    send_msg_to_all(game.getInformations())

    while True:
        # enquanto não descobriu a palavra e a quantidade de tentativas for maior que 0
        while not game.descobriuPalavra(): 
            if canPlay:
                game.rodada(letter)
                
                info_game = game.getInformations()
                
                send_msg_to_all(info_game)
                
                if game.descobriuPalavra():
                    send_msg_to_all("[C-WIN] - Palavra encontrada!") #aqui
                    print(game.
                    hashDisplay())
                    break                
                
                canPlay = False
                
                mutex_letra.release() 
                # Como cada jogador vai possuir uma thread, podemos manipular a vez de tal jogador, já que foram armazenadas em uma variável. 
                # Se for a vez do jogador ele poderá jogar graças ao release, caso não, ele ficará impossibilitado de jogar
                # Assim que o jogador termina de fazer a sua ação, ele liberará a área crítica, diminuindo o release.


def changeLetra(client_socket):
    global mutex_letra, letter, canPlay

    mutex_letra.acquire() # Coloando um jogador na área crítica

    try: 
        send_msg(client_socket, "[C-INSERT]") # envia o input para o cliente inserir a letra

        new_word = receive_msg(client_socket) # recebe a letra do cliente
        
        game.verificarLetra(new_word) # chama o método para verificar o status da letra
        
        letter = new_word # a variavel letra recebe a letra enviada pelo cliente

    except GameException as e: # lança a exceção de que a letra é invalida
        print(str(e))
        
        send_msg(client_socket, "[C-INVALID]") # envia pra quem mandou a mensagem que ela tá invalida
        
        print(game.getInformations())
        send_msg_to_all(game.getInformations())
        mutex_letra.release()
        # Release caso dê erro para ele sair da área crítica
        changeLetra(client_socket)
        
    except ValueError as e: # Lança a exceção de que a letra não existe na palavra
        send_msg(client_socket, "[C-NONEXISTENT]") # envia para o cliente a mensagem do protcolo que a letra não existe
        print(game.getInformations())
        send_msg_to_all(game.getInformations())
        mutex_letra.release()
        time.sleep(1)
        
    else:
        send_msg(client_socket, "[C-SENT]") # Informa ao cliente que a letra foi enviada com sucesso
        canPlay = True # O jogo pode prosseguir
        
      
def main():
    
    HOST =  '0.0.0.0' # IP do Servidor
    PORT = 40000

    sock = socket(AF_INET, SOCK_STREAM) # usando TCP
    sock.bind((HOST, PORT)) 

    sock.listen(amount_players) # Servidor no aguardo da quantidade de clientes
    
    print("\nServidor iniciado...")
    
    get_jogadores(sock) # obtém os clientes conectados no server pra virarem jogadores
    
    showGame() # mostra o jogo


if __name__ == "__main__":
    main()