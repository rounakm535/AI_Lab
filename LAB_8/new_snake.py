import tkinter as tk
from tkinter import ttk, messagebox
import random


class TwoPlayerSnakeLadder:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake & Ladder with AI Player")
        self.root.geometry("760x850")
        self.root.configure(bg='#2E2E2E')

        # Game configuration
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19,
                       64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84,
                        36: 44, 51: 67, 71: 91, 80: 100}

        # Game state
        self.player1_pos = 0
        self.player2_pos = 0
        self.game_active = True
        self.current_turn = 'player1'  # Player 1 starts

        # UI Setup
        self.CELL_SIZE = 70
        self.BOARD_OFFSET = 30
        self.COLORS = {'board_bg': '#F5F5DC', 'cell_bg': '#FFFFFF',
                       'snake': '#008000', 'ladder': '#964B00',
                       'player1': 'blue', 'player2': 'red'}

        self.setup_gui()
        self.draw_board()
        self.update_pieces()

    def setup_gui(self):
        self.canvas = tk.Canvas(self.root, width=700, height=700, bg=self.COLORS['board_bg'], highlightthickness=0)
        self.canvas.pack(pady=10)

        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=20, pady=5)

        self.dice_label = tk.Label(control_frame, text="🎲", font=("Arial", 40, "bold"), width=5)
        self.dice_label.pack(side=tk.LEFT, padx=10)

        self.dice_btn = ttk.Button(control_frame, text="Roll Dice", command=self.start_turn)
        self.dice_btn.pack(side=tk.LEFT, padx=5)

        self.status = ttk.Label(control_frame, text="Player 1's Turn | P1[0] P2[0]", font=('Helvetica', 14, 'bold'))
        self.status.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.reset_btn = ttk.Button(control_frame, text="New Game", command=self.reset_game)
        self.reset_btn.pack(side=tk.RIGHT, padx=5)

    def draw_board(self):
        for row in range(10):
            for col in range(10):
                x1 = self.BOARD_OFFSET + col * self.CELL_SIZE
                y1 = self.BOARD_OFFSET + (9 - row) * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.COLORS['cell_bg'], outline='#DDDDDD')

                if row % 2 == 0:
                    num = row * 10 + col + 1
                else:
                    num = (row + 1) * 10 - col

                self.canvas.create_text(x1 + self.CELL_SIZE / 2, y1 + self.CELL_SIZE / 2, text=str(num),
                                        font=('Arial', 10))

        self.draw_ladders()
        self.draw_snakes()

    def draw_ladders(self):
        for start, end in self.ladders.items():
            start_x, start_y = self.get_coords(start)
            end_x, end_y = self.get_coords(end)

            # Draw ladder lines with a more rustic look
            self.canvas.create_line(start_x, start_y, end_x, start_y, width=10, fill=self.COLORS['ladder'])
            self.canvas.create_line(end_x, start_y, end_x, end_y, width=10, fill=self.COLORS['ladder'])

            # Add rungs for a more detailed look
            num_rungs = 8
            for i in range(num_rungs):
                rung_x = start_x + (end_x - start_x) * i / (num_rungs - 1)
                self.canvas.create_line(rung_x - 8, start_y, rung_x + 8, start_y, width=6, fill='black')

    def draw_snakes(self):
        for start, end in self.snakes.items():
            start_x, start_y = self.get_coords(start)
            end_x, end_y = self.get_coords(end)

            # Draw snakes with a more organic look
            self.canvas.create_line(start_x, start_y, end_x, end_y, width=12, fill=self.COLORS['snake'], smooth=True)

            # Optional: Add snake body details
            num_coils = 4
            for i in range(num_coils):
                coil_x = start_x + (end_x - start_x) * i / (num_coils - 1)
                coil_y = start_y + (end_y - start_y) * i / (num_coils - 1)
                self.canvas.create_oval(coil_x - 5, coil_y - 5, coil_x + 5, coil_y + 5, fill='black')

    def get_coords(self, position):
        row = (position - 1) // 10
        col = (position - 1) % 10
        if row % 2 == 1:
            col = 9 - col

        x = self.BOARD_OFFSET + col * self.CELL_SIZE + self.CELL_SIZE // 2
        y = self.BOARD_OFFSET + (9 - row) * self.CELL_SIZE + self.CELL_SIZE // 2
        return x, y

    def update_pieces(self):
        self.canvas.delete('pieces')
        p1_x, p1_y = self.get_coords(self.player1_pos)
        p2_x, p2_y = self.get_coords(self.player2_pos)
        self.canvas.create_oval(p1_x - 16, p1_y - 16, p1_x + 16, p1_y + 16, fill=self.COLORS['player1'], tags='pieces')
        self.canvas.create_oval(p2_x - 16, p2_y - 16, p2_x + 16, p2_y + 16, fill=self.COLORS['player2'], tags='pieces')

    def start_turn(self):
        if not self.game_active:
            return
        dice = random.randint(1, 6)
        self.dice_label.config(text=f"🎲 {dice}")
        self.root.after(500, lambda: self.move_player(dice))

    def move_player(self, steps):
        if self.current_turn == 'player1':
            self.player1_pos += steps
            if self.player1_pos in self.snakes:
                print(
                    f"Player 1 landed on a snake! Moving from {self.player1_pos - steps} to {self.snakes[self.player1_pos]}.")
                self.player1_pos = self.snakes[self.player1_pos]
            elif self.player1_pos in self.ladders:
                print(
                    f"Player 1 landed on a ladder! Moving from {self.player1_pos - steps} to {self.ladders[self.player1_pos]}.")
                self.player1_pos = self.ladders[self.player1_pos]
        else:
            self.player2_pos += steps
            if self.player2_pos in self.snakes:
                print(
                    f"Player 2 landed on a snake! Moving from {self.player2_pos - steps} to {self.snakes[self.player2_pos]}.")
                self.player2_pos = self.snakes[self.player2_pos]
            elif self.player2_pos in self.ladders:
                print(
                    f"Player 2 landed on a ladder! Moving from {self.player2_pos - steps} to {self.ladders[self.player2_pos]}.")
                self.player2_pos = self.ladders[self.player2_pos]

        # Ensure the player doesn't exceed the board
        if self.player1_pos > 100:
            self.player1_pos -= steps
        if self.player2_pos > 100:
            self.player2_pos -= steps

        self.update_pieces()
        self.finalize_move()

    def finalize_move(self):
        if self.player1_pos >= 100 or self.player2_pos >= 100:
            winner = 'Player 1' if self.player1_pos >= 100 else 'AI Player 2'
            messagebox.showinfo("Game Over", f"{winner} Wins!")
            self.game_active = False
        else:
            self.current_turn = 'player2' if self.current_turn == 'player1' else 'player1'
            self.status.config(text=f"{self.current_turn}'s Turn ")
            if self.current_turn == 'player2':
                self.root.after(1000, self.start_turn)

    def reset_game(self):
        self.player1_pos = 0
        self.player2_pos = 0
        self.game_active = True
        self.current_turn = 'player1'
        self.update_pieces()
        self.status.config(text="Player 1's Turn ")


if __name__ == "__main__":
    root = tk.Tk()
    game = TwoPlayerSnakeLadder(root)
    root.mainloop()
