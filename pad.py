import random


def start_board():
    colors = ['r', 'g', 'b', 'l', 'd', 'h']
    board = []
    for i in range(30):
        board.append(random.choice(colors))
    return board

def gui_board(board):
    toSend = ''
    for i in range(len(board)):
        toSend += board[i] + ' '
        if i == 5:
            toSend += '  |5' + '\n'
        elif i == 11:
            toSend += '  |4' + '\n'
        elif i == 17:
            toSend += '  |3' + '\n'
        elif i == 23:
            toSend += '  |2' + '\n'
        elif i == 29:
            toSend += '  |1' + '\n'
    toSend += '___________' + '\n' + 'A B C D E F'
    return toSend

def analyze(matches):
    print('Analysis:')
    for row_idx in range(len(matches)):
        empty = True
        match_dic = {}
        for colors_idx in range(len(matches[row_idx])):
            if len(matches[row_idx][colors_idx]) != 0:
                empty = False
                if colors_idx == 0:
                    color = 'Red'
                elif colors_idx == 1:
                    color = 'Green'
                elif colors_idx == 2:
                    color = 'Blue'
                elif colors_idx == 3:
                    color = 'Light'
                elif colors_idx == 4:
                    color = 'Dark'
                elif colors_idx == 5:
                    color = 'Heart'
                match_dic[color] = matches[row_idx][colors_idx]
        if empty:
            print(f'Row {row_idx + 1}: No matches.')
        else:
            data = ''
            for key in match_dic:
                data += f'{key}:  {match_dic[key]} '
            print(f'Row {row_idx + 1}: ' + data)

def horizontal_matches(board):
    matches = {'r': [], 'g': [], 'b': [], 'l': [], 'd': [], 'h': []}
    
    # check horizontal matches first
    dont_check = [4, 5, 10, 11, 16, 17, 22, 23, 28, 29]
    for i in range(len(board)): 
        if i not in dont_check:
            if board[i] == board[i + 1] and board[i] == board[i + 2]:
                matches[board[i]].extend([i, i + 1, i + 2])

    # remove duplicate entries from each color
    for key in matches:
        uniq = list(dict.fromkeys(matches[key]))
        matches[key] = uniq

    for key in matches: #  matches[key] = [9, 10, 11, 12, 13, 14, 18, 19, 20]
        groups = [] # will replace original value in key
        # check each orb with every orb on the right of it
        if len(matches[key]) != 0:
            for i in range(len(matches[key]) - 1):
                for j in range(i + 1, len(matches[key])):
                    o1 = matches[key][i]
                    o2 = matches[key][j]
                    if touching(o1, o2): #if they are next to each other vertically or horizontally
                        if len(groups) == 0:
                            groups.append([o1, o2])
                        else:
                            grplen = len(groups)
                            if not any(o1 in sublist for sublist in groups):
                                groups.append([o1, o2])
                            else:
                                for grpi in range(grplen):
                                    if o1 in groups[grpi]:
                                        groups[grpi].append(o2)

        for grpidx in range(len(groups)):
            groups[grpidx] = list(dict.fromkeys(groups[grpidx]))
        
        matches[key] = groups
    return matches

def vertical_matches(board):
    matches = {'r': [], 'g': [], 'b': [], 'l': [], 'd': [], 'h': []}
    
    # check vertical matches
    dont_check = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    for i in range(len(board)): 
        if i not in dont_check:
            if board[i] == board[i + 6] and board[i] == board[i + 12]:
                matches[board[i]].extend([i, i + 6, i + 12])

    # remove duplicate entries from each color
    for key in matches:
        uniq = list(dict.fromkeys(matches[key]))
        matches[key] = uniq
    

    for key in matches:
        groups = []
        if len(matches[key]) != 0:
            for i in range(len(matches[key]) - 1):
                for j in range(i + 1, len(matches[key])):
                    o1 = matches[key][i]
                    o2 = matches[key][j]
                    if touching(o1, o2): #if they are next to each other vertically or horizontally
                        if len(groups) == 0:
                            groups.append([o1, o2])
                        else:
                            grplen = len(groups)
                            if not any(o1 in sublist for sublist in groups):
                                groups.append([o1, o2])
                            else:
                                for grpi in range(grplen):
                                    if o1 in groups[grpi]:
                                        groups[grpi].append(o2)

        for grpidx in range(len(groups)):
            groups[grpidx] = list(dict.fromkeys(groups[grpidx]))
        
        matches[key] = groups
    return matches

def combine_hv_matches(hdic, vdic):
    matches = {'r': [], 'g': [], 'b': [], 'l': [], 'd': [], 'h': []}
    for hkey in hdic:
        for vkey in vdic:
            if hkey == vkey:
                if hdic[hkey] == vdic[vkey]:
                    matches[hkey] = hdic[hkey]
                elif hdic[hkey] == [] and vdic[vkey] != []:
                    matches[hkey] = vdic[vkey]
                elif vdic[vkey] == [] and hdic[hkey] != []:
                    matches[hkey] = hdic[hkey]
                else:
                    mixed = mix(hdic[hkey], vdic[vkey])
                    matches[hkey] = mixed
    
    return matches

