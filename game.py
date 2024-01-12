import random
import pathlib
import config
from srtools import latin_to_cyrillic

from tkinter import *
from tkinter import messagebox

WORD = ''
LENGTH = 0
NUM_TRIES = 0
GUESSES_GRID = []
GUESSNUM = 0

ROOT = ''
WORD_INPUT = ''

WIN = False
SCORE = 0


def game_setup(length, num_tries):
    global WORD, LENGTH, NUM_TRIES, GUESSES_GRID, SCORE, GUESSNUM, ROOT, WORD_INPUT, WIN
    word_list = pathlib.Path(config.WORDLIST_PATH)
    words = [word.upper() for word in word_list.read_text(encoding="utf-8").strip().split("\n")]
    WORD = random.choice([word for word in words if len(word) == length])
    LENGTH = length
    NUM_TRIES = num_tries
    GUESSES_GRID = ['_'*LENGTH]*NUM_TRIES
    SCORE = 0
    GUESSNUM = 0
    WIN = False
    ROOT = ''
    WORD_INPUT = ''


def render_grid():
    global ROOT, WORD, GUESSES_GRID
    for i in range(len(GUESSES_GRID)):
        for j, letter in enumerate(GUESSES_GRID[i]):
            label = Label(ROOT, text=letter.upper(), font='arial 18', border='1px white', borderwidth=1, relief="solid", )
            label.grid(row=i, column=j, pady=(30,0))

            if letter == WORD[j]:  # if they get the letter right
                label.config(bg=config.GREEN, fg=config.BLACK)

            elif letter in WORD and not letter == WORD[j]  and not GUESSES_GRID[i].count(letter)>WORD.count(letter):  # if the letter is in the word, but not in the right spot
                label.config(bg=config.YELLOW, fg=config.BLACK)

            else:
                label.config(bg=config.BLACK, fg=config.WHITE)


def get_guess(e):
    global WORD, GUESSES_GRID, GUESSNUM, WORD_INPUT, SCORE, WIN
    guess = latin_to_cyrillic(WORD_INPUT.get().upper())
    if len(guess) != LENGTH:
        messagebox.showwarning(config.LENGTH_ERROR_TITLE, config.LENGTH_ERROR_TEXT.format(LENGTH))
        return

    for character in guess:
        if character not in config.CHARSET:
            messagebox.showwarning(config.CHARSET_ERROR_TITLE, config.CHARSET_ERROR_TEXT.format((character)))
            return

    WORD_INPUT.delete(0, END)

    GUESSES_GRID[GUESSNUM] = list(guess)
    GUESSNUM += 1

    render_grid()

    if WORD == guess:  # CORRECT
        messagebox.showinfo(config.WIN_GAME_TITLE, config.WIN_GAME_TEXT.format(WORD.upper()))
        SCORE = (NUM_TRIES - GUESSNUM) * LENGTH
        WIN = True
        ROOT.destroy()
        return

    if GUESSNUM == NUM_TRIES:
        messagebox.showerror(config.OUT_OF_TRIES_ERROR_TITLE, config.OUT_OF_TRIES_ERROR_TEXT.format(WORD.upper()))
        ROOT.destroy()
        return


def play(word_length, num_tries):
    global ROOT, WORD_INPUT, SCORE, WIN

    game_setup(word_length, num_tries)

    ROOT = Tk()
    ROOT.title(config.GAME_TITLE)
    ROOT.config(bg=config.BLACK)

    WORD_INPUT = Entry(ROOT, width=len(WORD) * 10, font='arial 18', justify="center")
    WORD_INPUT.grid(row=999, column=0, pady=(100, 0), columnspan=LENGTH)
    WORD_INPUT.focus_force()

    render_grid()
    ROOT.bind('<Return>', get_guess)
    ROOT.mainloop()

    return WIN, SCORE

