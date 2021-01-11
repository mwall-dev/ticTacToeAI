import numpy as np
import sys


class Board:

    def __init__(self, shape):
        self.board_shape = shape

        res = []
        for i in range(shape):
            res.append(np.arange(shape*i, shape*(i+1)))

        self.board = np.array(res)
        self.board += 1



    def print_board(self):
        
        for index, row in enumerate(self.board):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
            print("     |     |")
            print("  " + str(row[0]) + "  |  " + str(row[1]) + "  |  " + str(row[2]) )
            print("     |     |")

            if index == row.shape:
                break

            print("----------------")


    def make_move(self, position, symbol):

        # Flatten board so we can just directly use position number.
        self.board = self.board.flatten()

        # Check that position is empty so we can actually place something 
        if self.board[position - 1] == position:
            self.board[position - 1] = symbol
            self.board = self.board.reshape(self.board_shape, self.board_shape) 
            return 0
            
        else:
            self.board = self.board.reshape(self.board_shape, self.board_shape) 
            return 1         






    def check_for_win(self, symbol):

        # Check each row for a win
        for row in self.board:
           if np.all(row == symbol): 
               print("here")
               
               return True


        # Check each col for a win (just transpose matrix and do exact same code)
        for row in self.board.T:
            if np.all(row == symbol): return True


        # Check diagonals
        diag1 = np.diagonal(self.board)
        diag2 = np.diagonal(np.fliplr(self.board))

        if np.all(diag1 == symbol): return True
        if np.all(diag2 == symbol): return True

        return False 



def play_game():

    BOARD_DIM = 3
    SYMBOLS = {-1 : 'X', 
                -2: 'O'}

    move_count = 0 # To tell when board is full and if draw.  

    print("Welcome to TicTacToe")
    mode_select = input("Select mode: (2player) or (computer)")


    if mode_select == "2player":

        print("Selected 2 player: Begin game")
        print("Player 1 is X's")
        print("Player 2 is O's")

        # TO DO: Maybe implement a dice roll here for who goes first since theres such a big advantage.

        playing_board = Board(BOARD_DIM)
        playing_board.print_board()
        current_player = 1 # We use -player number as symbol. 

        while True:
            
            # Input move
            player_move = input("Player " + str(current_player) + " select a number: ")
            
            # Try to make move and if invalid then try again
            if playing_board.make_move(int(player_move), -current_player):
                print("Invalid Move" + player_move)
                continue

            # Check for win
            if playing_board.check_for_win(-current_player):
                playing_board.print_board()
                print("Player" + str(current_player) + " wins!")
                sys.exit()

            playing_board.print_board()


            current_player = 2 if current_player == 1 else 1
            move_count += 1

            if move_count == (BOARD_DIM * BOARD_DIM):
                print("Draw!")
                sys.exit()

            
    
    else:
        print("Invalid mode: please try again")
        play_game()


def main():

    play_game()



if __name__ == "__main__":
    main()


