import random
import time
from tkinter import *

with open('words.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]

# i don't feel like making these capital
width = 700
height = 500

class Game():
    def __init__(s, root, canvas, width, height):
        s.score = 0
        s.width = width ; s.height = height
        s.root = root
        s.time_between = 750 #in milliseconds                                          #CHANGEABLE NUMBER
        s.current_words = []
        s.record = ''
        s.live = True
        
        s.new_dropper()
        s.update()

    def add_input(s, event):
        s.record += event.char

    def generate_color(s):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        # Make sure it is bright enough
        brightness = (red + green + blue) / 3
        if brightness < 128:
            red = min(255, red + 128)
            green = min(255, green + 128)
            blue = min(255, blue + 128)

        hex_color = "#{:02x}{:02x}{:02x}".format(red, green, blue)
        return hex_color

        
    def new_dropper(s):
        if s.live:
            s.time_between -= 5                                                                           #CHANGEABLE NUMBER
            
            new_word = random.choice(wordlist)
            x = random.randint(50, s.width-50)
            color = s.generate_color()
            speed = random.randint(1,5) #in pixels dropped per update
            size = random.randint(15,30)
            canvas_item = canvas.create_text(x,0,text=new_word, font = f'Helvetica {size}', fill = color)
            # list of lists in form (canvas item, word speed, current y)
            s.current_words.append([x, 0, speed, new_word, size, color, canvas_item])

            s.root.after(s.time_between, s.new_dropper)


    def update(s):
        if s.live:
            to_delete = []
            for item in s.current_words:
                s.record = s.record[-20:]
                if item[3] in s.record:
                    s.score += 1
                    to_delete.append(item)
                    continue
                #deletes the old canvas item
                canvas.delete(item[-1])
                # changes the y pos based on the speed
                item[1] += item[2]
                if item[1] > s.height:
                    s.game_over()
                # creates the new canvas item and replaces the old one in the list
                item[-1] = canvas.create_text(item[0], item[1], text = item[3], font = f'Helvetica {item[4]}', fill = item[5])


            for item in to_delete:
                canvas.delete(item[-1])
                s.current_words.remove(item)

        
            s.root.after(45, s.update)                                                     #CHANGEABLE NUMBER


    def pause(s,event):
        if s.live:
            s.live = False
        else:
            s.live = True
            s.new_dropper()
            s.update()

    def game_over(s):
        s.live = False
        canvas.unbind_all('<KeyPress>')
        canvas.unbind_all('1')
        print(s.score)
        


root=Tk()
canvas = Canvas(root, width=width, height=height, bg='black')
canvas.pack()
game = Game(root, canvas, width, height)

canvas.bind_all('<KeyPress>', game.add_input)
canvas.bind_all('1', game.pause)
