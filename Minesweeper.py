#ez 10x8 w/ 10m, med 18x14 w/ 40m, hard 24x20 w/ 99m

import random as r
from tkinter import *
from copy import copy
from time import sleep, time

W = 10 ; H = 8 ; SS = 30
NUM_MINES = 10

class Game:
    def __init__(s):
        s.live = True
        s.started = False
        s.start_time = None
        s.locs = [(coli,rowi) for coli in range(W) for rowi in range(H)]
        s.mine_locs = []
        s.numbers = {}
        s.flags = {}
        s.screen = {}

        for coli, rowi in s.locs:
            x = coli*SS ; y = rowi*SS
            color = '#C8D8E4' if bool(coli%2==0) == bool(rowi%2==0) else '#A9BBCB'
            c.create_rectangle(x,y,x+SS,y+SS, fill=color, outline='')
    
    def get_loc(s,x,y):
        return x//SS,y//SS
    
    def get_touching_locs(s,loc):
        coli, rowi = loc
        offsets = [-1, 0, 1]
        touching_locs = [(coli+i, rowi+j) for i in offsets for j in offsets if (coli+i, rowi+j) in s.locs]
        touching_locs.remove((coli,rowi))
        return touching_locs
    
    def count_touching_mines(s,loc):
        return sum(1 for loc in s.get_touching_locs(loc) if loc in s.mine_locs)
    
    def set_up(s,click_loc):
        mine_loc_options = [loc for loc in s.locs if not loc in (*s.get_touching_locs(click_loc),click_loc)] 
        s.mine_locs = r.sample(mine_loc_options, NUM_MINES)
        s.started = True
        s.start_time = time()

    def click(s,e):
        loc = s.get_loc(e.x,e.y)
        if not loc in s.locs:
            return
        if loc in s.numbers:
            return
        if loc in s.mine_locs:
            s.explode_mines(loc)
            return
        
        if not s.started:
            s.set_up(loc)

        x = loc[0]*SS + SS/2
        y = loc[1]*SS + SS/2
        num_touching_mines = s.count_touching_mines(loc)
        s.numbers[loc]=c.create_text(x, y, text=num_touching_mines, font = f'Helvetica {int(SS/2)}')
        s.screen[loc] = num_touching_mines
        if num_touching_mines == 0:
            s.expand(s.get_touching_locs(loc))
        s.check_for_win()
    
    def expand(s, to_do):
        new_to_do = set()
        for loc in to_do:
            x = loc[0]*SS + SS/2
            y = loc[1]*SS + SS/2
            num_touching_mines = s.count_touching_mines(loc)
            s.numbers[loc]=c.create_text(x, y, text=num_touching_mines, font = f'Helvetica {SS//2}')
            s.screen[loc] = num_touching_mines
            if num_touching_mines == 0:
                new_to_do.update(s.get_touching_locs(loc))
        new_to_do = {loc for loc in new_to_do if loc in s.locs and not loc in s.numbers}
        if new_to_do:
            s.expand(new_to_do)

    def flag(s,e):
        loc = s.get_loc(e.x,e.y)
        if loc in s.flags:
            c.delete(s.flags[loc])
            del s.flags[loc]
            del s.screen[loc]
        else:
            x=loc[0]*SS ; y=loc[1]*SS
            s.flags[loc]=c.create_rectangle(x,y,x+SS,y+SS,fill='#FF6B6B',outline='')
            s.screen[loc] = 'flag'

    
    def check_for_win(s):
        if len(s.numbers) == W*H-NUM_MINES:
            s.live = False
            total_time = round(time() - s.start_time, 4)
            c.create_text((W*SS+10)/2, H*SS+35, text=f'Winner!    {total_time}s', font = 'Helvetica 20')


    def explode_mines(s,bad_click_loc):
        s.live = False
        # clicked mine will explode first
        s.mine_locs.remove(bad_click_loc)
        s.mine_locs.insert(0,bad_click_loc)
        for loc in s.mine_locs:
            x = loc[0]*SS ; y=loc[1]*SS
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
