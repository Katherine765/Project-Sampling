from random import choice
from tkinter import *
from time import sleep

with open('wordle_words1.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]
with open('wordle_words2.txt', 'r') as file:
	big_wordlist=[line.strip() for line in file.readlines()]
	
W = 65 ; H = 75 ; PAD = 10
fills = {'a':'#6aaa64', 'b':'#c9b458','c':'#787c7e'}

class Game():
	def __init__(s, word = choice(wordlist)):
		s.live = True
		s.word = word
		s.grays = []
		s.yellow_list = []
		s.yellow_dict={x:[] for x in range(5)}
		s.greens=[None for _ in range(5)]
		s.tries = 0
		
		s.cued = ''
		s.cued_canvas = []

	def submit_guess(s, guess):
		s.tries += 1
		if s.word == guess:
			s.live = False
			c.unbind_all('<KeyPress>')
			return 'aaaaa'
		result = ''
		for i, letter in enumerate(list(guess)):
			if letter == s.word[i]:
				s.greens[i]=letter
				result += 'a'
			elif letter in s.word:
				s.yellow_list.append(letter)
				s.yellow_dict[i].append(letter)
				result += 'b'
			else:
				s.grays.append(letter)
				result += 'c'
		return result
				

	def keypress(s, e):
		if e.keysym == 'Return' and s.cued in wordlist:
			result = s.submit_guess(s.cued)
			for c_item in s.cued_canvas:
				del c_item
			y = PAD + (s.tries-1)*(PAD+H)
			for i, letter in enumerate(s.cued):
				x = PAD + i*(PAD+W)
				c.create_rectangle(x,y,x+W,y+H, fill=fills[result[i]], outline='white') #white outline to cover old outline
				c.create_text(x+W/2,y+H/2, text=letter.upper(), font = 'Helvetica 30 bold', fill='white')
				tk.update()
				sleep(.22)
			s.cued = ''
			return
		elif e.keysym == 'BackSpace' and s.cued:
			s.cued = s.cued[:-1]
			c.delete(s.cued_canvas[-1]) # dark ring
			del s.cued_canvas[-1]
			c.delete(s.cued_canvas[-1]) # dark letter
			del s.cued_canvas[-1]
		elif e.char.isalpha() and len(s.cued) < 5:
			s.cued += e.char
			x = PAD + (len(s.cued)-1)*(PAD+W)
			y = PAD + s.tries*(PAD+H)
			s.cued_canvas.append(c.create_text(x+W/2,y+H/2, text=e.char.upper(), font = 'Helvetica 30 bold', fill = 'black'))
			s.cued_canvas.append(c.create_rectangle(x,y,x+W,y+H,fill='',outline='#787c7e'))
		
tk=Tk()
c=Canvas(tk, width=W*5+PAD*6, height=H*6+PAD*7)
tk.configure(bg='white')
c.pack()

for x in range(PAD, 5*(W+PAD), W+PAD):
	for y in range(PAD, 6*(H+PAD), H+PAD):
		c.create_rectangle(x,y,x+W,y+H, fill='',outline='#D3D6DA')
		
game = Game()
c.bind_all('<KeyPress>', game.keypress)		
tk.mainloop()
		
