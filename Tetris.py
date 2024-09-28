import random
from tkinter import *
from copy import copy
from itertools import chain

WIDTH = 10 ; HEIGHT = 19 ; SQUARE_SIZE = 30
shapes = {'#0DFF72': [(5, 0), (5, 1), (5, 2), (5, 3)], '#0EC2FF': [(4, 0), (5, 0), (4, 1), (5, 1)],
    '#3878FF': [(3, 0), (4, 0), (4, 1), (5, 1)], '#FFE138': [(4, 0), (5, 0), (3, 1), (4, 1)],
    '#F438FF': [(4, 0), (4, 1), (4, 2), (5, 2)], '#FF8E0C': [(4, 0), (4, 1), (3, 2), (4, 2)],
    '#FF0D73': [(3, 0), (4, 0), (5, 0), (4, 1)]}
references = {'#0DFF72': (4.5,1.5), '#0EC2FF': (4.5,0.5), '#3878FF': (4.5,0.5), '#FFE138': (4.5,.5),
    '#F438FF': (4.5, 1.5), '#FF8E0C': (4.5, 1.5), '#FF0D73': (4.5,0.5) }


class Tetris():
    def __init__(s, width, height, square_size, root, canvas):
        s.root = root ; s.canvas = canvas

        s.current_color = None ; s.current_locs = None ; s.current_ref = None
        s.square_size = square_size ; s.width = width ; s.height = height ; s.top = height
        s.grid = {(x,y): 'black' for y in range(height) for x in range(width) }
        s.no_zone = [(x,y) for x in range(width) for y in range(4)]

        s.coords = {}
        for loc in s.grid:
            x = loc[0]*square_size + 5
            y = loc[1]*square_size  + 5
            s.coords[loc] = (x,y)

        s.score = 0
        s.score_text = s.canvas.create_text((width*square_size+10)/2, height*square_size+35, text=str(s.score), font='Helvetica 20')
            
        s.spawn()
        s.fall_constant()
        s.de_lag() #also functions to draw the original screen

    def spawn(s):
        s.current_color = random.choice(list(shapes.keys()))
        s.current_locs = shapes[s.current_color]
        s.current_ref = references[s.current_color]
        for loc in shapes[s.current_color]:
            s.grid[loc] = s.current_color
            
        s.update(s.current_locs)

    def update(s, *locs):
        locs = set(chain(*locs)) if locs[0] else list(s.grid.keys())
        for loc in locs:
            x = s.coords[loc][0]
            y = s.coords[loc][1]
            s.canvas.create_rectangle(x,y,x+s.square_size,y+s.square_size, fill=s.grid[loc], outline='')
            
    def turn(s, event):
        if s.current_color == '#0EC2FF': #square
            return
        orig_locs = s.current_locs
        new_locs = []
        for loc in s.current_locs:
            step1 = (loc[0]-s.current_ref[0], loc[1]-s.current_ref[1])
            new_locs.append((-step1[1]+s.current_ref[0], step1[0]+s.current_ref[1]))

        if s.move(new_locs):
            s.update(orig_locs,s.current_locs)
        #new section, sometimes will move over for blocks though, get the numbers right
        elif s.current_locs[0][0] < 3:
            for x in range(2):
                new_locs = [(loc[0]+1,loc[1]) for loc in new_locs]
                if s.move(new_locs):
                    s.update(orig_locs,s.current_locs)
                    break
        elif s.current_locs[0][0] > s.width-3:
            for x in range(2):
                new_locs = [(loc[0]-1,loc[1]) for loc in new_locs]
                if s.move(new_locs):
                    s.update(orig_locs,s.current_locs)
                    break

    def move(s, new_locs):
        for loc in new_locs:
            if not loc in s.grid:
                return False
            if not s.grid[loc] == 'black' and not loc in s.current_locs:
                return False  
        for loc in s.current_locs:
            s.grid[loc] = 'black'
        for loc in new_locs:
            s.grid[loc] = s.current_color
        
        s.current_locs = new_locs
        return True

    def left(s,event):
        orig_locs = s.current_locs
        if s.move([(loc[0]-1,loc[1]) for loc in s.current_locs]):
            s.current_ref = (s.current_ref[0]-1, s.current_ref[1])
            s.update(orig_locs, s.current_locs)
                    
        
    def right(s,event):
        orig_locs = s.current_locs
        if s.move([(loc[0]+1,loc[1]) for loc in s.current_locs]):
            s.current_ref = (s.current_ref[0]+1, s.current_ref[1])
            s.update(orig_locs, s.current_locs)

    def fall_constant(s):
        orig_locs = s.current_locs
        if s.move([(loc[0],loc[1]+1) for loc in s.current_locs]):
            s.update(orig_locs, s.current_locs)
            s.current_ref = (s.current_ref[0], s.current_ref[1]+1)
        else:
            s.land_sequence()
                
        s.root.after(250, s.fall_constant)

    def touching(s):
        for loc in s.current_locs:
            below = (loc[0],loc[1]+1)
            if not below in s.grid:
                return True
            elif s.grid[below] == 'black' and not below in s.current_locs:
                return True
        return False

    def fall_full(s,event):
        orig_locs = copy(s.current_locs)
        falling = True
        while falling:
            if s.move([(loc[0],loc[1]+1) for loc in s.current_locs]):
                s.score += 1
                s.canvas.delete(s.score_text)
                s.score_text = s.canvas.create_text((s.width*s.square_size+10)/2, s.height*s.square_size+35, text=str(s.score), font='Helvetica 20')
                s.current_ref = (s.current_ref[0], s.current_ref[1]+1)
            else:
                #what has been done in the previous movements
                s.update(orig_locs,s.current_locs)
                falling = False


        s.update(orig_locs)
        s.land_sequence()

    def de_lag(s):
        s.canvas.delete('all')
        s.update(False)
        s.score_text = s.canvas.create_text((s.width*s.square_size+10)/2, s.height*s.square_size+35, text=str(s.score), font='Helvetica 20')
        s.root.after(20000, s.de_lag) #every twenty seconds
        


    def land_sequence(s):
        for loc in s.current_locs:
            if loc[1] < s.top:
                s.top = int(loc[1])
        to_update = []
        #we don't know if this row is full yet, but most of the code only runs if it is so this name is less confusing then
        for full_row_num in range(s.top, s.height):
            row_colors = [s.grid[(x, full_row_num)] for x in range(s.width)]
            if not 'black' in row_colors:
                row_locs = [(x, full_row_num) for x in range(s.width)]
                to_update.extend(row_locs)
                s.score += 10
                s.canvas.delete(s.score_text)
                s.score_text = s.canvas.create_text((s.width*s.square_size+10)/2, s.height*s.square_size+35, text=str(s.score), font='Helvetica 20')
                for loc in row_locs:
                    s.grid[loc] = 'black'

                rows_to_move = [row_num for row_num in range(s.top, s.height) if row_num < full_row_num]
                to_move = [(x,y) for x in range(s.width) for y in rows_to_move]
                to_update.extend(to_move)

                for loc in reversed(to_move):
                    s.grid[(loc[0],loc[1]+1)] = s.grid[loc]
                    s.grid[loc] = 'black'
    
                s.top += 1      
    
        s.update(to_update)
        
        if s.top < 4 :
            canvas.unbind_all('<Down>') 
            canvas.unbind_all('<Up>')
            canvas.unbind_all('<Left>') 
            canvas.unbind_all('<Right>')
            canvas.unbind_all('<space>')
        else:
            s.spawn()


root=Tk()
canvas = Canvas(root, width=WIDTH*SQUARE_SIZE+10, height=HEIGHT*SQUARE_SIZE+60)
canvas.pack()
t = Tetris(WIDTH, HEIGHT, SQUARE_SIZE, root, canvas)

canvas.bind_all('<Down>', t.fall_full)
canvas.bind_all('<Up>', t.turn)
canvas.bind_all('<Left>', t.left)
canvas.bind_all('<Right>', t.right)
root.mainloop()