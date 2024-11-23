# ai using monte carlo method
# can change simulations per direction and max moves per simulation

from copy import copy
from random import choice, randint
from tkinter import *

N=4 ; SS=80 ; PAD=5 ; TEXT_SIZE=15 # default 4 N and 50 SS and 8 PAD
simulations_per_direction = 15 ; max_moves_per_simulation = 50 # increase to be better, decrease to be faster

tk = Tk()
AX=15 ; AY=55 # dark grey bg anchors
c = Canvas(tk, width=2*AX+(N+1)*PAD+N*SS, height=AY+(N+1)*PAD+N*SS)
c.pack()

# dark grey bg and some text
rect = c.create_rectangle
text = c.create_text
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

directions = ['Up','Down','Left','Right']
# orters are functions for sorting keys by closeness to target wall
orders = {'Up': lambda loc: loc[1], 'Down': lambda loc: -loc[1],\
         'Left': lambda loc: loc[0], 'Right': lambda loc: -loc[0]} 
colors = {2: '#EEE4DA', 4: '#EDE0C8', 8: '#F2B179', 16: '#F59563',\
        32: '#F67C5F', 64: '#F65E3B', 128: '#EDCF72', 256: '#EDCC61',\
        512: '#EDC850', 1024: '#EDC53F', 2048: '#EDC22E',\
        4096: '#F4A63A', 8192: '#F57C5F', 16384: '#F75D5D'}

class Game:
    def __init__(s, b={loc:None for loc in coords.keys()}):
        s.live = True
        s.b = b
        s.c_items = []
        s.score = 0
        
    def new_block(s):
        value = 4 if randint(1,10)==1 else 2 # 90% chance will be a 2
        empty_locs = [loc for loc, val in s.b.items() if not val]
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
            fill = '#776E65' if val in (2,4) else '#F9F6F2'
            s.c_items.append(text(x+SS/2,y+SS/2, text=val, font=f'Helvetica {TEXT_SIZE} bold', fill=fill))

    def collapse(s,direction):
        order = sorted(s.b.keys(), key=orders[direction])
        alr_combined = []
        did_something = False

        for loc in order[N:]: # first N already on target wall
            full_locs = [loc for loc, val in s.b.items() if val]
            
            if loc in full_locs:
                current_loc = loc
                next_loc_i = order.index(current_loc) - N
                next_loc = order[next_loc_i]

                while next_loc_i > -1:
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
                                del alr_combined[current_loc] # alr combined block no longer in that loc
                            alr_combined.append(next_loc)   
                
                    # come back and add comments here
                    current_loc = order[order.index(current_loc) - N]
                    next_loc_i = order.index(current_loc) - N
                    next_loc = order[order.index(current_loc) - N]
        
        if did_something:
            s.new_block()
            if not s.get_possible_direcs():
                s.live = False

    # ai generated at first but ai did it wrong so i fixed it
    def get_possible_direcs(s):
        direcs = set()
        for coli in range(N):
            for rowi in range(N):
                if s.b[(coli,rowi)] is None:
                    if coli>0 and s.b[(coli-1, rowi)] is not None: direcs.add('Right')
                    if coli < N-1 and s.b[(coli+1, rowi)] is not None: direcs.add('Left')
                    if rowi>0 and s.b[(coli, rowi-1)] is not None: direcs.add('Down')
                    if rowi < N-1 and s.b[(coli, rowi+1)] is not None: direcs.add('Up')
                else:
                    if coli>0 and s.b[(coli, rowi)] == s.b[(coli-1, rowi)]: direcs.add('Left')
                    if coli < N-1 and s.b[(coli, rowi)] == s.b[(coli+1, rowi)]: direcs.add('Right')
                    if rowi>0 and s.b[(coli,rowi)] == s.b[(coli, rowi-1)]: direcs.add('Up')
                    if rowi < N-1 and s.b[(coli, rowi)] == s.b[(coli, rowi+1)]: direcs.add('Down')
        return direcs


class AI:
    def __init__(s):
        s.game = Game()
        for _ in range(2):
            s.game.new_block()

             
    def run_simulation(s, direction):
        simulation = Game(copy(s.game.b))
        simulation.collapse(direction)
        moves = 0
        while simulation.live and moves <= max_moves_per_simulation:
            simulation.collapse(choice(directions))
            moves += 1
        return simulation.score
    
    def get_best_move(s):
        possible_direcs = {direc: 0 for direc in s.game.get_possible_direcs()}
        for direc in possible_direcs:
            for _ in range(simulations_per_direction):
                possible_direcs[direc] += s.run_simulation(direc)

        return max(possible_direcs.items(), key=lambda item:item[1])[0]

ai = AI()
while ai.game.live:
    ai.game.collapse(ai.get_best_move())
    ai.game.draw_board()
    tk.update()

mainloop()