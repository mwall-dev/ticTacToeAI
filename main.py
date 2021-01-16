import numpy as np
import sys
import math 

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


    

def minimax(board, depth, maximizingPlayer):
    """ Recursive algorithm to determine the best possible next move to a fastest win.
        Implementation of the minimax algorithm. This algorithm has no idea of the games rules or 
        what constitues a good move. It simply goes off a point value system coded in.

        For TicTacToe, there are only 255168 possible games so the game tree is 
        small enough to search to the very bottom depth each move.

        Point values are as follows:
        +10 for comp win 
        -10 for human win 
        0 for draw

        The algoithm will create a tree of possible moves at each step. 
        It will recurse down each possible move and keep recursing through the next possible moves from there
        with each path finishing at a leaf node and returning a point value based on who won (or draw).
        (For games like chess, we can't calculate all possible moves and go right down to very end since the
        number of games is too massive. To apply this algorithm to chess, you would simply assign a point value to pieces
        and go down to a certain hardcoded depth.

        The algorithm switches between the maximizing and minimizing players. Basically we are looking at what happens 
        even if each side makes the very best move, and how we can still win if they do so from here. 


        Note: computer is 'O' and is therefore player 2 meaning check_for_win() 
        will return Board.P2 for comp win.


        --- TO DO ---
        Implement alpha-beta pruning.
        Since we will get many leaf nodes with the same win value, 
        we will subtract the depth from them
        so we are taking the FASTEST path to win.

        """

    win_check = board.check_for_win()

    # If someone has won, reached bottom of this 'tree path'. Will recurse this value back to top.
    if win_check:
        if win_check == Board.P1: return -10 # human wins
        elif win_check == Board.P2: return 10 # comp wins
        else: return 0 # Draw weighted in no ones favor.

    if maximizingPlayer:
        max_eval = -math.inf
        possible_next_moves = board.get_empty_squares()
        for move in possible_next_moves:
            board_copy = board.make_copy()
            board_copy.make_move(move, Board.P2)
            move_eval = minimax(board_copy, depth + 1, False) 
            if move_eval > max_eval:
                max_eval = move_eval
                best_move = move
        if depth == 0:
            return best_move

        return max_eval

    else:
        min_eval = math.inf
        possible_next_moves = board.get_empty_squares()

        for move in possible_next_moves:
            board_copy = board.make_copy()
            board_copy.make_move(move, Board.P1)
            move_eval = minimax(board_copy, depth + 1, True)
            min_eval = min(move_eval, min_eval)
        return min_eval


def human_turn(board, player):

    player_print = -player # For printing

    # Input move
    player_move = input("Player " + str(player_print) + " select a number: ")
    print('\n')
    # Check that input is valid
    try:
        player_move = int(player_move)

    except ValueError:
        print("Not an int ")
        human_turn(board, player)
        
    # Check move is in range of spaces
    if player_move < 1 or player_move > 9:
        print("Invalid Move: Must be integer in range [1,9].")
        human_turn(board, player)


    # Attempt to make move on board. Fail if spot is taken
    elif board.make_move(player_move, player):
        print("Invalid Move: " + str(player_move) )
        human_turn(board, player)
    
    # Valid move, make it.
    else:
        board.make_move(player_move, player)



def play_comp(board):
    """ 
    Human player vs computer.
    Human will always go first (give them the advantage).
    Human is therefore Player 1 and is X.
    
    """
    print("Selected vs Computer mode: Begin game")
    print("Player is X's")
    print("Computer is O's")

    print("Player gets first move")

    board.print_board()

    current_player = Board.P1 # Player 1 is human, player 2 is computer. Human goes first

    while True:
        # Human turn 
        if current_player == Board.P1:
            human_turn(board, current_player)
            # Check for win
            win_check = board.check_for_win()

            validate_win(board, win_check)

            board.print_board()
            current_player = Board.P2

        # Computer turn 
        else:
            print("Computer thinking...\n")
            board.make_move(minimax(board, 0, True), current_player)

             # Check for win
            win_check = board.check_for_win()

            validate_win(board, win_check)

            board.print_board()
            current_player = Board.P1


def validate_win(board, win_check):
    """ 
    Validation and printing for win information. 
    Kept seperate from check_for_win() so simulated games aren't printed.
    
    """

    if win_check:
        board.print_board()

        if win_check == Board.DRAW:
            print("Draw!")
            sys.exit()
        else:
            print("Player" + str(-win_check) + " wins!") # Negative for printing
            sys.exit()


    

def play_2player(board):
    """ 2 player game for TicTacToe between 2 human players. """

    print("Selected 2 player: Begin game")
    print("Player 1 is X's")
    print("Player 2 is O's")
    board.print_board()

    current_player = Board.P1 

    # Game loop until win or draw.
    while True: 
        human_turn(board, current_player)

        # Check for win
        win_check = board.check_for_win()
        validate_win(board, win_check)
       
        board.print_board()
        current_player = Board.P2 if current_player == Board.P1 else Board.P1




def launch_game():

    BOARD_DIM = 3 # TO DO - potential to have NxN games of TicTacToe but implement later. Have kept open.
                  # Will need to edit print function but have mostly keep things open.

    print("Welcome to TicTacToe")
    mode_select = input("Select mode: (2player) or (computer)")


    if mode_select == "2player":
        play_2player(Board(BOARD_DIM))

    elif mode_select == "computer":
        play_comp(Board(BOARD_DIM))

    elif mode_select == "debug":
        playing_board = Board(BOARD_DIM)
        playing_board.make_move(2,Board.P1)
        print(playing_board.get_empty_squares())
    else:
        print("Invalid mode: please try again")
        launch_game()



def main():
    launch_game()


if __name__ == "__main__":
    main()


