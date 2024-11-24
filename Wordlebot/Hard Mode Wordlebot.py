from copy import copy
from random import choice

with open('wordle_words1.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]
alphabet = [chr(i) for i in range(ord('a'), ord('z')+1)]


class Game():
	def __init__(s):
		s.live = True
		s.word = choice(wordlist)
		s.grays = []
		s.yellow_list = []
		s.yellow_dict={x:[] for x in range(5)}
		s.greens=[None for _ in range(5)]
		s.tries = 0

	def submit_guess(s, guess):
		s.tries += 1
		if s.word == guess:
			s.live = False
			return True
		for i, letter in enumerate(list(guess)):
			if letter == s.word[i]:
				s.greens[i]=letter
			elif letter in s.word:
				s.yellow_list.append(letter)
				s.yellow_dict[i].append(letter)
			else:
				s.grays.append(letter)

class AI:
	def __init__(s):
		s.game = Game()
		s.valid_guesses = copy(wordlist)
		s.frequency = {}
		s.placement = {}
		
		
	def get_validity(s, guess):
		letters=list(guess)
		for i, letter in enumerate(letters):
			if letter in s.game.grays:
				return False
			if letter in s.game.yellow_dict[i]:
				return False
			if s.game.greens[i] and not letter==s.game.greens[i]:
				return False
		for letter in s.game.yellow_list:
			if not letter in letters:
				return False
		return True
	
	def update_data(s):
		s.valid_guesses = [guess for guess in s.valid_guesses if s.get_validity(guess)]
		s.frequency= {letter: 0 for letter in alphabet}
		s.placement={letter:[0 for _ in range(5)] for letter in alphabet}
		for guess in s.valid_guesses:
			for i, letter in enumerate(list(guess)):
				# Frequency counted once per word
				if guess.find(letter) == i:
					s.frequency[letter] += 1
				s.placement[letter][i] += 1
				
	def choose_guess(s):
		s.update_data()
		choice = None
		best_score = 0
		for guess in s.valid_guesses:
			score = 0
			for i, letter in enumerate(list(guess)):
				if i == guess.find(letter):    
					score += s.frequency[letter]
				score += .55*s.placement[letter][i]
			if score > best_score:
				best_score = score
				choice = guess
		return choice

ai = AI()
while ai.game.live:
	guess = ai.choose_guess()
	print(guess)
	ai.game.submit_guess(guess)

print(f'Win in {ai.game.tries} tries!')
