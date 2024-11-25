# i plan on connecting this to my wordle graphics soon
# it chooses "soare" first, so i hard-coded that so it doesn't have to think every time
# the lookup table for the second guess is faster than thinking

from collections import defaultdict
from copy import copy
from math import log
import numpy as np
from random import choice, shuffle

with open('wordle_words1.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]
with open('wordle_words2.txt', 'r') as file:
	big_wordlist=set([line.strip() for line in file.readlines()])
	big_wordlist.update(wordlist)

alphabet = [chr(i) for i in range(ord('a'), ord('z')+1)]

lookup = {'ccacc': 'clink', 'bcaca': 'butch', 'ccaca': 'glitz', 'ccbcb': 'tepal', 'cbbcc': 'cloot', 'cbbbc': 'maron', 'ccbca': 'gault', 'cbbca': 'bundt', 'cbbac': 'antic', 'bcbca': 'thump', 'bcbcc': 'linty', 'ccbbc': 'riyal', 'ccbcc': 'clint', 'cbbaa': 'adore', 'ccbaa': 'afire', 'ccbbb': 'talar', 'ccbba': 'carbs', 'ccaac': 'dhuti', 'ccbab': 'letup', 'bcacc': 'chums', 'ccbac': 'mitch', 'cabbc': 'malty', 'bcbba': 'arise', 'bbbba': 'arose', 'bbbbc': 'arson', 'bcbbc': 'marsh', 'bbbcc': 'ascot', 'bcbcb': 'oaten', 'ccaaa': 'befog', 'ccacb': 'depth', 'ccaab': 'lathy', 'bcacb': 'fatly', 'ccccb': 'teind', 'cccca': 'guilt', 'cbccb': 'lento', 'cccbb': 'tined', 'cccab': 'delft', 'bcccb': 'uneth', 'ccccc': 'clint', 'cbccc': 'clint', 'cbcca': 'pling', 'cccbc': 'glint', 'bbccc': 'biogs', 'bcccc': 'mythi', 'cccac': 'tichy', 'caaac': 'board', 'baacc': 'bancs', 'caccc': 'culty', 'caccb': 'meynt', 'baccc': 'fubsy', 'cacca': 'guild', 'cacba': 'gouch', 'cacbb': 'rewth', 'ccaba': 'ditch', 'ccabc': 'clint', 'bcabc': 'chibs', 'cbabc': 'bravo', 'cccba': 'pudic', 'bccbc': 'cruft', 'cbcbc': 'cutin', 'cbcba': 'pwned', 'cbbcb': 'omega', 'bbacc': 'chaos', 'cbcac': 'cited', 'cbcaa': 'chore', 'bbcca': 'mitch', 'caacc': 'loath', 'cabac': 'cobra', 'cabcc': 'liman', 'cacbc': 'cyton', 'bacca': 'pilum', 'cacac': 'adult', 'cbcbb': 'trued', 'bccbb': 'richt', 'bbcbc': 'cited', 'bccba': 'punty', 'bccca': 'inust', 'bcaba': 'erase', 'bbccb': 'onset', 'cccaa': 'inust', 'bacba': 'worse', 'bacbb': 'loser', 'cbcab': 'retro', 'baccb': 'nosey', 'cbbab': 'opera', 'cbaac': 'ovary', 'cbaca': 'ovate', 'cbacc': 'piano', 'bbcba': 'prose', 'ccabb': 'mitch', 'caabc': 'roach', 'baabc': 'roast', 'bacbc': 'worst', 'acbcc': 'dault', 'acbbb': 'women', 'abbcc': 'salvo', 'acbca': 'sauce', 'acbbc': 'cuppy', 'abbbc': 'savor', 'acacc': 'thilk', 'acaca': 'thilk', 'acaaa': 'pinch', 'acaac': 'kotch', 'accca': 'pling', 'acccb': 'clipt', 'abccc': 'cloot', 'abcca': 'knelt', 'abcaa': 'pinch', 'abcac': 'nicht', 'abcbc': 'scour', 'accba': 'vaped', 'accbb': 'unwit', 'accbc': 'butch', 'acbcb': 'knelt', 'acccc': 'thilk', 'accaa': 'shire', 'accac': 'thilk', 'aaacc': 'soapy', 'aacbb': 'sober', 'aaccc': 'myoid', 'aabbc': 'solar', 'aacca': 'solve', 'aacac': 'sorry', 'accab': 'sperm', 'acabc': 'stair', 'bccac': 'usurp', 'bbcbb': 'verso'}


class Game():
	def __init__(s, word = choice(wordlist)):
		s.live = True
		s.word = word
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
	def __init__(s, word=choice(wordlist)):
		s.game = Game(word)
		s.possible_words = copy(wordlist)

	def get_possibleness(s, guess):
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
	
	def get_result(s,word,guess):
		result = ''
		for i, letter in enumerate(list(guess)):
			if letter == word[i]:
				result += 'a'
			elif letter in word:
				result += 'b'
			else:
				result += 'c'
		return result
	
	def get_guess_score(s, spread):
		result = 0
		for n in spread.values():
			result += log(len(s.possible_words)/n,2)*n  #/len(s.possible_words) not necessary, also just adding n^2 instead works pretty well
		return result
	def choose_second_guess(s):
		result = s.get_result(s.game.word,'soare')
		return lookup[result]

	def choose_guess(s):
		s.possible_words = [word for word in s.possible_words if s.get_possibleness(word)]
		if len(s.possible_words) < 3:
			return s.possible_words[0]
		best_score = 0
		choice = None
		for guess in big_wordlist:
			spread = copy(defaultdict(int))
			for word in s.possible_words:
				spread[s.get_result(word,guess)] += 1
			score = s.get_guess_score(spread)
			if score > best_score or (score==best_score and guess in s.possible_words):
				best_score = score
				choice = guess
		
		return choice


ai = AI('brown') # change word here, or leave blank for random
print('soare')
ai.game.submit_guess('soare')
guess = ai.choose_second_guess()
print(guess)
ai.game.submit_guess(ai.choose_second_guess())
while ai.game.live:
	guess = ai.choose_guess()
	print(guess)
	ai.game.submit_guess(guess)
print(f'Win in {ai.game.tries} tries!')

# average: 3.47279792746114
