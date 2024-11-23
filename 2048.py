from copy import copy
from random import choice, randint
from tkinter import *

AX=15 ; AY=55 # dark grey bg anchors
N=5 ; SS=50 ; PAD=5 # default 50 SS and 8 PAD # N for board being nxn grid (default 4)

tk = Tk()
c = Canvas(tk, width=2*AX+(N+1)*PAD+N*SS, height=AY+(N+1)*PAD+N*SS)
c.pack()
rect = c.create_rectangle ; text = c.create_text # shorthand

# dark grey bg and some text
rect(AX, AY, AX+N*SS+(N+1)*PAD, AY+N*SS+(N+1)*PAD, fill='#BBAFA0', outline='')
text(50, 30, text='2048', font=('Helvetica 25 bold'), fill='#776E65')
text(135, 15, text='Score', font=('Helvetica 10 bold'), fill='#776E65')

# light gray squares and coords list
coords = {(coli,rowi):None for coli in range(N) for rowi in range(N)}
y = AY+PAD
for rowi in range(N):
    x = AX+PAD
    for coli in range(N):
        rect(x, y, x+SS, y+SS, fill='#CDC1B4', outline='')
        coords[coli,rowi] = (x,y)
        x += SS+PAD
    y += SS+PAD

orders = {'Up': lambda loc: loc[1], 'Down': lambda loc: -loc[1],\
         'Left': lambda loc: loc[0], 'Right': lambda loc: -loc[0]} # sort key for by closeness to target wall
colors = {2: '#EEE4DA', 4: '#EDE0C8', 8: '#F2B179', 16: '#F59563',\
        32: '#F67C5F', 64: '#F65E3B', 128: '#EDCF72', 256: '#EDCC61',\
        512: '#EDC850', 1024: '#EDC53F', 2048: '#EDC22E',\
        4096: '#F4A63A', 8192: '#F57C5F', 16384: '#F75D5D'}

class Game:
    def __init__(s):
        s.b = {loc:None for loc in coords.keys()}
        s.c_items = []
        s.score = 0
        for i in range(2): # start w/ two blocks
            s.new_block()
        s.draw_board()
        
    def new_block(s):
        value = 4 if randint(1,10)==1 else 2 # 90% chance will be a 2
        empty_locs = [loc for loc in s.b.keys() if not s.b[loc]]
        s.b[choice(empty_locs)] = value

    def draw_board(s):
        for c_item in s.c_items:
            c.delete(c_item)
        s.c_items.append(text(135, 30, text=s.score, font=('Helvetica 10 bold'), fill='#776E65'))
        for loc, val in s.b.items():
            if not val:
                continue
            x, y = coords[loc]
            s.c_items.append(rect(x,y,x+SS,y+SS, fill=colors[val], outline=''))
            font = 'Helvetica 18 bold' if val<1000 else 'Helvetica 13 bold'
            fill = '#776E65' if val in (2,4) else '#F9F6F2'
            s.c_items.append(text(x+SS/2,y+SS/2, text=val, font=font, fill=fill))

    def collapse(s,e):
        direction = e.keysym
        order = sorted(s.b.keys(), key=orders[direction])
        alr_combined = []
        did_something = False

        for loc in order[N:]: # first few are already on target wall so won't move
            full_locs = [loc for loc, val in s.b.items() if val]
            
            if loc in full_locs:
                current_loc = loc
                next_loc_i = order.index(current_loc) - N
                next_loc = order[next_loc_i]

                while next_loc_i > -1: # would just check if next_loc is in s.b.keys() but the next loc is from order and takes negative index
                    #move into empty spot
                    if s.b[next_loc] is None:
                        did_something = True
                        s.b[next_loc] = copy(s.b[current_loc])
                        s.b[current_loc] = None
                    #combine forward
                    elif s.b[current_loc] == s.b[next_loc]:
                        if not current_loc in alr_combined and not next_loc in alr_combined:
                            did_something = True
                            s.b[next_loc] *= 2
                            s.score += s.b[next_loc]
                            s.b[current_loc] = None
                            if current_loc in alr_combined:
                                del alr_combined[current_loc] # alr combined block no longer in that spot
                            alr_combined.append(next_loc)   
                
                    # come back and double check these comments
                    current_loc = order[order.index(current_loc) - N] # farther from target wall
                    next_loc_i = order.index(current_loc) - N
                    next_loc = order[order.index(current_loc) - N] # one closer to the target wall 

        if did_something:
            s.new_block()
            s.draw_board()
            tk.update()
             
game = Game()
c.bind_all('<KeyPress>', game.collapse)
tk.mainloop()
