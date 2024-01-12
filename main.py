from tkinter import *
import config, game
from tkinter import messagebox


def wriite_history(win, score, length):
    with open(config.HISTORY_PATH, 'a') as file:
        file.write(' '.join([str(win), str(score), str(length)])+'\n')


ROOT = Tk()
ROOT.title(config.GAME_TITLE)
ROOT.config()

length_label = Label(ROOT, text='Дужина следеће речи', font='arial 14')
length_label.grid(row=1, column=0, pady=(10, 10), padx=(10, 10))
length_input = Entry(ROOT, width=5, font='arial 18', justify='center')
length_input.grid(row=1, column=1, pady=(10, 10), padx=(10, 10))
length_input.focus_set()


def start_game():
    length = length_input.get()
    try:
        length = int(length)
    except ValueError:
        messagebox.showwarning('Грешка', 'Број слова мора бити цео број (3-10)')
        return

    length_input.focus_set()
    win, score = game.play(length, 6)
    print(win, score)
    wriite_history(win, score, length)


start_button = Button(ROOT, text='Почни игру', font='arial 14', command=start_game)
start_button.grid(row=2, column=0, pady=(10, 10), padx=(10, 10), columnspan=2)

ROOT.mainloop()

