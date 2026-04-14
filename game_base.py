from abc import abstractmethod
import sys
import random
from typing import Union
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QSizePolicy,
    QApplication,
    QHBoxLayout,
)
from PyQt6.QtGui import QFont, QResizeEvent, QShowEvent
from PyQt6.QtCore import Qt

from enum import Enum
from grid2d import Grid2D

Debug = False


class Move(Enum):
    Empty = 0
    X = 1
    O = 2


class Result(Enum):
    Unknown = -1
    Draw = 0
    X_Win = 1
    O_Win = 2


class TicTacToe_Base:
    def __init__(self):
        super().__init__()

        self.grid = Grid2D(3, 3, Move.Empty)

    def get_cell(self, row: int, col: int) -> Move:
        """
        Add helpers to get and set cell values in the tic tac toe grid.
        """
        return self.grid.get(col, row)

    def set_cell(self, row: int, col: int, value: Move):
        """
        Add helpers to get and set cell values in the tic tac toe grid.
        """
        self.grid.set(col, row, value)

    def replay_game(self):
        """
        Clear the game board.
        """
        self.grid.clear_all()

    @abstractmethod
    def get_next_move(self) -> Move:
        pass

    @abstractmethod
    def set_next_move(self, move: Move):
        pass

    @abstractmethod
    def update_next_move(self):
        pass

    @abstractmethod
    def get_move_string(self, move: Move) -> str:
        pass

    @abstractmethod
    def get_move_style(self, move: Move) -> str:
        pass

    @abstractmethod
    def who_won(self) -> Result:
        pass

    @abstractmethod
    def get_winner_string(self, result: Result) -> str:
        pass

    @abstractmethod
    def get_winner_style(self, result: Result) -> str:
        pass

    @abstractmethod
    def record_winner(self, result: Result):
        pass

    @abstractmethod
    def get_stats(self) -> dict[Result, int]:
        pass

    @abstractmethod
    def clear_stats(self):
        pass