def mix(match1, match2):
    combined = []
    
    for arr1 in match1:
        for arr2 in match2:
            if any(x in arr1 for x in arr2): # if match found
                new = []
                new.extend(arr1)
                new.extend(arr2)
                new = list(dict.fromkeys(new))
                combined.append(new)
                if arr1 in combined:
                    combined.remove(arr1)
                if arr2 in combined:
                    combined.remove(arr2)
            else:
                if arr1 not in combined:
                    combined.append(arr1)
                if arr2 not in combined:
                    combined.append(arr2)
    
    for i in range(len(combined) - 1):
        for j in range(i + 1, (len(combined))):
            if any(m in combined[i] for m in combined[j]):
                combined[i].extend(combined.pop(j))
    
    for idx in range(len(combined)):
        combined[idx] = list(dict.fromkeys(combined[idx]))

    return combined

def touching(orb1, orb2):
    row_end = [5, 11, 17, 23, 29]
    if (orb1 % 6 == orb2 % 6 and abs(orb1 - orb2) == 6) or (abs(orb1 - orb2) == 1 and orb1 not in row_end):
        return True
    else:
        return False

def matches_exist(board):
    h_matches = horizontal_matches(board)
    v_matches = vertical_matches(board)
    combined_matches = combine_hv_matches(h_matches, v_matches)
    # print(combined_matches)

    for key in combined_matches:
        if len(combined_matches[key]) > 0:
            return [True, combined_matches]
    
    return [False, combined_matches]


def clear_matches(board, matches):

    remove = []
    
    for key in matches:
        for inner_arr in matches[key]:
            for num in inner_arr:
                remove.append(num)

    for num in remove:
        board[num] = 'x'

    push_down(board)
    replaced_board = replace_x(board)
    
    return replaced_board


def x_on_board(the_board):
    for orb in the_board:
        if orb == 'x':
            return True
    
    return False

def push_down(x_board):
    for i in range(len(x_board)):
        if x_board[i] != 'x':
            move = i
            copy = x_board[i]
            for j in range(i + 6, len(x_board), 6):
                if x_board[j] == 'x':
                    move = j
                    x_board[i] = 'x'
                else:
                    break
            x_board[move] = copy

def replace_x(x_board):
    colors = ['r', 'g', 'b', 'l', 'd', 'h']
    for i in range(len(x_board)):
        if x_board[i] == 'x':
            x_board[i] = random.choice(colors)

    return x_board

def random_coordinates(the_board):
    random_int = random.randint(0, 29)
    random_orb = the_board[random_int]

    if random_int >= 0 and random_int < 6:
        number = '5'
    elif random_int >= 6 and random_int < 12:
        number = '4'
    elif random_int >= 12 and random_int < 18:
        number = '3'
    elif random_int >= 18 and random_int < 24:
        number = '2'
    elif random_int >= 24 and random_int < 30:
        number = '1'

    if random_int % 6 == 0:
        letter = 'A'
    elif random_int % 6 == 1:
        letter = 'B'
    elif random_int % 6 == 2:
        letter = 'C'
    elif random_int % 6 == 3:
        letter = 'D'
    elif random_int % 6 == 4:
        letter = 'E'
    elif random_int % 6 == 5:
        letter = 'F'
    
    coordinate = letter + number
    return coordinate, random_orb

def invalid_coordinates(coords):
    if len(coords) > 2 or len(coords) < 2:
        return True
    if not coords[0].isalpha():
        return True
    if not coords[1].isnumeric():
        return True
    if coords[0].upper() != 'A' and coords[0].upper() != 'B' and coords[0].upper() != 'C' and coords[0].upper() != 'D' and coords[0].upper() != 'E' and coords[0].upper() != 'F':
        return True
    if int(coords[1]) > 5 or int(coords[1]) < 1:
        return True
    return False

def initialize_board():
    my = ''
    new_board = []
    if my == '':
        new_board = start_board()
    else:
        for letter in my:
            new_board.append(letter.lower())
    
    return new_board


def main():
    board = initialize_board()

    while matches_exist(board)[0] == True:
        board = clear_matches(board, matches_exist(board)[1])
    print()
    print('Welcome to my Puzzle & Dragons replica program built with Python.')
    print('Beneath is the board which you will be able to play PAD like normal, just in a much uglier fashion.')
    print('First you need to select the orb which you want to pick up. The board is shown with chessboard coordinates.')
    print()
    rand_coor, rand_orb = random_coordinates(board)
    print(gui_board(board))
    print()
    print(f'For example, {rand_coor} is {rand_orb}')

    user_coordinates = input("Enter the coordinates of the orb you wish to select (capitalization doesn't matter): ")
    while invalid_coordinates(user_coordinates):
        user_coordinates = input('Invalid coordinates. Try again: ')

    

main()

'''
general outline of code:


--------------------------------------------
1. main will initialize a board in an [array]
--------------------------------------------

->

--------------------------------------------
MATCH EXIST LOOP:
    if matches exist, return [true, matches dictionary]
    otherwise return [false, matches dictionary]
    
    while matches exist:
        

'''