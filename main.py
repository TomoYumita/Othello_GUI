from tkinter import *
import numpy as np
# HELLO WORLD

master = Tk()

# Flag:
default_rows = 8
default_columns = 8
canvas_size = 700
canvas_spacing = 100
othello_board_size = canvas_size - canvas_spacing * 2
oval_r_x = othello_board_size / default_columns / 2 * 0.9
oval_r_y = othello_board_size / default_rows / 2 * 0.9
cell_x_span = othello_board_size / default_columns
cell_y_span = othello_board_size / default_rows
turn = 0  # black goes first [black:0, white:1]
counter = 0

# Create game board matrices: NaN = no piece, 0 = black, 1 = white
game_board = np.full([default_rows, default_columns], np.nan)
possible_move_black = np.full([default_rows, default_columns], np.nan)
possible_move_white = np.full([default_rows, default_columns], np.nan)

# Create a rectangular canvas
w = Canvas(master, width=canvas_size, height=canvas_size, bg='#40b840')
w.pack()
w.create_text(100, 650, text='Black: 2', font=("Helvetica", 30), fill="black", tag='black_score',anchor=W)
w.create_text(600, 650, text='White: 2', font=("Helvetica", 30), fill="white", tag='white_score',anchor=E)
w.create_text(350, 50, text='Black\'s turn', font=("Helvetica", 30), fill="black", tag='turn',anchor=N)

# Create vertical & horizontal lines
for i in range(0, default_rows + 1):
    w.create_line(canvas_spacing, (othello_board_size / default_rows * i) + canvas_spacing,
                  othello_board_size + canvas_spacing, (othello_board_size / default_rows * i) + canvas_spacing)
for i in range(0, default_columns + 1):
    w.create_line((othello_board_size / default_columns * i) + canvas_spacing, canvas_spacing,
                  (othello_board_size / default_columns * i) + canvas_spacing, othello_board_size + canvas_spacing)


def place_piece(row, column, player):
    if player == 0:
        color_turn = 'black'
    elif player == 1:
        color_turn = 'white'
    y = (row + 0.5) * cell_x_span + canvas_spacing  # +0.5 marks the center of pieces
    x = (column + 0.5) * cell_y_span + canvas_spacing  # +0.5 marks the center of pieces
    w.create_oval(x - oval_r_x, y - oval_r_y, x + oval_r_x, y + oval_r_y, fill=color_turn)


# Default: 4 pieces are placed in center (TL = BR = black, TR = BL = white)
row_center = int(default_rows / 2)
column_center = int(default_columns / 2)
game_board[row_center, column_center] = game_board[row_center - 1, column_center - 1] = 0  # black_ID
game_board[row_center - 1, column_center] = game_board[row_center, column_center - 1] = 1  # white_ID
# default 4 pieces
place_piece(3, 3, 0)
place_piece(4, 4, 0)
place_piece(3, 4, 1)
place_piece(4, 3, 1)


