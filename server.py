import socket
import random as rd
import urllib.request
from TicTacToe import TicTacToe

BUFFER_SIZE=1024

def appendToStrIfNotNone(base_str,prefix):
    if base_str is None:
        return None
    return prefix+base_str

def getExternalIp():
    try:
        return urllib.request.urlopen('https://checkip.amazonaws.com').read().decode('utf8').strip()
    except:
        return None

def getInternalIp():
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        sock.connect(('10.255.255.255', 1))
        ip=sock.getsockname()[0]
    except Exception:
        ip=None
    finally:
        sock.close()
    return ip

def listenSinglePlayer(sock):
    try:
        sock.listen(1)
        while True:
            print('Esperando jogador...')
            conn,cli_addr=sock.accept()
            try:
                print('Jogador conectado: {}'.format(cli_addr))
                game=TicTacToe()
                pieces=list(TicTacToe.VALID_PIECES)
                rd.shuffle(pieces)
                computer_piece=pieces[0]
                player_piece=pieces[1]
                conn.sendall(player_piece.encode('utf-8'))
                while True:
                    conn.sendall(game.encode())
                    state=conn.recv(BUFFER_SIZE)
                    if not state:
                        print('Conexao interrompida')
                        break
                    game.decode(state)
                    game.print()
                    if game.finished():
                        print('O jogo acabou!')
                        conn.close()
                        break
                    game.computerAction(computer_piece)
                    game.print()
            finally:
                conn.close()
    except Exception as e:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

def getNextPlayer(current_player):
    return (current_player+1)%2

def listenMultiplayer(sock):
    try:
        sock.listen(2)
        while True:
            players=[]
            print('Esperando jogadores...')
            for i in range(2):
                conn,cli_addr=sock.accept()
                print('Jogador {} conectado: {}'.format(i+1,cli_addr))
                players.append(conn)
            try:
                rd.shuffle(players)
                game=TicTacToe()
                pieces=list(TicTacToe.VALID_PIECES)
                rd.shuffle(pieces)
                for i,player in enumerate(players):
                    player.sendall(pieces[i].encode('utf-8'))
                current_player=0
                while True:
                    players[current_player].sendall(game.encode())
                    state=players[current_player].recv(BUFFER_SIZE)
                    if not state:
                        print('Conexao interrompida')
                        break
                    game.decode(state)
                    game.print()
                    if game.finished():
                        print('O jogo acabou!')
                        players[getNextPlayer(current_player)].sendall(game.encode())
                        for player in players:
                            player.close()
                        break
                    current_player=getNextPlayer(current_player)

            finally:
                for player in players:
                    player.close()
    except Exception as e:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()


print('Jogo da velha')
TicTacToe.printPositions()

players=0
while players <1 or players>2:
    try:
        players=int(input('Deseja iniciar o servidor para 1 ou para 2 jogares [1-2]? '))
    except KeyboardInterrupt:
        break
    except:
        players=0

port=8686
print('Subindo o servidor na porta {}'.format(8686))

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address=('0.0.0.0', 8686)
sock.bind(server_address)

ips=['127.0.0.1',getInternalIp(),appendToStrIfNotNone(getExternalIp(),'Via internet: ')]
ips=list(filter(None.__ne__, ips)) 

print('Servidor ligado em todos os ips disponiveis (0.0.0.0) na porta {}, você pode acessar o servidor através dos endereços abaixo:'.format(port))
for ip in ips:
    print('\t{}:{}'.format(ip,port))
print()
if players==1:
    listenSinglePlayer(sock)
else:
    listenMultiplayer(sock)
