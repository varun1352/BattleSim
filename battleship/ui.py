# src/battleship/ui.py

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from battleship.main import run_simulation
from dotenv import load_dotenv
import os

class BattleshipUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Battleship Simulator")
        # Larger window size for bigger boards
        self.geometry("1200x800")
        self.configure(padx=10, pady=10)

        self.create_widgets()

    def create_widgets(self):
        """Set up the UI layout and widgets with larger fonts and bigger boards."""

        # Title Label (bigger font)
        title_label = ttk.Label(self, text="Battleship Simulator", font=("Helvetica", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Player 1 Labelframe
        self.player1_frame = ttk.Labelframe(self, text="Player 1", padding=10)
        self.player1_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Strategy Label (Player 1) - bigger wraplength if needed
        self.strategy1_label = ttk.Label(
            self.player1_frame,
            text="Strategy goes here (will be updated on start).",
            font=("Helvetica", 18),
            wraplength=500
        )
        self.strategy1_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

        # Player 1: Personal Board
        ttk.Label(self.player1_frame, text="Personal Board:", font=("Helvetica", 18, "bold")).grid(row=1, column=0, sticky="w")
        self.personal_board1_text = tk.Text(self.player1_frame, width=20, height=12, font=("Courier", 24))
        self.personal_board1_text.grid(row=2, column=0, sticky="w")

        # Player 1: Real Board
        ttk.Label(self.player1_frame, text="Real Board (Static):", font=("Helvetica", 18, "bold")).grid(row=1, column=1, sticky="w")
        self.real_board1_text = tk.Text(self.player1_frame, width=20, height=12, font=("Courier", 24))
        self.real_board1_text.grid(row=2, column=1, sticky="w")

        # Player 2 Labelframe
        self.player2_frame = ttk.Labelframe(self, text="Player 2", padding=10)
        self.player2_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Strategy Label (Player 2)
        self.strategy2_label = ttk.Label(
            self.player2_frame,
            text="Strategy goes here (will be updated on start).",
            font=("Helvetica", 18),
            wraplength=500
        )
        self.strategy2_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

        # Player 2: Personal Board
        ttk.Label(self.player2_frame, text="Personal Board:", font=("Helvetica", 18, "bold")).grid(row=1, column=0, sticky="w")
        self.personal_board2_text = tk.Text(self.player2_frame, width=20, height=12, font=("Courier", 24))
        self.personal_board2_text.grid(row=2, column=0, sticky="w")

        # Player 2: Real Board
        ttk.Label(self.player2_frame, text="Real Board (Static):", font=("Helvetica", 18, "bold")).grid(row=1, column=1, sticky="w")
        self.real_board2_text = tk.Text(self.player2_frame, width=20, height=12, font=("Courier", 24))
        self.real_board2_text.grid(row=2, column=1, sticky="w")

        # Buttons Frame (Start/Quit)
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.start_button = ttk.Button(self.buttons_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=0, column=0, padx=5)

        self.quit_button = ttk.Button(self.buttons_frame, text="Quit", command=self.destroy)
        self.quit_button.grid(row=0, column=1, padx=5)

    def update_boards(self, player1=None, player2=None, game_over=False, winner=None):
        """
        Callback used by run_simulation() each turn.
        Updates both personal boards and real boards for each player.
        """
        if game_over:
            messagebox.showinfo("Game Over", f"Winner: {winner}")
            return

        if player1 and player2:
            # Player1 Personal
            self.personal_board1_text.config(state="normal")
            self.personal_board1_text.delete("1.0", tk.END)
            self.personal_board1_text.insert(tk.END, player1.personal_board.to_string())
            self.personal_board1_text.config(state="disabled")

            # Player2 Personal
            self.personal_board2_text.config(state="normal")
            self.personal_board2_text.delete("1.0", tk.END)
            self.personal_board2_text.insert(tk.END, player2.personal_board.to_string())
            self.personal_board2_text.config(state="disabled")

            # Player1 Real
            self.real_board1_text.config(state="normal")
            self.real_board1_text.delete("1.0", tk.END)
            self.real_board1_text.insert(tk.END, player1.real_board.to_string())
            self.real_board1_text.config(state="disabled")

            # Player2 Real
            self.real_board2_text.config(state="normal")
            self.real_board2_text.delete("1.0", tk.END)
            self.real_board2_text.insert(tk.END, player2.real_board.to_string())
            self.real_board2_text.config(state="disabled")

    def start_simulation(self):
        """
        Start the simulation in a background thread.
        Also update the strategy labels to match what's in agents.yaml, if desired.
        """
        self.strategy1_label.config(text="Aggressive Hunter\nFocus on systematic search and rapid targeting.")
        self.strategy2_label.config(text="Defensive Counter\nBalance exploration with careful targeting.")

        # Start the simulation in a separate thread
        sim_thread = threading.Thread(target=self.run_sim)
        sim_thread.daemon = True
        sim_thread.start()

    def run_sim(self):
        """
        Calls the run_simulation function from main.py, passing this UI's update_boards callback.
        """
        run_simulation(ui_update_callback=self.update_boards)

def main():
    # If you need environment variables
    load_dotenv()
    print("Cerebras API Key:", os.getenv("CEREBRAS_API_KEY"))

    app = BattleshipUI()
    app.mainloop()

if __name__ == "__main__":
    main()
