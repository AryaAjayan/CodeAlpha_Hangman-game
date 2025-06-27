import random
import tkinter as tk
from tkinter import messagebox

# List of possible words to guess
word_list = ['python', 'hangman', 'challenge', 'programming', 'interface', 'function', 'variable', 'exception']

# Function to choose a random word from the list
def choose_word():
    return random.choice(word_list)

# Function to display the current state of the guessed word
def display_word(word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])


class HangmanGUI:
    def __init__(self, master):
        self.master = master
        master.title("Hangman Game")
        master.geometry("600x400")  # Set a more appropriate window size
        master.configure(bg="#f0f0f0")  # Light background

        self.word_to_guess = choose_word()
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.max_incorrect = 6
        self.game_over = False # Added a flag to prevent further guesses after game ends


        # UI elements
        self.word_label = tk.Label(master, text="", font=("Courier", 24), bg="#f0f0f0")
        self.word_label.pack(pady=20)

        self.guessed_letters_label = tk.Label(master, text="Guessed letters: ", font=("Arial", 12), bg="#f0f0f0")
        self.guessed_letters_label.pack()

        self.guess_entry = tk.Entry(master, width=5, font=("Arial", 14))
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind("<Return>", self.guess_letter)  # Bind Enter key

        self.guess_button = tk.Button(master, text="Guess", command=self.guess_letter, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.guess_button.pack()

        self.tries_label = tk.Label(master, text=f"Tries left: {self.max_incorrect}", font=("Arial", 12), bg="#f0f0f0")
        self.tries_label.pack(pady=10)

        self.message_label = tk.Label(master, text="", font=("Arial", 12), bg="#f0f0f0", fg="red") # Use fg for text color
        self.message_label.pack()

        # Start a new game button
        self.new_game_button = tk.Button(master, text="New Game", command=self.start_new_game, font=("Arial", 12), bg="#2196F3", fg="white")
        self.new_game_button.pack(pady=10)
        
        self.update_display()


    def guess_letter(self, event=None): # Added event=None to handle key binding
        if self.game_over:
            return # Do nothing if game is over
        
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)  # Clear the input field

        if not guess.isalpha() or len(guess) != 1:
            self.message_label.config(text="Please enter a single alphabetic character.")
            return

        if guess in self.guessed_letters:
            self.message_label.config(text="You've already guessed that letter.")
            return

        self.guessed_letters.add(guess)

        if guess in self.word_to_guess:
            self.message_label.config(text=f"Good job! '{guess}' is in the word.")
        else:
            self.incorrect_guesses += 1
            self.message_label.config(text=f"Wrong guess! You have {self.max_incorrect - self.incorrect_guesses} tries left.")

        self.update_display()
        self.check_game_over()

    def update_display(self):
        self.word_label.config(text=display_word(self.word_to_guess, self.guessed_letters))
        self.guessed_letters_label.config(text=f"Guessed letters: {', '.join(sorted(self.guessed_letters))}")
        self.tries_label.config(text=f"Tries left: {self.max_incorrect - self.incorrect_guesses}")


    def check_game_over(self):
        if all(letter in self.guessed_letters for letter in self.word_to_guess):
            self.message_label.config(text=f"Congratulations! You've guessed the word: {self.word_to_guess}", fg="green")  # Green for winning message
            self.game_over = True
            self.disable_input()
        elif self.incorrect_guesses >= self.max_incorrect:
            self.message_label.config(text=f"You've run out of guesses! The word was: {self.word_to_guess}")
            self.game_over = True
            self.disable_input()

    def start_new_game(self):
        self.word_to_guess = choose_word()
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.game_over = False
        self.message_label.config(text="") #clear the message label
        self.tries_label.config(text=f"Tries left: {self.max_incorrect}") #reset tries
        self.enable_input() #enable input again
        self.update_display()

    def disable_input(self):
        self.guess_entry.config(state="disabled")
        self.guess_button.config(state="disabled")

    def enable_input(self):
        self.guess_entry.config(state="normal")
        self.guess_button.config(state="normal")


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    gui = HangmanGUI(root)
    root.mainloop()