import sys
import time
import socket
from TicTacToe import TicTacToe

BUFFER_SIZE=1024

def sleep(t):
    try:
        time.sleep(t)
    except:
        pass

str_usage='Uso: python3 client.py <ip do servidor>:<porta>'
if len(sys.argv) != 2:
    print(str_usage)
    sys.exit(1)
if ':' not in sys.argv[1]:
    print('A porta deve estar presente')
    print(str_usage)
    sys.exit(1)

server_addr=sys.argv[1]
print('conectando ao servidor {}'.format(server_addr))
server_addr=server_addr.split(':')
server_addr=tuple([server_addr[0],int(server_addr[1])])

conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(server_addr)

print('Jogo da velha')
TicTacToe.printPositions()

game=TicTacToe()
try:
    player_piece=conn.recv(1).decode('utf-8')
    for piece in TicTacToe.VALID_PIECES:
        if piece!=player_piece:
            opponent_piece=piece
            break
    print('Jogador jogando a peça {}'.format(player_piece))
    print('Adversário jogando a peça {}'.format(opponent_piece))
    print()
    sleep(1)

    while True:
        state=conn.recv(BUFFER_SIZE)
        game.decode(state)
        game.print()
        if game.finished():
            print('O jogo acabou!')
            break
        print('Jogue com a peça {}:'.format(player_piece))
        TicTacToe.printPositions()
        position=0
        while position <1 or position>9:
            try:
                position=int(input('Digite uma posição no intervalo [1-9]: '))
                if not game.allowedAction(position):
                    print('Jogue em uma posição valida')
                    position=0
            except KeyboardInterrupt:
                break
            except:
                position=0
        game.makeAction(position,player_piece)
        conn.sendall(game.encode())
finally:
    conn.close()