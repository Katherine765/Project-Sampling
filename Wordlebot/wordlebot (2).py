with open('wordle_words1.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]


class Game():
	def __init__(self):
		self.frequency, self.placement = {}, {}
		self.wrong, self.somewhere = [], []
		self.know=[None for x in range(5)]
		self.yellow={x:[] for x in range(5)}
		self.tries=0
		self.topChoice=None

	def checkValidity(self, potential_guess):
		guess_list=list(potential_guess)

		for x, letter in enumerate(guess_list):
			#No grays in word
			if letter in self.wrong:
				return False
			#No unmoved yellow
			if letter in self.yellow[x]:
				return False

		for x, letter in enumerate(self.somewhere):
        	#All yellows in word
			if not letter in guess_list:
				return False

		for x, letter in enumerate(self.know):
       		#All greens in word
			if not letter is None and not letter==guess_list[x]:
				return False

		return True


	def generateData(self, possible):
		self.frequency=[0 for x in range(26)]
		self.placement=[[0 for x in range(5)] for x in range(26)]
		for possible_guess in possible:
			guess_list=list(possible_guess)
			for x in range(5):
				letterNum=ord(possible_guess[x])-97
				# Frequency counted once per word
				if x == possible_guess.find(guess_list[x]):
					self.frequency[letterNum] += 1
				self.placement[letterNum][x] += 1


	def chooseBest(self, possible):
		topRank=0
		for possible_guess in possible:
			rank=0
			guess_list=list(possible_guess)

			for x, letter in enumerate(guess_list):
				letterToNumber=ord(letter)-97
				# Can only get frequency points once per letter per word
				if x == possible_guess.find(letter):    
					rank += self.frequency[letterToNumber]
				rank += .55*self.placement[letterToNumber][x] # the .55 is experimentally determined
			# switch this sign to be bad at wordle (would also have to make rank start bigger)
			if rank>topRank:
				topRank=rank
				self.topChoice=possible_guess
		
		self.tries += 1

	def actualCheck(self, word):
		if word == self.topChoice:
			return True

		guess_list=list(self.topChoice)
		for x, letter in enumerate(guess_list):
			#Green  
			if letter == word[x]:
				self.know[x]=letter
			#Yellow
			elif letter in word:
				self.somewhere.append(letter)
				self.yellow[x].append(letter)
			#Grey
			else:
				self.wrong.append(letter)


def main(word):
	if not word in wordlist:
		print('Word not in wordlist.')
		return

	game=Game()
	possible=wordlist
	while True:
		old_possible = possible
		possible=[]
		for potential_guess in old_possible:
			if game.checkValidity(potential_guess):
				possible.append(potential_guess)

		game.generateData(possible)
		game.chooseBest(possible)

		print(game.topChoice)
		if game.actualCheck(word):
			print('Win in %s tries!' %game.tries)
			return game.tries

from random import choice
total = 0
for x in range(10):
        total += main(choice(wordlist))
        print()

print(f'The bot averaged {total/10} guesses across these 10 games.')
input('Type enter to exit.')