# Create new circle when mouse is clicked
def update_board(event):
    # Get coordinates of clicked location
    x_click = event.x
    y_click = event.y
    # Allocate to cells
    cell_num_column = int((x_click - canvas_spacing) // cell_x_span)
    cell_num_row = int((y_click - canvas_spacing) // cell_y_span)
    # print(possible_move_black)
    # print(possible_move_white)

    x = (cell_num_column + 0.5) * cell_x_span + canvas_spacing  # +0.5 marks the center of pieces
    y = (cell_num_row + 0.5) * cell_y_span + canvas_spacing  # +0.5 marks the center of pieces
    global turn
    if (canvas_spacing < x < othello_board_size + canvas_spacing) and (
            canvas_spacing < y < othello_board_size + canvas_spacing):
        if turn % 2 == 0:
            player_color = 0  # black
        else:
            player_color = 1  # white

        # print(check_directions(cell_num_row, cell_num_column, player_color))

        # Check if the cell is placable
        if len(check_directions(cell_num_row, cell_num_column, player_color)) == 0:
            print('invalid move, select again')
        else:
            flip(cell_num_row, cell_num_column, player_color)
            place_piece(cell_num_row, cell_num_column, player_color)
            game_board[int(cell_num_row), int(cell_num_column)] = player_color
            print(game_board)
            update_score()  # update score board
            if np.sum(possible_move_black) == 0 and np.sum(possible_move_white) == 0:  # if both players can't place
                # Decide who won
                black_num = np.sum(game_board == 0)
                white_num = np.sum(game_board == 1)
                if black_num > white_num:
                    winner = 'Winner: Black'
                    w.itemconfigure('turn', text=winner, fill='black', font=("Helvetica", 50))
                elif black_num < white_num:
                    winner = 'Winner: White'
                    w.itemconfigure('turn', text=winner, fill='white', font=("Helvetica", 50))
                else:
                    winner = 'Game ended tie! Good Game!'
                    w.itemconfigure('turn', text=winner, fill='Green', font=("Helvetica", 50))
            elif turn % 2 == 0 and np.sum(possible_move_white) != 0:
                turn += 1  # next player
                w.itemconfigure('turn', text='White\'s turn', fill='white')
            elif turn % 2 == 0 and np.sum(possible_move_white) == 0:
                w.itemconfigure('turn', text='White skipped - Black\'s turn', fill='Black')
            elif turn % 2 == 1 and np.sum(possible_move_black) != 0:
                turn += 1  # next player
                w.itemconfigure('turn', text='Black\'s turn', fill='black')
            elif turn % 2 == 1 and np.sum(possible_move_black) == 0:
                w.itemconfigure('turn', text='Black skipped - White\'s turn', fill='White')


# Check all 8 possible directions and return list of direction and number of flippable pieces
def check_directions(r, c, t):
    if t == 0:  # black
        opp_id = 1  # white
    else:
        opp_id = 0  # black
    global counter
    possible_direction_list = []
    # 0 o'clock
    if np.isnan(game_board[r, c]):
        # 0 o'clock
        direction = '0'
        counter = 0

        if 0 <= r - 1 <= default_rows - 1:  # prevent going to the other side
            if game_board[r - 1, c] == opp_id:
                # count how many whites in up direction
                while 0 <= r - 1 - counter <= default_rows - 1:
                    if game_board[r - 1 - counter, c] == opp_id:
                        counter += 1
                    else:
                        break
                    # Only when black found after white add to list as "True"
                    if r - 1 - counter >= 0:  # prevent
                        if game_board[r - 1 - counter, c] == t:
                            temp_list = [direction, counter, 'True']
                            possible_direction_list.append(temp_list)

        # 1.5 o'clock
        direction = '1.5'
        counter = 0
        if 0 <= r - 1 <= default_rows - 1 and 0 <= c + 1 <= default_columns - 1:
            if game_board[r - 1, c + 1] == opp_id:
                # count how many whites in up direction
                while 0 <= r - 1 - counter <= default_rows - 1 and 0 <= c + 1 + counter <= default_columns - 1:
                    if game_board[r - 1 - counter, c + 1 + counter] == opp_id:
                        counter += 1
                    else:
                        break
                # Only when black found after white add to list as "True"
                if r - 1 - counter >= 0 and c + 1 + counter < default_rows:  # prevent
                    if game_board[r - 1 - counter, c + 1 + counter] == t:
                        temp_list = [direction, counter, 'True']
                        possible_direction_list.append(temp_list)

        # 3 o'clock
        direction = '3'
        counter = 0
        if 0 <= c + 1 <= default_columns - 1:  # prevent going to the other side
            if game_board[r, c + 1] == opp_id:
                # count how many whites in up direction
                while 0 <= c + 1 + counter <= default_columns - 1:
                    if game_board[r, c + 1 + counter] == opp_id:
                        counter += 1
                    else:
                        break
                # Only when black found after white add to list as "True"
                if c + 1 + counter < default_columns:  # prevent
                    if game_board[r, c + 1 + counter] == t:
                        temp_list = [direction, counter, 'True']
                        possible_direction_list.append(temp_list)

        # 4.5 o'clock
        direction = '4.5'
        counter = 0
        if 0 <= r + 1 <= default_rows - 1 and 0 <= c + 1 <= default_columns - 1:
            if game_board[r + 1, c + 1] == opp_id:
                # count how many whites in up direction
                while 0 <= r + 1 + counter <= default_rows - 1 and 0 <= c + 1 + counter <= default_columns - 1:
                    if game_board[r + 1 + counter, c + 1 + counter] == opp_id:
                        counter += 1
                    else:
                        break
                # Only when black found after white add to list as "True"
                if r + 1 + counter < default_rows and c + 1 + counter < default_columns:  # prevent
                    if game_board[r + 1 + counter, c + 1 + counter] == t:
                        temp_list = [direction, counter, 'True']
                        possible_direction_list.append(temp_list)

        # 6 o'clock
        direction = '6'
        counter = 0
        if 0 <= r + 1 <= default_rows - 1:  # prevent going to the other side
            if game_board[r + 1, c] == opp_id:
                # count how many whites in up direction
                while 0 <= r + 1 + counter <= default_rows - 1:
                    if game_board[r + 1 + counter, c] == opp_id:
                        counter += 1
                    else:
                        break
                # Only when black found after white add to list as "True"
                if r + 1 + counter < default_rows:  # prevent
                    if game_board[r + 1 + counter, c] == t:
                        temp_list = [direction, counter, 'True']
                        possible_direction_list.append(temp_list)

        # 7.5 o'clock
        direction = '7.5'
        counter = 0
        if 0 <= r + 1 <= default_rows - 1 and 0 <= c - 1 <= default_columns - 1:
            if game_board[r + 1, c - 1] == opp_id:
                # count how many whites in up direction
                while 0 <= r + 1 + counter <= default_rows - 1 and 0 <= c - 1 - counter <= default_columns - 1:
                    if game_board[r + 1 + counter, c - 1 - counter] == opp_id:
                        counter += 1
                    else:
                        break
                    # Only when black found after white add to list as "True"
                    if r + 1 + counter < default_rows and c - 1 - counter >= 0:  # prevent
                        if game_board[r + 1 + counter, c - 1 - counter] == t:
                            temp_list = [direction, counter, 'True']
                            possible_direction_list.append(temp_list)

        # 9 o'clock
        direction = '9'
        counter = 0
        if 0 <= c - 1 <= default_columns - 1:  # prevent going to the other side
            if game_board[r, c - 1] == opp_id:
                # count how many whites in up direction
                while 0 <= c - 1 - counter <= default_columns - 1:
                    if game_board[r, c - 1 - counter] == opp_id:
                        counter += 1
                    else:
                        break
                    # Only when black found after white add to list as "True"
                    if c - 1 - counter >= 0:  # prevent
                        if game_board[r, c - 1 - counter] == t:
                            temp_list = [direction, counter, 'True']
                            possible_direction_list.append(temp_list)

        # 10.5 o'clock
        direction = '10.5'
        counter = 0
        if 0 <= r - 1 <= default_rows - 1 and 0 <= c - 1 <= default_columns - 1:
            if game_board[r - 1, c - 1] == opp_id:
                # count how many whites in up direction
                while 0 <= r - 1 - counter <= default_rows - 1 and 0 <= c - 1 - counter <= default_columns - 1:
                    if game_board[r - 1 - counter, c - 1 - counter] == opp_id:
                        counter += 1
                    else:
                        break
                    # Only when black found after white add to list as "True"
                    if r - 1 - counter >= 0 and c - 1 - counter >= 0:  # prevent
                        if game_board[r - 1 - counter, c - 1 - counter] == t:
                            temp_list = [direction, counter, 'True']
                            possible_direction_list.append(temp_list)

    return possible_direction_list


# Flip pieces
def flip(r, c, t):  # row, column, turn
    global counter
    flip_list = check_directions(r, c, t)
    num_directions_flipped = len(flip_list)
    for d in range(0, num_directions_flipped):
        direction = flip_list[d][0]
        num_pieces = flip_list[d][1]
        print(str(num_pieces) + ' , ' + str(direction))
        if direction == '0':  # 0 o'clcok
            counter = 1
            for n in range(0, num_pieces):
                place_piece(r - counter, c, t)
                game_board[r - counter, c] = t
                counter += 1
        elif direction == '1.5':  # 0 o'clcok
            counter = 1
            for n in range(0, num_pieces):
                place_piece(r - counter, c + counter, t)
                game_board[r - counter, c + counter] = t
                counter += 1
        elif direction == '3':  # 3 o'clcok
            counter = 1
            for n in range(0, num_pieces):
                place_piece(r, c + counter, t)
                game_board[r, c + counter] = t
                counter += 1
        elif direction == '4.5':  # 4.5 o'clcok
            counter = 1
            for n in range(0, num_pieces):
                place_piece(r + counter, c + counter, t)
                game_board[r + counter, c + counter] = t
                counter += 1
        elif direction == '6':  # 6 o'clcok
            counter = 1
            for n in range(0, num_pieces):
                place_piece(r + counter, c, t)
                game_board[r + counter, c] = t
                counter += 1
        elif direction == '7.5':  # 7.5 o'clcok
            counter = 1
            for n in range(0, num_pieces):
                place_piece(r + counter, c - counter, t)
                game_board[r + counter, c - counter] = t
                counter += 1
        elif direction == '9':  # 9 o'clcok
            print('ss')
            counter = 1
            for n in range(0, num_pieces):
                place_piece(r, c - counter, t)
                game_board[r, c - counter] = t
                counter += 1
        elif direction == '10.5':  # 10.5 o'clcok
            counter = 1
            for n in range(0, num_pieces):
                place_piece(r - counter, c - counter, t)
                game_board[r - counter, c - counter] = t
                counter += 1


# Make a matrix of possible moves for inner locations: return 1 if allowed, return 0 if not
def update_score():
    for row in range(0, default_rows):
        for column in range(0, default_columns):
            # make matrices of possible moves for both black and white
            if len(check_directions(row, column, 0)) == 0:
                possible_move_black[row, column] = 0
            else:
                possible_move_black[row, column] = 1

            if len(check_directions(row, column, 1)) == 0:
                possible_move_white[row, column] = 0
            else:
                possible_move_white[row, column] = 1

    # update score board:
    black_num = np.sum(game_board == 0)
    white_num = np.sum(game_board == 1)
    b_var = 'Black: ' + str(black_num)
    w_var = 'White: ' + str(white_num)
    w.itemconfigure('black_score', text=b_var)
    w.itemconfigure('white_score', text=w_var)


w.bind("<Button 1>", update_board)

mainloop()
