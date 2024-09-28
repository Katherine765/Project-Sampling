# s stands for self, b stands for board, c stands for canvas

from copy import copy
from random import choice, randint
from tkinter import *

# dark grey bg anchors
AX = 15
AY = 55

SS = 70 #default 50 square size
PAD = 5 #default 8 between squares

W = 2*AX + 5*PAD + 4*SS
H = AY + 5*PAD + 4*SS

tk = Tk()
c = Canvas(tk, width=W, height=H)
c.pack()

# shorthand
rect = c.create_rectangle
text = c.create_text

# dark grey bg and some text
rect(AX, AY, AX+4*SS+5*PAD, AY+4*SS+5*PAD, fill='#BBAFA0', outline='')
text(50, 30, text='2048', font=('Helvetica', 25, 'bold'), fill='#776E65')
text(135, 15, text='Score', font=('Helvetica', 10, 'bold'), fill='#776E65')

# creates light grey squares and coords list
coords = []
y = AY+PAD
for row in range(4):
    x = AX+PAD
    for column in range(4):
        rect(x, y, x+SS, y+SS, fill='#CDC1B4', outline='')
        coords.append((x, y))
        x += SS+PAD
    y += SS+PAD


# order to collapse the squares in, so closer to target wall first
orders = {'Up':list(range(16)),'Down':list(range(15, -1, -1)), \
          'Left':(0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15), \
          'Right': (3, 7, 11, 15, 2, 6, 10, 14, 1, 5, 9, 13, 0, 4, 8, 12)}

directions = ['up','down','left','right']

# same as actual game
colors = {2: '#EEE4DA', 4: '#EDE0C8', 8: '#F2B179', 16: '#F59563',\
        32: '#F67C5F', 64: '#F65E3B', 128: '#EDCF72', 256: '#EDCC61',\
        512: '#EDC850', 1024: '#EDC53F', 2048: '#EDC22E',\
        4096: '#F4A63A', 8192: '#F57C5F', 16384: '#F75D5D'}


class Game:
    def __init__(s):
        s.b = [None for x in range(16)]
        s.c_items = []
        s.score = 0
        for i in range(2): # start w/ two blocks
            s.new_block()
        s.draw_board()
        
    def new_block(s):
        value = 4 if randint(1,10)==1 else 2 # 90% chance will be a 2
        empty_indexes = [blockID for blockID, val in enumerate(s.b) if val is None]
        s.b[choice(empty_indexes)] = value

    def draw_board(s):
        for ID in s.c_items:
            c.delete(ID)

        # update score
        s.c_items.append(text(135, 30, text=s.score, font=('Helvetica', 10, 'bold'), fill='#776E65'))

        # redraw all blocks
        for i in range(16):
            value = s.b[i]
            if value:
                x = coords[i][0]
                y = coords[i][1]
                s.c_items.append(rect(x, y, x + SS, y + SS, fill=colors[value], outline=''))
                s.c_items.append(text(x + SS/2, y + SS/2, text=value, \
                                                         font=('Helvetica', 18 if value<1000 else 13, 'bold'), \
                                                         fill='#776E65' if value in (2,4) else '#F9F6F2'))

    def collapse(s,event):
        order = orders[event.keysym]
        alr_combined = []
        did_something = False

        # ids are spot numbers from 1-16 from left to right then top to bottom
        for blockID in order[4:16]: #first 4 are already on target wall so won't move
            full_indexes = [i for i, blockID in enumerate(s.b) if not blockID is None]
            
            if blockID in full_indexes:
                currentID = blockID
                nextID_i = order.index(currentID) - 4 # closer to the target wall
                nextID = order[nextID_i]

                #next gets out of range first bc it is moving
                while -1 < nextID_i :

                    #move into empty spot
                    if s.b[nextID] is None:
                        did_something = True
                        s.b[nextID] = s.b[currentID]
                        s.b[currentID] = None

                    #combine forward
                    elif s.b[nextID] == s.b[currentID]:
                        did_someting = True
                        if not currentID in alr_combined and not nextID in alr_combined:
                            s.b[nextID] *= 2 # value doubles bc combined
                            s.score += s.b[nextID]
                            s.b[currentID] = None
                            if currentID in alr_combined:
                                del alr_combined[currentID] # the block that was already combined is no longer in that spot
                            alr_combined.append(nextID)   

                    currentID = order[order.index(currentID) - 4] # farther from target wall
                    nextID_i = order.index(currentID) - 4  
                    nextID = order[nextID_i] # one closer to the target wall 

        if did_something:
            s.new_block()
            s.draw_board()
            tk.update()
             
game = Game()
c.bind_all('<KeyPress>', game.collapse)
tk.mainloop()
