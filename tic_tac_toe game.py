from __future__ import annotations

import tkinter as tk
from typing import List

from tic_tac_toe import Game, winner, is_draw


class TicTacToeUI(tk.Tk):
    """Tkinter-based frontend for the `Game` class defined in `tic_tac_toe.py`."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.resizable(False, False)
        self.configure(padx=10, pady=10)

        self.game = Game()
        self.status_var = tk.StringVar(value="Player X's turn")
        self.buttons: List[List[tk.Button]] = []

        board_frame = tk.Frame(self)
        board_frame.grid(row=0, column=0, columnspan=3)

        for row in range(3):
            button_row: List[tk.Button] = []
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text=" ",
                    width=3,
                    height=1,
                    font=("Helvetica", 32),
                    command=lambda r=row, c=col: self.on_cell_pressed(r, c),
                )
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                button_row.append(button)
            self.buttons.append(button_row)

        status_label = tk.Label(self, textvariable=self.status_var, font=("Helvetica", 14))
        status_label.grid(row=1, column=0, columnspan=3, pady=(10, 0))

        reset_button = tk.Button(self, text="Reset", command=self.reset_board, font=("Helvetica", 12))
        reset_button.grid(row=2, column=0, columnspan=3, pady=(10, 0))

        self.update_board_ui()

    def on_cell_pressed(self, row: int, col: int) -> None:
        """Handle a user's click on a given cell."""
        if winner(self.game.board) or is_draw(self.game.board):
            return
        if not self.game.play_turn(row, col):
            return

        self.update_board_ui()

        victor = winner(self.game.board)
        if victor:
            self.status_var.set(f"Player {victor} wins! Press Reset to play again.")
            return

        if is_draw(self.game.board):
            self.status_var.set("It's a draw! Press Reset to play again.")
            return

        self.game.next_player()
        self.status_var.set(f"Player {self.game.current_player}'s turn")

    def update_board_ui(self) -> None:
        """Sync button labels with the board state."""
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=self.game.board[row][col])

    def reset_board(self) -> None:
        self.game.reset()
        self.update_board_ui()
        self.status_var.set("Player X's turn")


def main() -> None:
    app = TicTacToeUI()
    app.mainloop()


if __name__ == "__main__":
    main()


