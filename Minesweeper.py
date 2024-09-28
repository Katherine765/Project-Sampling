#Easy dimensions: 10x8, Medium dimensions: 18x14, Hard dimensions: 24x20   #Number of mines goes in order 10, 40, 99
#if you click the same thing a bunch of times, it will count them as new opens

#Imports
import random
from tkinter import *
from copy import copy
from time import sleep, time

#Constants
WIDTH = 10 ; HEIGHT = 8
NUM_MINES = 10
SQUARE_SIZE = 40

#Create dictionaries of coordinates
grid = {(x,y): None for x in range(WIDTH) for y in range(HEIGHT)}
clicked = copy(grid)
flagged = copy(grid)


#Set up checkered canvas
#The coord dict matches the location with the canvas coordinates (of the top right corner of the square)
tk=Tk()
canvas = Canvas(tk, width=WIDTH*SQUARE_SIZE+10, height=HEIGHT*SQUARE_SIZE+60)
canvas.pack()
coords={}
for loc in grid.keys():
    startx = loc[0]*SQUARE_SIZE + 5
    starty = loc[1]*SQUARE_SIZE + 5
    coords[loc] = (startx,starty)
    color = '#C8D8E4' if bool(loc[0] %2 == 0) == bool(loc[1] %2 == 0) else '#A9BBCB'
    canvas.create_rectangle(startx,starty,startx+SQUARE_SIZE,starty+SQUARE_SIZE, fill=color, outline='')


#Returns the 8 blocks surrounding the arguement
def get_touching_locs(loc):
    x = loc[0] ; y = loc[1]
    offsets = [-1, 0, 1]
    touching_locs = [(x + i, y + j) for i in offsets for j in offsets if (x + i, y + j) in grid.keys()]
    touching_locs.remove((x,y))
    return touching_locs

#Chooses the mine locations based on the first click, then runs the click sequence as usual
def set_up_board(event):
    clickx = event.x
    clicky = event.y
    loc = get_square_loc(event.x,event.y)
    cannot = get_touching_locs(loc)
    cannot.append(get_square_loc(clickx,clicky))
    count = 0
    while not count == NUM_MINES:
        mine_location = random.choice(list(grid.keys()))
        if not grid[mine_location] == 'm' and not mine_location in cannot:

            grid[mine_location] = 'm'
            count += 1

    for loc in grid.keys():
        if not grid[loc] == 'm':
            grid_values = [grid[location] for location in get_touching_locs(loc)]
            grid[loc] = grid_values.count('m')

    click(event)


#Given canvas coordinates, retruns a locations that can be used within the dictionaries
def get_square_loc(x,y):
    return (x-5)//SQUARE_SIZE,(y-5)//SQUARE_SIZE

#Runs when a left click occurs, runs the start sequence if it is the first valid click
def click(event):
    global started
    if not started:
        if get_square_loc(event.x, event.y) in grid:
            started = True
            set_up_board(event)
    else:
        clickx = event.x
        clicky = event.y
        loc = get_square_loc(clickx,clicky)
        if loc in grid:
            if grid[loc] == 'm':
                game_over(loc)
                return
            x = coords[loc][0] + SQUARE_SIZE/2
            y = coords[loc][1] + SQUARE_SIZE/2
            if not clicked[loc]:
                clicked[loc]=canvas.create_text(x, y, text=grid[loc], font = f'Helvetica {int(SQUARE_SIZE/2)}')
            if grid[loc] == 0:
                expand(get_touching_locs(loc))

            check_for_win()
    
#Runs when a right click occurs, flags or unflags the square
def flag(event):
    clickx = event.x ; clicky = event.y
    loc = get_square_loc(clickx,clicky)
    coord = coords[loc]
    x = coord[0] ; y = coord[1]
    if flagged[loc]:
        canvas.delete(flagged[loc])
        flagged[loc] = None
    else:
        flagged[loc]=canvas.create_rectangle(x,y,x+SQUARE_SIZE,y+SQUARE_SIZE,fill='#FF6B6B',outline='')

#uses rEcuRsIOn, continues expanding the click until there are no zeros on the outside
def expand(to_do):
    new_to_do = set()
    for loc in to_do:
        x = coords[loc][0] + SQUARE_SIZE/2
        y = coords[loc][1] + SQUARE_SIZE/2
        clicked[loc]=canvas.create_text(x, y, text=grid[loc], font = f'Helvetica {int(SQUARE_SIZE/2)}')
        if grid[loc] == 0:
            new_to_do.update(get_touching_locs(loc))
    new_to_do = {loc for loc in new_to_do if not clicked[loc]}
    if new_to_do:
        expand(new_to_do)
    

def check_for_win():
    opened = 0
    for item in clicked.values():
        if bool(item) is True:
            opened += 1
    if opened == WIDTH*HEIGHT-NUM_MINES:
        total_time = round(time() - start_time)
        canvas.unbind_all('<Button-1>')
        canvas.unbind_all('<Button-3>')
        canvas.create_text((WIDTH*SQUARE_SIZE+10)/2, HEIGHT*SQUARE_SIZE+35, text=f'Winner!    {total_time}s', font = 'Helvetica 20')


def game_over(bad_click_loc):
    canvas.unbind_all('<Button-1>') 
    canvas.unbind_all('<Button-3>') 
    
    mine_locs = [loc for loc in grid.keys() if grid[loc] == 'm']
    random.shuffle(mine_locs)
    #so the clicked mine will explode first
    mine_locs.remove(bad_click_loc)
    mine_locs.insert(0,bad_click_loc)
    for loc in mine_locs:
        startx = loc[0]*SQUARE_SIZE + 5
        starty = loc[1]*SQUARE_SIZE + 5
        canvas.create_rectangle(startx,starty,startx+SQUARE_SIZE,starty+SQUARE_SIZE,fill='#80718C',outline='')  #old color to light: #AFA0AF
        tk.update()
        sleep(.25)


global started
started = False
start_time = time()
canvas.bind_all('<Button-1>', click)
canvas.bind_all('<Button-3>', flag)

tk.mainloop()