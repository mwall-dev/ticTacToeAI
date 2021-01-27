import numpy as np
import sys
import math 

from board import Board



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
    

def minimax(board, depth, maximizingPlayer):

    """ 
        Recursive algorithm to determine the best possible next move to a fastest win.
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
    """ Human turn logic. Makes a single move on board. """

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


