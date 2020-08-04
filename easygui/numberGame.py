import random
import easygui as gui

# msgbox title
title = "Number Game"
# min value of the random number
lower_bound = 1
# max value of the random number
upper_bound = 10
# max allowed number of guesses in one game
max_round = 3


def play():
    secret = random.randint(lower_bound, upper_bound)
    for i in range(max_round):
        guess = gui.integerbox(
            "You have {0} chance(s) left! Please guess the number ({1}-{2}):".format(
                max_round - i, lower_bound, upper_bound
            ),
            title,
            None,
            lower_bound,
            upper_bound,
        )
        if guess is None:  # user closed the msgbox
            exit(0)
        elif guess < secret:
            gui.msgbox("Your guess is smaller than the secret number", title)
        elif guess > secret:
            gui.msgbox("Your guess is larger than the secret number", title)
        else:
            gui.msgbox("Congratulations! You win :)", title)
            break
    else:
        gui.msgbox("Sorry, you lose :(", title)


def check():
    if gui.ccbox("Do you want to play another round?", title):
        pass
    else:
        exit(0)


while True:
    play()
    check()
