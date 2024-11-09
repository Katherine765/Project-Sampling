import random
from tkinter import *
from copy import copy
from itertools import chain

W = 10 ; H = 19 ; SS = 30
shapes = {'#0DFF72': [(5, 0), (5, 1), (5, 2), (5, 3)], '#0EC2FF': [(4, 0), (5, 0), (4, 1), (5, 1)],
    '#3878FF': [(3, 0), (4, 0), (4, 1), (5, 1)], '#FFE138': [(4, 0), (5, 0), (3, 1), (4, 1)],
    '#F438FF': [(4, 0), (4, 1), (4, 2), (5, 2)], '#FF8E0C': [(4, 0), (4, 1), (3, 2), (4, 2)],
    '#FF0D73': [(3, 0), (4, 0), (5, 0), (4, 1)]}
references = {'#0DFF72': (4.5,1.5), '#0EC2FF': (4.5,0.5), '#3878FF': (4.5,0.5), '#FFE138': (4.5,.5),
    '#F438FF': (4.5, 1.5), '#FF8E0C': (4.5, 1.5), '#FF0D73': (4.5,0.5) }


class Tetris():
    def __init__(s):
        s.b = {(x,y): 'black' for y in range(H) for x in range(W)}
        s.coords = {loc:(loc[0]*SS+5,loc[1]*SS +5) for loc in s.b.keys()}
        s.squares = {loc:None for loc in s.b.keys()}
        s.current_color = None ; s.current_locs = None ; s.current_ref = None
        s.no_zone = [(x,y) for x in range(W) for y in range(4)] ; s.top = copy(H)
        s.score_text = c.create_text((W*SS+10)/2, H*SS+35, text=str(s.score), font='Helvetica 20')
        for loc in s.squares.keys():
            x, y = s.coords[loc]
            s.squares[loc] = c.create_rectangle(x,y,x+SS,y+SS, fill=s.b[loc], outline = '', width  = 5)

        s.score = 0   
        s.spawn()
        s.fall_constant()

    def spawn(s):
        s.current_color = random.choice(list(shapes.keys()))
        s.current_locs = shapes[s.current_color]
        s.current_ref = references[s.current_color]
        for loc in shapes[s.current_color]:
            s.b[loc] = s.current_color
        s.update(s.current_locs)

    def update(s, *locs):
        locs = set(chain(*locs)) if locs[0] else list(s.b.keys())
        for loc in locs:
            x, y = s.coords[loc]
            c.itemconfig(s.squares[loc], fill=s.b[loc])

    def turn(s, event):
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
        elif s.current_locs[0][0] > W-3:
            for x in range(2):
                new_locs = [(loc[0]-1,loc[1]) for loc in new_locs]
                if s.move(new_locs):
                    s.update(orig_locs,s.current_locs)
                    break

    def move(s, new_locs):
        for loc in new_locs:
            if not loc in s.b:
                return False
            if not s.b[loc] == 'black' and not loc in s.current_locs:
                return False  
        for loc in s.current_locs:
            s.b[loc] = 'black'
        for loc in new_locs:
            s.b[loc] = s.current_color
        
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
                
        root.after(250, s.fall_constant)

    def touching(s):
        for loc in s.current_locs:
            below = (loc[0],loc[1]+1)
            if not below in s.b:
                return True
            elif s.b[below] == 'black' and not below in s.current_locs:
                return True
        return False

    def fall_full(s,event):
        orig_locs = copy(s.current_locs)
        falling = True
        while falling:
            if s.move([(loc[0],loc[1]+1) for loc in s.current_locs]):
                s.score += 1
                c.delete(s.score_text)
                s.score_text = c.create_text((W*SS+10)/2, H*SS+35, text=str(s.score), font='Helvetica 20')
                s.current_ref = (s.current_ref[0], s.current_ref[1]+1)
            else:
                #what has been done in the previous movements
                s.update(orig_locs,s.current_locs)
                falling = False


        s.update(orig_locs)
        s.land_sequence()


    def land_sequence(s):
        for loc in s.current_locs:
            if loc[1] < s.top:
                s.top = int(loc[1])
        to_update = []
        #we don't know if this row is full yet, but most of the code only runs if it is so this name is less confusing then
        for full_row_num in range(s.top, H):
            row_colors = [s.b[(x, full_row_num)] for x in range(W)]
            if not 'black' in row_colors:
                row_locs = [(x, full_row_num) for x in range(W)]
                to_update.extend(row_locs)
                s.score += 10
                c.delete(s.score_text)
                s.score_text = c.create_text((W*SS+10)/2, H*SS+35, text=str(s.score), font='Helvetica 20')
                for loc in row_locs:
                    s.b[loc] = 'black'

                rows_to_move = [row_num for row_num in range(s.top, H) if row_num < full_row_num]
                to_move = [(x,y) for x in range(W) for y in rows_to_move]
                to_update.extend(to_move)

                for loc in reversed(to_move):
                    s.b[(loc[0],loc[1]+1)] = s.b[loc]
                    s.b[loc] = 'black'
    
                s.top += 1      
    
        s.update(to_update)
        
        if s.top < 4 :
            c.unbind_all('<Down>') 
            c.unbind_all('<Up>')
            c.unbind_all('<Left>') 
            c.unbind_all('<Right>')
            c.unbind_all('<space>')
        else:
            s.spawn()


root=Tk()
c = Canvas(root, width=W*SS+10, height=H*SS+60)
c.pack()
t = Tetris()

c.bind_all('<Down>', t.fall_full)
c.bind_all('<Up>', t.turn)
c.bind_all('<Left>', t.left)
c.bind_all('<Right>', t.right)
root.mainloop()
