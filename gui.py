import pygame
import time
from queue import PriorityQueue
import copy
import random
pygame.init()   #initialize pygame


win = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("3x3 Sliding Puzzle Solver")
line_color = (192, 192, 192)
line_width = 7
width = 193
height = 193
vel = 2     #velocity of moving piece
tile_color = (102, 102, 255)
default_font = pygame.font.SysFont("comicsansms", 68)
solved_moves = {}

board = [
    [6, 7, 5],
    [3, 2, 4],
    [1, 8, 0],
]

board_solved = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0],
]

positions = {}
total_moves = 0
initial = copy.deepcopy(board)

class Button:
    def __init__(self, color, x, y, width, height, font_size, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size

    def draw(self, win, outline=None):  #draws button outline
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4))

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        if self.text != '':   #center aligns text on button
            button_font = pygame.font.SysFont("comicsansms", self.font_size)
            text = button_font.render(self.text, True, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):  #checks if mouse position over button
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


button1 = Button((0,255,0), 675, 50, 250, 100, 60, "Solve")
button2 = Button((0,255,0), 675, 180, 250, 100, 60, "Reset")
button3 = Button((0,255,0), 675, 310, 250, 100, 45, "Randomize")


def show_score():   #displays user's total moves
    score = default_font.render("Moves: " + str(total_moves), True, line_color)
    win.blit(score, (645, 435))


def find_nums(board): #translates the numbers in variable 'board', into the numbers' position on the GUI board
    for n in range(0,9):
        for i in range(len(board)):  #i = row
            for j in range(len(board[0])):  #j = column
                if board[i][j] == n:
                    if i == 0:
                        positions["y%s" %n] = 7   #changing row affects y coordinate
                    if i == 1:
                        positions["y%s" %n] = 205
                    if i == 2:
                        positions["y%s" %n] = 403
                    if j == 0:
                        positions["x%s" %n] = 7  #changing column affects x coordinate
                    if j == 1:
                        positions["x%s" %n] = 205
                    if j == 2:
                        positions["x%s" %n] = 403


def translate_board():  #translates the GUI board numbers into the variable 'board'
    for n in range(0,9):
        if positions["y%s" %n] == 7:
            i = 0
        if positions["y%s" %n] == 205:
            i = 1
        if positions["y%s" %n] == 403:
            i = 2
        if positions["x%s" %n] == 7:
            j = 0
        if positions["x%s" %n] == 205:
            j = 1
        if positions["x%s" %n] == 403:
            j = 2
        board[i][j] = n
        find_nums(board)  #thus, moving the GUI board updates the variable 'board' each time


def is_solvable():
    inversions = 0
    for i in range(1, 9):
        x1, y1 = find(board, i)
        for j in range(i + 1, 9):
            x2, y2 = find(board, j)
            if x2 - x1 == 0 and y2 - y1 < 0:
                inversions += 1
            elif x2 - x1 < 0:
                inversions += 1
    if inversions % 2 == 0:
        return True
    else:
        return False


def find(board, num):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == num:
                return (i, j)  # row, col


def grid():   #creates the grid lines
    pygame.draw.line(win, line_color, (0, 3), (598, 3), line_width)
    pygame.draw.line(win, line_color, (0, 201), (598, 201), line_width)
    pygame.draw.line(win, line_color, (0, 399), (598, 399), line_width)  #horz
    pygame.draw.line(win, line_color, (0, 597), (598, 597), line_width)

    pygame.draw.line(win, line_color, (3, 0), (3, 600), line_width)
    pygame.draw.line(win, line_color, (201, 0), (201, 600), line_width)
    pygame.draw.line(win, line_color, (399, 0), (399, 600), line_width)  #vert
    pygame.draw.line(win, line_color, (597, 0), (597, 600), line_width)


