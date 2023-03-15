import random
import sys
import time

# Global Variables
w, h = 9, 9
num_mines = 9
board = {}
board_flags = {}


# slow text display.
def typing_print(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)


# Display Instructions.
def disp_instructions():
    print()
    typing_print("Minesweeper Python 2023 \n")
    typing_print("=======================\n")
    typing_print("Mines will be placed on a game board.\n")
    typing_print("you will have the option of selecting a square.\n")
    typing_print("If you select a mine. you loose.\n")
    typing_print("If you select a open spot a section of the board will be displayed.\n")
    typing_print("If you select a spot that contains a proximity number then it will inform\n")
    typing_print("you that there are mines near by.  You will have to try to determine their\n")
    typing_print("placement.  If you think you know you can place a marker on the mine to\n")
    typing_print("mark that spot.\n")
    typing_print("You win if you can clear the board without hitting any mines.\n")
    print()


# Level Choose
def level_select():
    global w, h, num_mines
    level = int(input("Lets select level (1- Beginner, 2- Medium, 3- Advanced) : "))
    # level = 1
    # Beginner – 9 * 9 Board and 10 Mines
    # Intermediate – 16 * 16 Board and 40 Mines
    # Advanced – 24 * 24 Board and 99 Mines
    if level == 1:
        w, h = 9, 9
        num_mines = 10
    if level == 2:
        w, h = 16, 16
        num_mines = 40
    if level == 3:
        w, h = 24, 24
        num_mines = 99


# Init the Board
def init_board():
    # wipe boards
    for x in range(0, h):
        for y in range(0, w):
            board[x, y] = 0
            board_flags[x, y] = " "
    # set mine locations
    for z in range(0, num_mines):
        pick = True
        while pick:
            x1 = random.randint(0, h-1)
            y1 = random.randint(0, w-1)
            chk = board[x1, y1]
            if chk == 0:
                board[x1, y1] = -1
                pick = False
            else:
                pick = True
    # set board values based on mine locations
    for x in range(0, h):
        for y in range(0, w):
            check_neighbours(x, y)


# Show where mines are.
def show_mines():
    for x in range(0, h):
        for y in range(0, w):
            if board[x, y] == -1:
                board_flags[x, y] = "X"


# Check for Win condition.
def check_win():
    flg_correct = 0
    flg_return = False
    for x in range(0, h):
        for y in range(0, w):
            if board_flags[x, y] == "P" and board[x, y] == -1:
                flg_correct += 1
    if flg_correct == num_mines:
        print("you have marked all Mines Correctly - You win.")
        flg_return = True
    return flg_return


# Check spots (1) is for adjacent counts, (2) is for Select check.
def check_neighbours_spot(x_line, y_line, typ):
    try:
        tl = board[x_line, y_line]
    except KeyError:
        return

    if typ == 1:
        if tl != -1:
            k = int(tl)
            k += 1
            board[x_line, y_line] = k
    else:
        if tl == -1:
            board_flags[x_line, y_line] = 'X'
        else:
            board_flags[x_line, y_line] = str(tl)


# check eight squares around selected spot.
def check_neighbours(x, y):
    if board[x, y] == -1:
        checklist = [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1],
                     [x, y - 1], [x, y + 1],
                     [x + 1, y - 1], [x + 1, y], [x + 1, y + 1]]
        for itm in checklist:
            check_neighbours_spot(itm[0], itm[1], 1)


# Set spots as visible on game board
def reveal_neighbours(x, y):
    # After 1st spot.
    checklist = [[x - 1, y - 1], [x - 1, y], [x - 1, y + 1],
                 [x, y - 1], [x, y + 1],
                 [x + 1, y - 1], [x + 1, y], [x + 1, y + 1]]

    for itm in checklist:
        try:
            tf = board_flags[itm[0], itm[1]]
            tl = board[itm[0], itm[1]]
            if tf == ' ':
                if tl > 0:
                    check_neighbours_spot(itm[0], itm[1], 2)
                if tl == 0:
                    check_neighbours_spot(itm[0], itm[1], 2)
                    # Here is recursive for opening up other empty spaces around.
                    reveal_neighbours(itm[0], itm[1])
        except KeyError:
            x = 0


# Display Current Board
def disp_board(typ):
    print(' ' * 6, end="")
    for z in range(0, w):
        print(" {:^2} ".format(z), end="")
    print()
    print('-' * (w*4 + 8), end="")
    print()
    for x in range(0, h):
        print(" {:^2} ".format(x), "|", end="")
        for y in range(0, w):
            if typ == 1:
                print(" {:^2} ".format(board_flags[x, y]), end="")
            else:
                print(" {:^2} ".format(board[x, y]), end="")
        print("|")
    print('-' * (w*4 + 8), end="")
    print()


# Main Game Run
def mine_sweeper():
    try_again = 1
    while try_again == 1:
        # Init
        disp_instructions()
        level_select()
        init_board()
        playing = True
        # Game Loop
        while playing:
            # disp_board(0)
            disp_board(1)
            my_selection = ""
            # Only valid selection.
            while my_selection == "":
                my_selection = input("Function : (S)elect location, (T)oggle Flag, (Q)uit :")
                my_selection = my_selection.upper()
                if my_selection != "S" and my_selection != "T" and my_selection != "Q":
                    my_selection = ""

            if my_selection != "Q":
                my_move_x = int(input("X:"))
                my_move_y = int(input("Y:"))

                if my_selection == "T":
                    tf = board_flags[my_move_x, my_move_y]
                    if tf == "P":
                        board_flags[my_move_x, my_move_y] = " "
                    else:
                        board_flags[my_move_x, my_move_y] = "P"

                if my_selection == "S":
                    tl = board[my_move_x, my_move_y]
                    tf = board_flags[my_move_x, my_move_y]
                    if tl == -1:
                        show_mines()
                        disp_board(1)
                        print("MINE!!! - Game Over.")
                        playing = False
                    else:
                        if tf == " ":
                            # open up space.
                            check_neighbours_spot(my_move_x, my_move_y, 2)
                            if tl == 0:
                                reveal_neighbours(my_move_x, my_move_y)
                        else:
                            if int(tf) > 0:
                                board_flags[my_move_x, my_move_y] = board[my_move_x, my_move_y]
            else:
                playing = False

            if check_win():
                playing = False

        try_again = int(input("Would you like to play another game (1- Yes / 2- No) :"))

    print()
    print("End of Line.")


mine_sweeper()
