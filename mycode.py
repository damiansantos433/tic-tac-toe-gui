import sys
import random
from typing import Union
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QGraphicsColorizeEffect, QApplication
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from game_base import TicTacToe_Base, TicTacToe_Window, Move, Result


class TicTacToe(TicTacToe_Base):
    def __init__(self):
        super().__init__()
        # TODO: Add the class variables for wins, losses, draws, and next move
        # Replace pass with your code
        

        self.wins = 0
        self.losses = 0
        self.draws = 0

        self.next_move = Move.X

    def get_next_move(self) -> Move:
        # TODO: Fill in get_next_move method body
        # Replace pass with your code
        return self.next_move

    def set_next_move(self, move: Move):
        # TODO: Fill in set_next_move method body
        # Replace pass with your code
        self.next_move = move

    def update_next_move(self):
        # TODO: Fill in update_next_move method body
        # Replace pass with your code
        if self.next_move == Move.X:
            self.next_move = Move.O
        else:
            self.next_move = Move.X

    def get_move_string(self, move: Move) -> str:
        # TODO: Fill in get_move_string method body
        # Replace pass with your code
        if move == Move.X:
            return "X"
        if move == Move.O:
            return "O"
        return ""

    def get_move_style(self, move: Move) -> str:
        # TODO: Fill in get_move_style method body
        # Replace pass with your code
        if move == Move.X:
            return "border: 1px solid black; background: lightgreen; color: black;"
        if move == Move.O:
            return "border: 1px solid black; background: blue; color: white;"
        return "border: 1px solid black; background: white; color: black;"

    def who_won(self) -> Result:
        # TODO: Fill in who_won method body
        # Replace pass with your code
    

        #Check for winner - return if there is a winner
        winner = self.determine_winning_cells(0,0,1,1,2,2)   
        if (winner != Result.Unknown):
            return winner
        
        winner = self.determine_winning_cells(2,0,1,1,0,2)   
        if (winner != Result.Unknown):
            return winner
        
        for row in range(3):
            winner = self.determine_winning_cells(row,0,row,1,row,2) 
            if (winner != Result.Unknown):
                return winner
            
        for col in range(3):
            winner = self.determine_winning_cells(0, col, 1, col, 2, col) 
            if (winner != Result.Unknown):
                return winner
        #Check if there are any empty cells - if so, return unknown
        for row in range(3):
            for col in range(3):
                if self.get_cell(row,col) == Move.Empty:
                    return Result.Unknown
        #return draw
        return Result.Draw
    
    def determine_winning_cells(self, r1, c1, r2, c2, r3, c3):
        if self.get_cell(r1, c1) == self.get_cell(r2, c2) == self.get_cell(r3, c3):
            if self.get_cell(r1,c1) == Move.X:
                return Result.X_Win
            elif self.get_cell(r1,c1) == Move.O:
                return Result.O_Win    
        return Result.Unknown     

      
    def get_winner_string(self, result: Result) -> str:
        # TODO: Fill in get_winner_string method body
        # Replace pass with your code
        if result == Result.X_Win:
            return "X Wins"
        if result == Result.O_Win:
            return "O Wins"
        if result == Result.Draw:
            return "Draw"
        return ""

    def get_winner_style(self, result: Result) -> str:
        # TODO: Fill in get_winner_style method body
        # Replace pass with your code
        if result == Result.X_Win:
            return "border: 1px solid black; background: lightgreen; color: black;"
        if result == Result.O_Win:
            return "border: 1px solid black; background: blue; color: white;"
        if result == Result.Draw:
            return "border: 1px solid black; background: yellow; color: black;"
        return "border: 1px solid black; background: white; color: black;"

    def record_winner(self, result: Result):
        # TODO: Fill in record_winner method body
        # Replace pass with your code
        
        
        if result == Result.X_Win:
            self.wins = self.wins + 1

        if result == Result.O_Win:
            self.losses = self.losses + 1

        if result == Result.Draw:
            self.draws = self.draws + 1

    def get_stats(self) -> dict[Result, int]:
        # TODO: Fill in get_stats method body
        # Replace pass with your code
        return {Result.X_Win: self.wins, Result.O_Win: self.losses, Result.Draw: self.draws}

    def clear_stats(self):
        # TODO: Fill in clear_stats method body
        # Replace pass with your code
        
        self.wins, self.losses, self.draws = 0, 0, 0
        return 


#
# DO NOT MODIFY ANYTHING BELOW THIS LINE
# --------------------------------------
#


def main():
    app = QApplication(sys.argv)
    window = TicTacToe_Window(TicTacToe())
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