def redraw_window():   #redraws the grid, square tiles, numbers, score, and buttons
    win.fill((0, 0, 0))
    grid()
    pygame.draw.rect(win, tile_color, (positions["x1"], positions["y1"], width, height))
    pygame.draw.rect(win, tile_color, (positions["x2"], positions["y2"], width, height))
    pygame.draw.rect(win, tile_color, (positions["x3"], positions["y3"], width, height))
    pygame.draw.rect(win, tile_color, (positions["x4"], positions["y4"], width, height))
    pygame.draw.rect(win, tile_color, (positions["x5"], positions["y5"], width, height))
    pygame.draw.rect(win, tile_color, (positions["x6"], positions["y6"], width, height))
    pygame.draw.rect(win, tile_color, (positions["x7"], positions["y7"], width, height))
    pygame.draw.rect(win, tile_color, (positions["x8"], positions["y8"], width, height))
    num1 = default_font.render("1", True, line_color)
    win.blit(num1, (positions["x1"] + 80, positions["y1"] + 35))
    num2 = default_font.render("2", True, line_color)
    win.blit(num2, (positions["x2"] + 80, positions["y2"] + 35))
    num3 = default_font.render("3", True, line_color)
    win.blit(num3, (positions["x3"] + 80, positions["y3"] + 35))
    num4 = default_font.render("4", True, line_color)
    win.blit(num4, (positions["x4"] + 80, positions["y4"] + 35))
    num5 = default_font.render("5", True, line_color)
    win.blit(num5, (positions["x5"] + 80, positions["y5"] + 35))
    num6 = default_font.render("6", True, line_color)
    win.blit(num6, (positions["x6"] + 80, positions["y6"] + 35))
    num7 = default_font.render("7", True, line_color)
    win.blit(num7, (positions["x7"] + 80, positions["y7"] + 35))
    num8 = default_font.render("8", True, line_color)
    win.blit(num8, (positions["x8"] + 80, positions["y8"] + 35))
    show_score()
    button1.draw(win, (255, 255, 255))
    button2.draw(win, (255, 255, 255))
    button3.draw(win, (255, 255, 255))
    pygame.display.update()


grid()
count = 0   #for A* search algorithm
counter = 0  #for randomization button

find_nums(board) #translates numbers on variable 'board' to the GUI
running = True  #keeps the GUI running
moved = False  #for moving tiles with arrow keys

