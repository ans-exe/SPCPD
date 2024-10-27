class Frog:
    def __init__(self,index) -> None:
        self.index=index
    def moveStep(board):
        pass
    def moveTwoSteps(board):
        pass

class RedFrog(Frog):

    def move(self, board):
        pass

    def moveStep(self, board):
        # Encuentra el índice actual de la rana en el tablero
        current_index = board.index(self.index)

        # Calcula el nuevo índice restando 1
        new_index = current_index - 1
        if self.isValidMove(board):

        # Intercambia las posiciones entre la rana y la celda vacía '_'
            board[current_index], board[new_index] = board[new_index], board[current_index]
    
    def moveTwoStep(self, board):
        # Encuentra el índice actual de la rana en el tablero
        current_index = board.index(self.index)

        # Calcula el nuevo índice restando 1
        new_index = current_index - 2

        if self.isValidMove(board):

        # Intercambia las posiciones entre la rana y la celda vacía '_'
            board[current_index], board[new_index] = board[new_index], board[current_index]

    def isValidMove(self, board):
        # Encuentra el índice actual de la rana en el tablero
        current_index = board.index(self.index)

        # Calcula el nuevo índice restando 1
        new_index = current_index - 1

        # Si el índice es válido, entonces es un movimiento válido
        return new_index >= 0 and board[new_index] == '_'

class BlueFrog(Frog):
    def moveStep(self, board):
        # Encuentra el índice actual de la rana en el tablero
        current_index = board.index(self.index)

        # Calcula el nuevo índice restando 1
        new_index = current_index + 1
        if self.isValidMove(board):
        # Intercambia las posiciones entre la rana y la celda vacía '_'
            board[current_index], board[new_index] = board[new_index], board[current_index]

    def moveTwoStep(self, board):
        # Encuentra el índice actual de la rana en el tablero
        current_index = board.index(self.index)

        # Calcula el nuevo índice restando 1
        new_index = current_index + 2
        if self.isValidMove(board):

        # Intercambia las posiciones entre la rana y la celda vacía '_'
            board[current_index], board[new_index] = board[new_index], board[current_index]
    
    def isValidMove(self, board):
        # Encuentra el índice actual de la rana en el tablero
        current_index = board.index(self.index)

        # Calcula el nuevo índice restando 1
        new_index = current_index + 1

        # Si el índice es válido, entonces es un movimiento válido
        return new_index < len(board) and board[new_index] == '_'