class TicTacToe_Window(QMainWindow):
    def __init__(self, game: TicTacToe_Base):
        super().__init__()
        self.game = game

        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(100, 100, 350, 650)
        self.setMinimumSize(300, 600)

        self.initUi()

        self.reset_game()
        self.clear_stats()

    def initUi(self):
        # Create main layout
        self.main_layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.main_layout.setSpacing(10)

        # Create header label
        self.header_label = QLabel("Tic Tac Toe")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.header_label.setFixedHeight(50)
        self.header_label.setStyleSheet("color : darkcyan; font-size: 20px; font-weight: bold;")
        self.main_layout.addWidget(self.header_label)

        self.turn_label = QLabel()
        self.turn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turn_label.setStyleSheet("border: 2px solid black; background: white; color: black; font-size: 16px;")
        self.main_layout.addWidget(self.turn_label)

        # Create a 9 grid layout for tic tac toe that stretches properly using layouts
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_widget.setLayout(self.grid_layout)

        # Allow the grid widget to expand only vertically
        self.grid_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.main_layout.addWidget(self.grid_widget)

        # Create a 3x3 grid of buttons
        self.buttons = []
        for i in range(3):
            self.buttons.append([])
            for j in range(3):
                button = QPushButton()
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                button.setFont(QFont("Times", 14))
                button.value = (i, j)
                button.clicked.connect(self.button_clicked)
                self.grid_layout.addWidget(button, i, j)
                self.buttons[i].append(button)

        # Create result label
        self.result_label = QLabel()
        self.result_label.setFont(QFont("Times", 14))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("border: 2px solid black; background: white; color: black;")
        self.result_label.setFixedHeight(50)
        self.main_layout.addWidget(self.result_label)

        # Create push button to replay the game
        self.game_replay_button = QPushButton("Play Again")
        self.game_replay_button.clicked.connect(self.reset_game)
        self.game_replay_button.setFixedHeight(50)
        self.game_replay_button.setContentsMargins(40, 0, 40, 0)
        self.game_replay_button.setStyleSheet("color : red; font-size: 14px;")
        self.main_layout.addWidget(self.game_replay_button)

        # Create stats label
        self.stats_label = QLabel()
        self.stats_label.setFont(QFont("Times", 14))
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setStyleSheet("border: 2px solid black; background: white; color: black;")
        self.stats_label.setFixedHeight(50)
        self.main_layout.addWidget(self.stats_label)

        # Create a push button to clear stats
        self.clear_stats_button = QPushButton("Clear Stats")
        self.clear_stats_button.clicked.connect(self.clear_stats)
        self.clear_stats_button.setFixedHeight(50)
        self.clear_stats_button.setContentsMargins(40, 0, 40, 0)
        self.clear_stats_button.setStyleSheet("color : red; font-size: 14px;")
        self.main_layout.addWidget(self.clear_stats_button)

        # Create a push button to clear stats
        exit_button_layout = QHBoxLayout()
        exit_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        exit_button.setFixedHeight(50)
        exit_button.setStyleSheet("color : blue; font-size: 16px;")
        exit_button_layout.addWidget(exit_button)
        self.main_layout.addLayout(exit_button_layout)

        # Set initial state
        self.reset_game()

    def reset_game(self):
        self.result_label.setText(self.get_winner_string(Result.Unknown))
        self.result_label.setStyleSheet(self.get_winner_style(Result.Unknown))

        move_string = self.get_move_string(Move.Empty)
        move_style = self.get_move_style(Move.Empty)

        # Enable the push buttons
        for row in self.buttons:
            for button in row:
                button.setEnabled(True)
                button.setText(move_string)
                button.setStyleSheet(move_style)

        self.replay_game()
        self.set_next_move(self.get_random_move())
        self.turn_label.setText(self.get_next_move_string())

    def button_clicked(self):
        button = self.sender()
        i, j = button.value

        if Debug:
            print(f"Button clicked at {i}, {j} - value: {self.get_cell(i, j)}")

        if self.get_cell(i, j) != Move.Empty:
            if Debug:
                print("Cell is already occupied")
            return

        next_move = self.get_next_move()
        button.setText(self.get_move_string(next_move))
        button.setStyleSheet(self.get_move_style(next_move))
        button.setEnabled(False)

        self.set_cell(i, j, next_move)
        winner = self.who_won()

        if winner != Result.Unknown:
            self.record_winner(winner)
            self.result_label.setText(self.get_winner_string(winner))
            self.result_label.setStyleSheet(self.get_winner_style(winner))
            self.stats_label.setText(self.get_stats_string())
            self.stats_label.setStyleSheet(self.get_stats_style())
            for row in self.buttons:
                for button in row:
                    button.setEnabled(False)
            return

        self.update_next_move()
        self.turn_label.setText(self.get_next_move_string())

    def clear_stats(self):
        self.clear_game_stats()
        self.stats_label.setText(self.get_stats_string())
        self.stats_label.setStyleSheet(self.get_stats_style())

    def resizeEvent(self, event: QResizeEvent):
        """Ensure buttons remain square on resize."""
        super().resizeEvent(event)
        self.update_button_sizes()

    def showEvent(self, event: QShowEvent):
        """Ensure buttons are sized correctly when the window first appears."""
        super().showEvent(event)
        self.update_button_sizes()

    def update_button_sizes(self):
        """Ensure buttons remain square while properly accounting for row spacing."""
        grid_width = self.grid_widget.geometry().width()
        grid_height = self.grid_widget.geometry().height()

        if grid_width == 0 or grid_height == 0:
            return  # Avoid setting 0-size buttons

        # Define spacing between cells
        spacing = max(grid_height // 15, 10)  # Ensure spacing scales, min 10px
        self.grid_layout.setVerticalSpacing(spacing)
        self.grid_layout.setHorizontalSpacing(spacing)

        # Adjust button size to account for spacing (subtract total spacing)
        adjusted_width = grid_width - (2 * spacing)
        adjusted_height = grid_height - (2 * spacing)
        size = min(adjusted_width, adjusted_height) // 3  # Divide by 3 for square buttons

        # Apply size to buttons
        for row in self.buttons:
            for button in row:
                button.setFixedSize(size, size)

    def get_random_move(self):
        return Move.X if random.randint(0, 1) == 0 else Move.O

    def get_stats_string(self) -> str:
        ret = self.game.get_stats()

        if ret == None:
            return "(not implemented)"
        elif all(r in ret for r in [Result.X_Win, Result.O_Win, Result.Draw]):
            return f"X: {ret[Result.X_Win]}, O: {ret[Result.O_Win]}, Draw: {ret[Result.Draw]}"
        else:
            return "(stats invalid)"

    def get_stats_style(self) -> str:
        ret = self.game.get_stats()

        if ret == None or not all(r in ret for r in [Result.X_Win, Result.O_Win, Result.Draw]):
            r = None
        else:

            if ret[Result.X_Win] > ret[Result.O_Win]:
                r = Result.X_Win
            elif ret[Result.O_Win] > ret[Result.X_Win]:
                r = Result.O_Win
            else:
                r = Result.Draw

        return self.get_winner_style(r)

    def get_next_move_string(self) -> str:
        return f"Next Turn: {self.get_move_string(self.get_next_move())}"

    def get_move_string(self, move: Move) -> str:
        ret = self.game.get_move_string(move)
        return "?" if ret is None else ret

    def get_move_style(self, move: Move) -> str:
        ret = self.game.get_move_style(move)
        return "border: 2px solid black; background: white; color: black;" if ret is None else ret

    def get_winner_string(self, result: Result) -> str:
        ret = self.game.get_winner_string(result)
        return "(not implemented)" if ret is None else ret

    def get_winner_style(self, result: Result) -> str:
        ret = self.game.get_winner_style(result)
        return "border: 2px solid black; background: white; color: black;" if ret is None else ret

    def record_winner(self, result: Result):
        self.game.record_winner(result)

    def get_stats(self) -> dict[Result, int]:
        return self.game.get_stats()

    def clear_game_stats(self):
        self.game.clear_stats()

    def who_won(self) -> Result:
        ret = self.game.who_won()
        return Result.Unknown if ret not in Result else ret

    def get_next_move(self):
        ret = self.game.get_next_move()
        return Move.Empty if ret not in Move else ret

    def set_next_move(self, move: Move):
        self.game.set_next_move(move)

    def update_next_move(self):
        self.game.update_next_move()

    def set_cell(self, row: int, col: int, value: Move):
        self.game.set_cell(row, col, value)

    def get_cell(self, row: int, col: int) -> Move:
        return self.game.get_cell(row, col)

    def replay_game(self):
        self.game.replay_game()


def main():
    app = QApplication(sys.argv)
    window = TicTacToe_Window(TicTacToe_Base())
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    Debug = True

    main()