while running:
    translate_board()  #translates GUI board numbers to the variable 'board'
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:  #makes it so that holding down the arrow keys will not move a piece more than once
            moved = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.isOver(pos):  #if button 1 clicked, board will solve
                button1.color = (255,0,0)
                button1.text = "Solving..."

                total_moves = 0
                count = 0
                translate_board()
                initial = copy.deepcopy(board)
                board_previous = copy.deepcopy(board)


                def is_solvable():
                    inversions = 0
                    for i in range(1, 9):
                        x1, y1 = find(board, i)
                        for j in range(i + 1, 9):
                            x2, y2 = find(board, j)
                            if x2 - x1 == 0 and y2 - y1 < 0:
                                inversions += 1
                            elif x2 - x1 < 0:
                                inversions += 1
                    if inversions % 2 == 0:
                        return True
                    else:
                        return False


                def backtrack(n1):
                    current = n1
                    g_score = 0
                    solved = False
                    if current == board_solved:
                        for x in current:
                            print(x)
                        print("\n")
                    while current != came_from["previous_node0"]:
                        if current == board_solved:
                            solved = True
                            solved_moves["move%s" % g_score] = current
                        for i in range(0, len(nodes.keys())):
                            if nodes["node%s" % i] == current:
                                current = came_from["previous_node%s" % i]
                                g_score += 1
                                if solved:
                                    solved_moves["move%s" % g_score] = current
                                    for x in current:
                                        print(x)
                                    print("\n")
                                    if current == initial:
                                        print(str(g_score) + " moves \n")
                                if current == came_from["previous_node0"]:
                                    return g_score

                                break


                def distance():
                    man = 0
                    for i in range(1, 9):
                        x1, y1 = find(board, i)
                        x2, y2 = find(board_solved, i)
                        distance = abs(x2 - x1) + abs(y2 - y1)
                        man += distance
                    return man


                def RLrestrict():
                    global allow_r
                    global allow_l
                    allow_r = True
                    allow_l = True
                    for i in range(0, 3):
                        if board[i][0] == 0:
                            allow_l = False
                        elif board[i][2] == 0:
                            allow_r = False


                def UDrestrict():
                    global allow_u
                    global allow_d
                    allow_u = True
                    allow_d = True
                    for i in range(0, 3):
                        if board[0][i] == 0:
                            allow_u = False
                        if board[2][i] == 0:
                            allow_d = False


                def find(board, num):
                    for i in range(len(board)):
                        for j in range(len(board[0])):
                            if board[i][j] == num:
                                return (i, j)  # row, col


                def right():
                    i, j = find(board, 0)
                    board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]
                    return board


                def up():
                    i, j = find(board, 0)
                    board[i][j], board[i - 1][j] = board[i - 1][j], board[i][j]
                    return board


                def left():
                    i, j = find(board, 0)
                    board[i][j], board[i][j - 1] = board[i][j - 1], board[i][j]
                    return board


                def down():
                    i, j = find(board, 0)
                    board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]
                    return board


                class Node:
                    def __init__(self, position, f_score):
                        self.position = position
                        self.f_score = f_score


                def in_closed(n1):
                    if len(closed_set) == 1:
                        return False
                    if n1 == closed_set["start"]:
                        return True
                    if n1 in closed_set.values():
                        return True
                    return False


                n1 = Node(board, distance())
                open_set = PriorityQueue()
                nodes = {}
                closed_set = {}
                came_from = {}
                closed_set["start"] = copy.deepcopy(board)

                if is_solvable():
                    while board != board_solved:
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                        RLrestrict()
                        UDrestrict()
                        if allow_r:
                            n1.position = right()
                            if in_closed(n1.position):
                                left()
                            if not in_closed(n1.position):
                                nodes["node%s" % count] = n1.position
                                came_from["previous_node%s" % count] = copy.deepcopy(left())
                                n1.position = copy.deepcopy(right())
                                h_score = distance()
                                n1.f_score = h_score + backtrack(n1.position)
                                open_set.put((n1.f_score, h_score, count, n1.position))
                                board = copy.deepcopy(board_previous)
                                count += 1


                        if allow_l:
                            n1.position = left()
                            if in_closed(n1.position):
                                right()
                            if not in_closed(n1.position):
                                nodes["node%s" % count] = n1.position
                                came_from["previous_node%s" % count] = copy.deepcopy(right())
                                n1.position = copy.deepcopy(left())
                                h_score = distance()
                                n1.f_score = h_score + backtrack(n1.position)
                                open_set.put((n1.f_score, h_score, count, n1.position))
                                board = copy.deepcopy(board_previous)
                                count += 1


                        if allow_u:
                            n1.position = up()
                            if in_closed(n1.position):
                                down()
                            if not in_closed(n1.position):
                                nodes["node%s" % count] = n1.position
                                came_from["previous_node%s" % count] = copy.deepcopy(down())
                                n1.position = copy.deepcopy(up())
                                h_score = distance()
                                n1.f_score = h_score + backtrack(n1.position)
                                open_set.put((n1.f_score, h_score, count, n1.position))
                                board = copy.deepcopy(board_previous)
                                count += 1


                        if allow_d:
                            n1.position = down()
                            if in_closed(n1.position):
                                up()
                            if not in_closed(n1.position):
                                nodes["node%s" % count] = n1.position
                                came_from["previous_node%s" % count] = copy.deepcopy(up())
                                n1.position = copy.deepcopy(down())
                                h_score = distance()
                                n1.f_score = h_score + backtrack(n1.position)
                                open_set.put((n1.f_score, h_score, count, n1.position))
                                board = copy.deepcopy(board_previous)
                                count += 1

                        next_item = open_set.get()[3]
                        board = copy.deepcopy(next_item)
                        find_nums(board)  #variable 'board' translates to GUI board
                        redraw_window()

                        if board == board_solved:
                            print("SOLVED")
                            break
                        closed_set["node%s" % count] = copy.deepcopy(next_item)
                        board_previous = copy.deepcopy(board)

                    else:
                        print("BOARD NOT SOLVABLE")

                    print(str(len(closed_set)) + " nodes explored")
                    print(str(len(nodes)) + " nodes total")
                    total_moves = 0
                    for n in range(0, len(solved_moves)):  #board solves by itself on GUI
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)  #without this, clicking mouse will crash GUI
                        time.sleep(1)  #EDIT TIME IF YOU WANT TO SLOW DOWN BOARD SHOWING SOLUTION
                        find_nums(solved_moves["move%s" % (len(solved_moves) - n - 1)])
                        redraw_window()
                        if n != len(solved_moves) - 1:
                            total_moves += 1
                    solved_moves = {}
                    button1.color = (0, 255, 0)
                    button1.text = "Solve"
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

            else:
                button1.color = (0,255,0)
                button1.text = "Solve"

            if button2.isOver(pos):  #resets board based on inital position (or last randomization)
                button2.color = (255,0,0)
                board = copy.deepcopy(initial)
                find_nums(board)
                redraw_window()
                button2.color = (0,255,0)
                total_moves = 0

            if button3.isOver(pos):  #board randomizes
                if board[2][2] != 0:
                    i, j = find(board, 0)
                    board[i][j], board[2][2] = board[2][2], board[i][j]
                button3.color = (255, 0, 0)
                total_moves = 0
                unsolvable = False

                def randomize():
                    global unsolvable
                    global counter
                    while counter < 8 or unsolvable:  #increasing the number (8 in this case) will intensify randomization visual
                        tiles = [1, 2, 3, 4, 5, 6, 7, 8]
                        for i in range(0, 3):
                            for j in range(0, 3):
                                if i == 2 and j == 2:
                                    pass
                                else:
                                    num = random.choice(tiles)
                                    board[i][j] = num
                                    tiles.remove(num)
                                    find_nums(board)
                                    redraw_window()
                        counter += 1
                        unsolvable = False
                    if not is_solvable():
                        unsolvable = True
                        randomize()
                        unsolvable = True
                    else:
                        unsolvable = False
                randomize()
                counter = 0
                button3.color = (0, 255, 0)
                initial = copy.deepcopy(board)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:  #moves board piece left of empty space right
        for n in range(1,9):
            if positions["x0"] - 198 == positions["x%s" %n] and positions["y0"] - positions["y%s" %n] == 0 and not moved:
                count = 0
                positions["x0"] -= 198
                while count < 99:   #makes sure board piece stays in grid
                    positions["x%s" %n] += vel
                    count += 1
                moved = True
                total_moves += 1


    if keys[pygame.K_LEFT]:  #moves board piece right of empty space left
        for n in range(1, 9):
            if positions["x0"] + 198 == positions["x%s" %n] and positions["y0"] - positions["y%s" %n] == 0 and not moved:
                count = 0
                positions["x0"] += 198
                while count < 99:  #makes sure board piece stays in grid
                    positions["x%s" % n] -= vel
                    count += 1
                moved = True
                total_moves += 1

    if keys[pygame.K_UP]:   #moves board piece below of empty space up
        for n in range(1, 9):
            if positions["y0"] + 198 == positions["y%s" %n] and positions["x0"] - positions["x%s" %n] == 0 and not moved:
                count = 0
                positions["y0"] += 198
                while count < 99:  #makes sure board piece stays in grid
                    positions["y%s" % n] -= vel
                    count += 1
                moved = True
                total_moves += 1

    if keys[pygame.K_DOWN]:  #moves board piece above of empty space down
        for n in range(1, 9):
            if positions["y0"] - 198 == positions["y%s" %n] and positions["x0"] - positions["x%s" %n] == 0 and not moved:
                count = 0
                positions["y0"] -= 198
                while count < 99:  #makes sure board piece stays in grid
                    positions["y%s" % n] += vel
                    count += 1
                moved = True
                total_moves += 1

    redraw_window()
pygame.quit()

