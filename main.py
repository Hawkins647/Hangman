"""Hangman tkinter game - written by Hawkins647"""

import tkinter as tk
import random
import time
import threading


class Hangman:
    """This class requires a root window to be passed, and contains a hangman game."""

    def __init__(self, root):
        self.root = root
        self.root.title("Hangman")
        self.root.geometry("300x300")
        self.root.resizable(0, 0)

        self.title_frame = tk.Frame(root)
        self.title_frame.pack(pady=10)
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()
        self.hidden_frame = tk.Frame(root)
        self.hidden_frame.pack()

        tk.Label(self.title_frame, text="Hangman", font=("Rubrik", 20)).pack()

        self.let_var = tk.StringVar()
        self.let_var.trace('w', self.validate)

        self.letter_entry = tk.Entry(self.main_frame, textvariable=self.let_var, width=4, justify=tk.CENTER)
        self.letter_entry.grid(row=3, column=0, pady=10)

        self.chosen_word = self.get_random_word(self)

        self.check_button = tk.Button(self.main_frame, text="Confirm", width=15, command=self.check_let)
        self.check_button.grid(row=4, column=0, padx=5, pady=5)

        self.num_guesses = 10

        self.num_guesses_label = tk.Label(self.main_frame, text="Number of Guesses Left: " + str(self.num_guesses))
        self.num_guesses_label.grid(row=6, column=0)

        self.hidden_let_dict = {}

        for i in range(len(self.chosen_word)):
            self.hidden_let_label = tk.Label(self.hidden_frame, text="_", font=("Rubrik", 20))
            self.hidden_let_label.grid(row=5, column=i, padx=10, pady=10)
            self.hidden_let_dict[i] = self.hidden_let_label

    def thread_restart(self):
        """Use the threading module to thread the restart function, which allows for
        a time delay between resets."""
        thread = threading.Thread(target=self.restart)
        thread.start()

    def check_let(self):
        """Check if the entered letter is in the word or not, and take the appropriate action."""
        if self.letter_entry.get().upper() in self.chosen_word.upper():
            for i in range(len(self.chosen_word)):
                if self.chosen_word[i] == self.letter_entry.get().lower():
                    self.hidden_let_dict[i].config(text=self.chosen_word[i])

        else:
            self.num_guesses -= 1
            self.num_guesses_label.config(text="Number of Guesses Left: " + str(self.num_guesses))

        self.check_for_loss()
        self.check_for_win()

    def validate(self, *args):
        """Validate the entry box to see if it is longer than 1 character, or not an alpha character;
        if it is either, reset the entry to contain 1 character (or no character if invalid)."""
        if len(self.let_var.get()) > 1:
            self.let_var.set(self.let_var.get()[:1])
        if not self.let_var.get().isalpha():
            self.let_var.set("")

    @staticmethod
    def get_random_word(self):
        """Return a random word from the list"""
        word_list = ["tree", "wood", "lemon", "orange", "apple", "plant", "power",
                     "flower", "leaf", "game", "fight", "python", "coding"]
        word_choice = random.choice(word_list)
        return word_choice

    def restart(self):
        """Restart the game through destroying and creating the frames and widgets."""
        time.sleep(2)
        self.main_frame.destroy()
        self.hidden_frame.destroy()

        self.main_frame = tk.Frame(root)
        self.main_frame.pack()
        self.hidden_frame = tk.Frame(root)
        self.hidden_frame.pack()

        self.let_var = tk.StringVar()
        self.let_var.trace('w', self.validate)

        self.letter_entry = tk.Entry(self.main_frame, textvariable=self.let_var, width=4, justify=tk.CENTER)
        self.letter_entry.grid(row=3, column=0)

        self.chosen_word = self.get_random_word(self)

        self.check_button = tk.Button(self.main_frame, text="Confirm", width=15, command=self.check_let)
        self.check_button.grid(row=4, column=0, padx=5, pady=5)

        self.num_guesses = 10

        self.num_guesses_label = tk.Label(self.main_frame, text="Number of Guesses Left: " + str(self.num_guesses))
        self.num_guesses_label.grid(row=6, column=0)

        self.hidden_let_dict = {}

        for i in range(len(self.chosen_word)):
            self.hidden_let_label = tk.Label(self.hidden_frame, text="_", font=("Rubrik", 20))
            self.hidden_let_label.grid(row=5, column=i, padx=10, pady=10)
            self.hidden_let_dict[i] = self.hidden_let_label

    def check_for_loss(self):
        """Check for a loss through the num_guesses variable, and display a lose message if it is equal to zero.
        If the user has lost, the game is reset."""
        if self.num_guesses == 0:
            self.num_guesses_label.config(text="You lost! Try again!")
            self.check_button.config(state=tk.DISABLED)
            self.thread_restart()

    def check_for_win(self):
        """Check for a win through appending all the letters typed to a string, and
        comparing that to the chosen_word variable. If the user has won, display a win message
        then reset."""
        win_str = ""
        for i in range(len(self.hidden_let_dict)):
            win_str += self.hidden_let_dict[i]["text"]

        if win_str == self.chosen_word:
            self.num_guesses_label.config(text="You won! Great Job!")
            self.check_button.config(state=tk.DISABLED)
            self.thread_restart()


if __name__ == "__main__":
    root = tk.Tk()
    Hangman(root)
    root.mainloop()
