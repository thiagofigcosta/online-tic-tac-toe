import os
import math
import random as rd

class TicTacToe:
    VALID_PIECES=('x','o')
    EMPTY_PIECE=' '

    def __init__(self):
        self.board=[TicTacToe.EMPTY_PIECE for _ in range(9)]

    def clearScreen(self):
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def encode(self):
        board_to_send='|'.join(self.board)
        board_to_send='B'+board_to_send
        return board_to_send.encode('utf-8')

    def decode(self, data):
        received_board=data.decode('utf-8')
        if len(received_board) > 0 and received_board[0]=='B':
            received_board=received_board[1:]
            self.board=received_board.split('|')

    def print(self):
        self.clearScreen()
        print('Configuraçao atual do jogo:')
        for i in range(0,len(self.board),3):
            if i!=0:
                print("-----")
            print('{}|{}|{}'.format(self.board[i+0],self.board[i+1],self.board[i+2]))
        print()
    
    @staticmethod
    def printPositions():
        print(' 1 | 2 | 3')
        print('---+---+---')
        print(' 4 | 5 | 6')
        print('---+---+---')
        print(' 7 | 8 | 9')

    def allowedAction(self, position):
        return self.board[position-1] == TicTacToe.EMPTY_PIECE

    def makeAction(self, position, piece):
        if position < 1 or position > 9:
            raise RuntimeError('Posição {} invalida. As posições do tabuleiro devem obedecer ao intervalo [1-9].'.format(position))
        if not self.allowedAction(position):
            raise RuntimeError('Já existe uma peça nessa posição ({}) do tabuleiro'.format(position))

        piece=piece.lower()
        if piece not in TicTacToe.VALID_PIECES:
            raise RuntimeError('Peça {} inválida.'.format(piece))

        self.board[position-1]=piece

    def computerAction(self, piece):
        empty_places=[]
        for i,placed in enumerate(self.board):
            if placed == TicTacToe.EMPTY_PIECE:
                empty_places.append(i+1)
        choice=empty_places[math.floor(rd.random()*len(empty_places))]
        self.makeAction(choice,piece)

    def finished(self):
        # horizontal
        if self.board[0]!=TicTacToe.EMPTY_PIECE and self.board[0]==self.board[1] and self.board[1]==self.board[2] and self.board[2]==self.board[0]:
            return True 
        if self.board[3]!=TicTacToe.EMPTY_PIECE and self.board[3]==self.board[4] and self.board[4]==self.board[5] and self.board[5]==self.board[3]:
            return True 
        if self.board[6]!=TicTacToe.EMPTY_PIECE and self.board[6]==self.board[7] and self.board[7]==self.board[8] and self.board[8]==self.board[6]:
            return True 
        # vertical
        if self.board[0]!=TicTacToe.EMPTY_PIECE and self.board[0]==self.board[3] and self.board[3]==self.board[6] and self.board[6]==self.board[0]:
            return True 
        if self.board[1]!=TicTacToe.EMPTY_PIECE and self.board[1]==self.board[4] and self.board[4]==self.board[7] and self.board[7]==self.board[1]:
            return True 
        if self.board[2]!=TicTacToe.EMPTY_PIECE and self.board[2]==self.board[5] and self.board[5]==self.board[8] and self.board[8]==self.board[2]:
            return True 
        # diagonal
        if self.board[0]!=TicTacToe.EMPTY_PIECE and self.board[0]==self.board[4] and self.board[4]==self.board[8] and self.board[8]==self.board[0]:
            return True 
        if self.board[6]!=TicTacToe.EMPTY_PIECE and self.board[2]==self.board[4] and self.board[4]==self.board[6] and self.board[6]==self.board[2]:
            return True 
        # tie
        tied=True
        for place in self.board:
            if place==TicTacToe.EMPTY_PIECE:
                tied=False
        return tied