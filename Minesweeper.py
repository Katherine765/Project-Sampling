#ez 10x8 w/ 10m, med 18x14 w/ 40m, hard 24x20 w/ 99m
#if you click the same thing a bunch of times, it will count them as new opens

#Imports
import random as r
from tkinter import *
from copy import copy
from time import sleep, time

W = 10 ; H = 8 ; SS = 40
NUM_MINES = 10

class Game:
    def __init__(s):
        s.started = False
        s.start_time = None
        s.b = {(coli,rowi): None for coli in range(W) for rowi in range(H)} # stores 'm' for mines and # mines touching otherwise, bad naming but im not fixing that
        s.mine_locs = None
        s.clicked = copy(s.b)
        s.flagged = copy(s.b)

        s.coords={}
        for coli, rowi in s.b.keys():
            x = coli*SS ; y = rowi*SS
            s.coords[(coli,rowi)] = (x,y)
            color = '#C8D8E4' if bool(coli%2==0) == bool(rowi%2==0) else '#A9BBCB'
            c.create_rectangle(x,y,x+SS,y+SS, fill=color, outline='')

    def get_loc(s,x,y):
        return (x)//SS,(y)//SS
    
    def get_touching_locs(s,loc):
        coli = loc[0] ; rowi = loc[1]
        offsets = [-1, 0, 1]
        touching_locs = [(coli + i, rowi + j) for i in offsets for j in offsets if (coli+i, rowi+j) in s.b.keys()]
        touching_locs.remove((coli,rowi))
        return touching_locs
    
    def set_up_board(s,e):
        click_loc = s.get_loc(e.x, e.y)
        placement_options = [loc for loc in s.b if not loc in s.get_touching_locs(click_loc)]
        s.mine_locs = r.sample(placement_options, NUM_MINES)
        for loc in s.mine_locs:
            s.b[loc] = 'm'
        for loc in s.b:
            if not loc in s.mine_locs:
                touching_vals = [s.b[loc2] for loc2 in s.get_touching_locs(loc)]
                s.b[loc] = touching_vals.count('m')

        s.click(e)
    
    #Runs when a left click occurs, runs the start sequence if it is the first valid click
    def click(s,e):
        if not s.started:
            if s.get_loc(e.x, e.y) in s.b:
                s.started = True
                s.start_time = time()
                s.set_up_board(e)
            return
        
        loc = s.get_loc(e.x,e.y)
        if loc in s.b:
            if s.b[loc] == 'm':
                s.explode_mines(loc)
                return
            x = s.coords[loc][0] + SS/2
            y = s.coords[loc][1] + SS/2
            if not s.clicked[loc]:
                s.clicked[loc]=c.create_text(x, y, text=s.b[loc], font = f'Helvetica {int(SS/2)}')
            if s.b[loc] == 0:
                s.expand(s.get_touching_locs(loc))

            s.check_for_win()
    
    def expand(s, to_do):
        new_to_do = set()
        for loc in to_do:
            x = s.coords[loc][0] + SS/2
            y = s.coords[loc][1] + SS/2
            s.clicked[loc]=c.create_text(x, y, text=s.b[loc], font = f'Helvetica {int(SS/2)}')
            if s.b[loc] == 0:
                new_to_do.update(s.get_touching_locs(loc))
        new_to_do = {loc for loc in new_to_do if not s.clicked[loc]}
        if new_to_do:
            s.expand(new_to_do)

    def flag(s,e):
        loc = s.get_loc(e.x,e.y)
        coord = s.coords[loc]
        x = coord[0] ; y = coord[1]
        if s.flagged[loc]:
            c.delete(s.flagged[loc])
            s.flagged[loc] = None
        else:
            s.flagged[loc]=c.create_rectangle(x,y,x+SS,y+SS,fill='#FF6B6B',outline='')

    
    def check_for_win(s):
        opened = sum(1 for item in s.clicked.values() if item)
        if opened == W*H-NUM_MINES:
            total_time = round(time() - s.start_time)
            c.unbind_all('<Button-1>')
            c.unbind_all('<Button-3>')
            c.create_text((W*SS+10)/2, H*SS+35, text=f'Winner!    {total_time}s', font = 'Helvetica 20')


    def explode_mines(s,bad_click_loc):
        c.unbind_all('<Button-1>') 
        c.unbind_all('<Button-3>') 
        
        # clicked mine will explode first
        s.mine_locs.remove(bad_click_loc)
        s.mine_locs.insert(0,bad_click_loc)
        for coli,rowi in s.mine_locs:
            x = coli*SS ; y=rowi*SS
            c.create_rectangle(x,y,x+SS,y+SS,fill='#80718C',outline='')
            tk.update()
            sleep(.25)

tk=Tk()
c = Canvas(tk, width=W*SS, height=H*SS+60)
c.pack()

g = Game()
c.bind_all('<Button-1>', g.click)
c.bind_all('<Button-3>', g.flag)

tk.mainloop()
