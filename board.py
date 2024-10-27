from frogs import *
class Board:
    def __init__(self,cantidad_de_ranas_por_color:int) -> None:
        self.board=[]
        self.cantidad_de_ranas_por_color=cantidad_de_ranas_por_color
        self.tableroSet(self.board)

    def tableroSet(self,board):
        for i in range(self.cantidad_de_ranas_por_color):
            self.board.append(BlueFrog())
        self.board.append('_')
        for i in range(self.cantidad_de_ranas_por_color):
            self.board.append(RedFrog())
    


    def print(self):
        print(self.board)

Board(3).print()