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
	big_wordlist=[line.strip() for line in file.readlines()]

alphabet = [chr(i) for i in range(ord('a'), ord('z')+1)]

lookup = {'ccacc': 'plink', 'bcaca': 'leuch', 'ccaca': 'glitz', 'ccbcb': 'tepal', 'cbbcc': 'cloot', 'cbbbc': 'maron', 'ccbca': 'gault', 'cbbca': 'bundt', 'cbbac': 'abaca', 'bcbca': 'ampul', 'bcbcc': 'linty', 'ccbbc': 'riyal', 'ccbcc': 'clint', 'cbbaa': 'adore', 'ccbaa': 'afire', 'ccbbb': 'talar', 'ccbba': 'barca', 'ccaac': 'dhuti', 'ccbab': 'altho', 'bcacc': 'chals', 'ccbac': 'humic', 'cabbc': 'malty', 'bcbba': 'aalii', 'bbbba': 'arose', 'bbbbc': 'arson', 'bcbbc': 'abamp', 'bbbcc': 'aalii', 'bcbcb': 'ajwan', 'ccaaa': 'abaft', 'ccacb': 'letch', 'ccaab': 'lathy', 'bcacb': 'bufty', 'ccccb': 'teind', 'cccca': 'culti', 'cbccb': 'lento', 'cccbb': 'tined', 'cccab': 'delft', 'bcccb': 'teugh', 'ccccc': 'clint', 'cbccc': 'clint', 'cbcca': 'pling', 'cccbc': 'clint', 'bbccc': 'agloo', 'bcccc': 'mythi', 'cccac': 'fitch', 'caaac': 'board', 'baacc': 'abaca', 'caccc': 'culty', 'caccb': 'meynt', 'baccc': 'fubsy', 'cacca': 'pugil', 'cacba': 'faugh', 'cacbb': 'rewth', 'ccaba': 'diact', 'ccabc': 'clint', 'bcabc': 'bachs', 'cbabc': 'bravo', 'cccba': 'pudic', 'bccbc': 'cruft', 'cbcbc': 'cutin', 'cbcba': 'pownd', 'cbbcb': 'abcee', 'bbacc': 'chaos', 'cbcac': 'acidy', 'cbcaa': 'chore', 'bbcca': 'aitch', 'caacc': 'acyls', 'cabac': 'cobra', 'cabcc': 'liman', 'cacbc': 'cyton', 'bacca': 'pilum', 'cacac': 'almud', 'cbcbb': 'trued', 'bccbb': 'richt', 'bbcbc': 'acids', 'bccba': 'centu', 'bccca': 'cunit', 'bcaba': 'erase', 'bbccb': 'aahed', 'cccaa': 'abets', 'bacba': 'aargh', 'bacbb': 'loser', 'cbcab': 'abeam', 'baccb': 'nosey', 'cbbab': 'opera', 'cbaac': 'ovary', 'cbaca': 'ovate', 'cbacc': 'piano', 'bbcba': 'prose', 'ccabb': 'ached', 'caabc': 'roach', 'baabc': 'roast', 'bacbc': 'avows', 'acbcc': 'dault', 'acbbb': 'enmew', 'abbcc': 'ablow', 'acbca': 'ablet', 'acbbc': 'cuppy', 'abbbc': 'savor', 'acacc': 'thilk', 'acaca': 'thilk', 'acaaa': 'chapt', 'acaac': 'chapt', 'accca': 'pling', 'acccb': 'clipt', 'abccc': 'cloot', 'abcca': 'nempt', 'abcaa': 'chapt', 'abcac': 'nicht', 'abcbc': 'scour', 'accba': 'becap', 'accbb': 'unwet', 'accbc': 'bahut', 'acbcb': 'dempt', 'acccc': 'thilk', 'accaa': 'shire', 'accac': 'hault', 'aaacc': 'soapy', 'aacbb': 'sober', 'aaccc': 'atony', 'aabbc': 'solar', 'aacca': 'solve', 'aacac': 'sorry', 'accab': 'sperm', 'acabc': 'stair', 'bccac': 'usurp', 'bbcbb': 'verso'}

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
			result += log(len(s.possible_words)/n,2)*n  #/len(s.possible_words)
		return result
	def choose_second_guess(s):
		return lookup[s.get_result(s.game.word,'soare')]

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
			#score = sum(n**2 for n in results.values())
			score = s.get_guess_score(spread)
			if score > best_score or (score==best_score and guess in s.possible_words):
				best_score = score
				choice = guess
		
		return choice


'''word = 'twist'
assert word in wordlist'''

ai = AI()
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


# average: 3.5367012089810017
