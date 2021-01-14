import numpy as np
import sys
import math 

class Board:

    def __init__(self, shape):

        self.board_shape = shape # Easier to store instead of calling self.board.shape[0]

        res = []
        for i in range(shape):
            res.append(np.arange(shape*i, shape*(i+1)))

        self.board = np.array(res)
        self.board += 1

        self.num_moves = 0
        
        
   

    def print_board(self):
        """ Pretty printing for the board object instance. """

        def to_symbol(symbol):
            if symbol == -1: return 'X'
            elif symbol == -2: return 'O'
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
            if position != -1 or position != -2:
                empty_squares.append(position)

        return empty_squares




    def make_move(self, position, symbol):
        """ 
        Attempt to make move on board object given a position number and a symbol to go there.

            Returns:
                0 if valid move.
                1 if invalid move.
        """
        # Flatten board so we can just directly use position number.
        self.board = self.board.flatten()

        # Check that position is empty so we can actually place something 
        if self.board[position - 1] == position:
            self.board[position - 1] = symbol
            self.board = self.board.reshape(self.board_shape, self.board_shape)
            self.num_moves += 1 
            return 0
            
        else:
            # Invalid move: position not free.
            self.board = self.board.reshape(self.board_shape, self.board_shape) 
            return 1         




    
    def check_for_win(self):
        """
        Check board for winning position.
        
            Returns:
                -1 if player 1 (X) has won
                -2 if player 2 (O) has won 
                -3 if draw
                0 if inconclusive (no win yet)

        """
        # Check each row for a win
        for row in self.board:
           if np.all(row == -1): return -1
           if np.all(row == -2): return -2 


        # Check each col for a win (just transpose matrix and do exact same code)
        for row in self.board.T:
            if np.all(row == -1): return -1
            if np.all(row == -2): return -2 

        # Check diagonals
        diag1 = np.diagonal(self.board)
        diag2 = np.diagonal(np.fliplr(self.board))

        if np.all(diag1 == -1): return -1
        if np.all(diag1 == -2): return -2  
        if np.all(diag2 == -1): return -1
        if np.all(diag2 == -2): return -2     

        if self.num_moves == (self.board_shape * self.board_shape):
            return -3

        return 0 


    

def minimax(board, depth, maximizingPlayer):
    """ Recursive function to determine the best possible next move to a fastest win.
        Implementation of the minimax algorithm.
        For TicTacToe, there are only 255168 possible games so the game tree is small enough to search
        to the very bottom depth each move.

        Point values are as follows:
        +10 for comp win 
        -10 for human win 
        0 for draw

        Since we will get many leaf nodes with the same win value, we will subtract the depth from them
        so we are taking the FASTEST path to win.

        Note: computer is 'O' and is therefore player 2 meaning check_for_win() will return -2 for comp win.
        """
    win_check = board.check_for_win()

    # If someone has won, reached bottom of this 'tree path'. Will recurse this value back to top.
    if win_check:
        if win_check == -1: return -10 # human wins
        elif win_check == -2: return 10 # comp wins
        else: return 0 # draw

    empty_squares = (board.board_shape ** 2) - board.num_moves
    if maximizingPlayer:
        max_eval = -math.inf
        possible_next_moves = get_empty_squares(board)
        for move in possible_next_moves:
            board_copy = np.copy(board.board)
            board_copy.make_move(move, 'O')
            move_eval = minimax(board_copy, depth + 1, False) 
            if move_eval > max_eval:
                max_eval = move_eval
                best_move = move
        if depth == 0:
            return best_move
        return max_eval

    else:
        min_eval = math.inf
        possible_next_moves = get_empty_squares(board)

        for move in possible_next_moves:
            board_copy = np.copy(board.board)
            board_copy.make_move(move, 'X')
            move_eval = minimax(board_copy, depth + 1, True)
            min_eval = min(move_eval, min_eval)
        return max_eval


def human_turn(board, player_number):

     # Input move
        player_move = input("Player " + str(player_number) + " select a number: ")
        print('\n')
        # Check that input is valid
        try:
            player_move = int(player_move)

        except ValueError:
            print("Not an int ")
            continue
            
        # Check move is in range of spaces
        if player_move < 1 or player_move > 9:
            print("Invalid Move: Must be integer in range [1,9].")
            continue

        # Attempt to make move on board
        if board.make_move(player_move, -player_number):
            print("Invalid Move: " + str(player_move) )
            continue
        


def computer_turn(board, player_number):


def play_comp(board):
    """ 
    Human player vs computer.
    Human will always go first (give them the advantage).
    Human is therefore Player 1 and is X.
    
    """
    print("Selected vs cOmputer mode: Begin game")
    print("Player is X's")
    print("Computer is O's")

    print("Player gets first move")

    board.print_board()

    current_player = 1 # Player 1 is human, player 2 is computer.
    
    while True:

        # Input move
        player_move = input("Player " + str(current_player) + " select a number: ")
        print('\n')
        # Check that input is valid
        try:
            player_move = int(player_move)

        except ValueError:
            print("Not an int ")
            continue
        
         # Check move is in range of spaces
        if player_move < 1 or player_move > 9:
            print("Invalid Move: Must be integer in range [1,9].")
            continue

        # Attempt to make move on board
        if board.make_move(player_move, -current_player):
            print("Invalid Move: " + str(player_move) )
            continue
            

        # Check for win
        win_check = board.check_for_win()

        if win_check:
            board.print_board()

            if win_check == -3:
                print("Draw!")
                sys.exit()
            else:
                print("Player" + str(current_player) + " wins!")
                sys.exit()

        board.print_board()
        current_player = 2 if current_player == 1 else 1




def play_2player(board):
    """ 2 player game for TicTacToe between 2 human players. """

    print("Selected 2 player: Begin game")
    print("Player 1 is X's")
    print("Player 2 is O's")
    board.print_board()

    current_player = 1 # We use -player number as symbol. 

    # Game loop until win or draw.
    while True: 
        human_turn(board, current_player):

        # Check for win
        win_check = board.check_for_win()

        if win_check:
            board.print_board()

            if win_check == -3:
                print("Draw!")
                sys.exit()
            else:
                print("Player" + str(current_player) + " wins!")
                sys.exit()

        board.print_board()
        current_player = 2 if current_player == 1 else 1




def launch_game():

    BOARD_DIM = 3 # TO DO - potential to have NxN games of TicTacToe but implement later. Have kept open
                  # Will need to edit print function.

    print("Welcome to TicTacToe")
    mode_select = input("Select mode: (2player) or (computer)")


    if mode_select == "2player":
        play_2player(Board(BOARD_DIM))

    elif mode_select == "computer":
        play_comp(Board(BOARD_DIM))

    else:
        print("Invalid mode: please try again")
        launch_game()



def main():
    launch_game()


if __name__ == "__main__":
    main()


