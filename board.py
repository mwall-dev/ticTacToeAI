import numpy as np


class Board:

    P1 = -1
    P2 = -2
    DRAW = -3
    NO_WIN = 0

    MOVE_SUCCESS = 0
    MOVE_INVALID = 1
    
    def __init__(self, shape):

        self.board_shape = shape # Easier to store instead of calling self.board.shape[0]

        res = []
        for i in range(shape):
            res.append(np.arange(shape*i, shape*(i+1)))

        self.board = np.array(res)
        self.board += 1

        self.num_moves = 0
        
        
    def make_copy(self):
        """ Return a copy of a board instance. Used for minimax."""

        new_board = Board(self.board_shape)
        new_board.board = np.copy(self.board)
        new_board.num_moves = self.num_moves
        return new_board


    def print_board(self):
        """ Pretty printing for the board object instance. """

        def to_symbol(symbol):
            if symbol == Board.P1: return 'X'
            elif symbol == Board.P2: return 'O'
            else: return symbol

        for index, row in enumerate(self.board):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
            print("     |     |")
            print("  " + str(to_symbol(row[0])) + "  |  " + str(to_symbol(row[1])) + "  |  " 
            + str(to_symbol(row[2])) )
            print("     |     |")

            if index == self.board_shape - 1:
                break

            print("----------------")

    def get_empty_squares(self):
        """ Return a list of the empty squares on this board."""
        empty_squares = []
        for position in self.board.flat:
            if position != Board.P1 and position != Board.P2:
                empty_squares.append(position)

        return empty_squares




    def make_move(self, position, symbol):
        """ 
        Attempt to make move on board object given a position number and a symbol to go there.
        :param int position: numbers 1 to 9
            Returns:
                MOVE_SUCCESS if valid move.
                MOVE_INVALID if invalid move.
        """
        # Flatten board so we can just directly use position number.
        self.board = self.board.flatten()

        # Check that position is empty so we can actually place something 
        if self.board[position - 1] == position:
            self.board[position - 1] = symbol
            self.board = self.board.reshape(self.board_shape, self.board_shape)
            self.num_moves += 1 
            return Board.MOVE_SUCCESS
            
        else:
            # Invalid move: position not free.
            self.board = self.board.reshape(self.board_shape, self.board_shape) 
            return Board.MOVE_INVALID    




    
    def check_for_win(self):
        """
        Check board for winning position.
        
            Returns:
                Board.P1 if player 1 (X) has won
                Board.P2 if player 2 (O) has won 
                Board.DRAW if draw
                Board.NO_WIN if inconclusive

        """

        # Check each row for a win
        for row in self.board:
            if np.all(row == Board.P1): return Board.P1
            if np.all(row == Board.P2): return Board.P2 

        # Check columns
        for row in self.board.T:
            if np.all(row == Board.P1): return Board.P1
            if np.all(row == Board.P2): return Board.P2

        # Check diagonals
        diag1 = np.diagonal(self.board)
        diag2 = np.diagonal(np.fliplr(self.board))

        if np.all(diag1 == Board.P1): return Board.P1
        if np.all(diag1 == Board.P2): return Board.P2  
        if np.all(diag2 == Board.P1): return Board.P1
        if np.all(diag2 == Board.P2): return Board.P2     

        if self.num_moves == (self.board_shape * self.board_shape):
            return Board.DRAW

        return Board.NO_WIN 
