import random
import pygame
import math
import sys
from copy import deepcopy

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class minimaxAI(connect4Player):

	def play(self, env, move):
		
		random.seed(self.seed)
		isMax = True
		dep = 2
		# find all possible spots
		env = deepcopy(env)
		env.visualize = False
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p:
				indices.append(i)
		# call the minimax algorithm and make the optimal move
		col = self.minimax(deepcopy(env), dep, isMax, self.position)[0]
		move[:] = [col]
	# minimax algorithm
	def minimax(self, env, dep, isMax, player):

		# find all possible spots in the given state
		env.visualize = False
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p:
				indices.append(i)

		# check if terminal state is reached
		# if it is the terminal state, decide the winner and return max or min score
		# if it is not terminal state, run the evaluation function to get a score
		gameOver = self.isTerminal(env)
		if dep == 0 or gameOver:
			if gameOver:
				if player == self.position:
					return(None, 100000000)
				elif player == self.opponent.position:
					return(None, -100000000)
			else:
				return(None, self.evaluateState(env))
		# recursively run the minimax algorithm
		# max branches
		if isMax:

			maxScore = -math.inf
			isMax = False

			for col in indices:
				env = deepcopy(env)
				tmpEnv = self.simulateMove(env, col, self.position)
				score = self.minimax(tmpEnv, dep - 1, isMax, self.opponent.position)[1]
				

				if score > maxScore:
					maxScore = score
					move = col

			return move, maxScore
		# min branches
		else:

			minScore = math.inf
			isMax = True

			for col in indices:
				env = deepcopy(env)
				tmpEnv = self.simulateMove(env, col, self.opponent.position)
				score = self.minimax(tmpEnv, dep - 1, isMax, self.position)[1]
				

				if score < minScore:
					minScore = score
					move = col
			
			return move, minScore

	# the evaluation function
	def evaluateState(self, env):

		# initialize score
		score = 0
		
		# evaluate the central column
		cenArr = [i for i in list(env.board[:, 3])]
		centerEmpty = cenArr.count(0)
		centerCount = cenArr.count(self.position)
		if centerEmpty >= 3:
			# The center column is important in early game so 
			# I'm trying to make my algorithm occupy more cells 
			# in the center in early game.
			score += centerCount * 3
		
		# evaluate the horizontal score
		for r in range(0, 6):
			rowArr = [i for i in list(env.board[r, :])]
			for c in range(0, 4):
				fourBlock = rowArr[c:c+4]
				score += self.evaluateFourBlock(fourBlock, rowArr)
			for c in range(0, 3):
				fiveBlock = rowArr[c:c+5]
				score += self.evaluateFiveBlock(fiveBlock, fiveBlock)

		# evaluate the vertical score
		for c in range(0, 7):
			colArr = [i for i in list(env.board[:, c])]
			for r in range(0, 3):
				fourBlock = colArr[r:r+4]
				score += self.evaluateFourBlock(fourBlock, colArr)
			for r in range(0, 2):
				fiveBlock = colArr[r:r+5]
				score += self.evaluateFiveBlock(fiveBlock, fiveBlock)
		
		# evaluate the diagonal score
		for r in range(0, 2):
			for c in range(0, 3):
				fourBlock = [env.board[r + i][c + i] for i in range(4)]
				score += self.evaluateFourBlock(fourBlock, fourBlock)
		for r in range(0, 2):
			for c in range(0, 3):
				fiveBlock = [env.board[r + i][c + i] for i in range(5)]
				score += self.evaluateFiveBlock(fiveBlock, fiveBlock)

		for r in range(0, 2):
			for c in range(0, 3):
				fourBlock = [env.board[r + 3 - i][c + i] for i in range(4)]
				score += self.evaluateFourBlock(fourBlock, fourBlock)
		for r in range(0, 2):
			for c in range(0, 3):
				fiveBlock = [env.board[r + 4 - i][c + i] for i in range(5)]
				score += self.evaluateFiveBlock(fiveBlock, fiveBlock)
		
		return score


	def evaluateFourBlock(self, fourBlock, arr):

		score = 0
		reward = 0

		if arr.count(0) >= 3:
			reward = 1

		if fourBlock.count(self.position) == 4:
			score += 100 + reward
		elif fourBlock.count(self.position) == 3 and fourBlock.count(0) == 1:
			score += 10 + reward * 2
		elif fourBlock.count(self.position) == 2 and fourBlock.count(0) ==2:
			score += 4 + reward
		elif fourBlock.count(self.opponent.position) == 4:
			score -= 99 + reward
		elif fourBlock.count(self.opponent.position) == 3 and fourBlock.count(0) == 1:
			score -= 9 + reward * 2
		elif fourBlock.count(self.opponent.position) == 2 and fourBlock.count(0) == 2:
			score -= 3 + reward

		return score

	def evaluateFiveBlock(self, fiveBlock, arr):
		score = 0
		reward = 0

		if arr.count(0) >= 3:
			reward = 1

		if fiveBlock.count(self.position) == 3 and fiveBlock.count(0) == 2:
			score += 9 + reward * 2
		elif fiveBlock.count(self.position) == 2 and fiveBlock.count(0) == 3:
			score += 5 + reward
		elif fiveBlock.count(self.opponent.position) == 3 and fiveBlock.count(0) == 2:
			score -= 7 + reward *2
		elif fiveBlock.count(self.opponent.position) == 2 and fiveBlock.count(0) == 3:
			score -= 2 + reward

		return score


	def isTerminal(self, env):
		if len(env.history[0]) == 42:
			return True

		# check horizontal terminal condition
		for r in range(0, 6):
			rowArr = [i for i in list(env.board[r, :])]
			for c in range (0, 4):
				block = rowArr[c:c+4]
				if block.count(self.position) == 4:
					return True
				elif block.count(self.opponent.position) == 4:
					return True
				else:
					return False

		# check vertical terminal condition
		for c in range(0, 7):
			colArr = [i for i in list(env.board[:, c])]
			for r in range(0, 3):
				block = colArr[r:r+4]
				if block.count(self.position) == 4:
					return True
				elif block.count(self.opponent.position) == 4:
					return True
				else:
					return False

		# check diagonal terminal condition
		for c in range(0, 3):
			for r in range(0, 2):
				block = [env.board[r + i][c + i] for i in range(4)]
				if block.count(self.position) == 4:
					return True
				elif block.count(self.opponent.position) == 4:
					return True
				else:
					return False
		
		for c in range(0, 3):
			for r in range(0, 2):
				block = [env.board[r + 3 - i][c + i] for i in range(4)]
				if block.count(self.position) == 4:
					return True
				elif block.count(self.opponent.position) == 4:
					return True
				else:
					return False


	def simulateMove(self, env, move, player):

		env = deepcopy(env)
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
		return env


					
		

		

class alphaBetaAI(connect4Player):

	def play(self, env, move):
		
		random.seed(self.seed)

		isMax = True
		dep = 4
		# find all possible spots
		env = deepcopy(env)
		env.visualize = False
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p:
				indices.append(i)
		# call the alpha beta pruning algorithm and make the optimal move
		col = self.abPruning(deepcopy(env), dep, -math.inf, math.inf, isMax, self.position)[0]
		move[:] = [col]

	# alpha beta pruning algorithm
	def abPruning(self, env, dep, alpha, beta, isMax, player):

		# find all possible spots in the given state
		env.visualize = False
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p:
				indices.append(i)

		# check if terminal state is reached
		# if it is the terminal state, decide the winner and return max or min score
		# if it is not terminal state, run the evaluation function to get a score
		gameOver = self.isTerminal(env)
		if dep == 0 or gameOver:
			if gameOver:
				if player == self.position:
					return(None, 100000000)
				elif player == self.opponent.position:
					return(None, -100000000)
			else:
				return(None, self.evaluateState(env))
		# recursively run the alpha beta pruning algorithm
		# max branches
		if isMax:
			maxScore = -math.inf
			isMax = False
			orderedIndices = self.orderIndice(deepcopy(env))
			for col in orderedIndices:
			#for col in indices:
				env = deepcopy(env)
				tmpEnv = self.simulateMove(env, col, self.position)
				score = self.abPruning(tmpEnv, dep - 1, alpha, beta, isMax, self.opponent.position)[1]

				if score > maxScore:
					maxScore = score
					move = col

				alpha = max(alpha, score)
				if alpha >= beta:
					break

			return move, maxScore
		# min branches
		else:
			minScore = math.inf
			isMax = True
			orderedIndices = self.orderIndice(deepcopy(env))
			for col in orderedIndices:
			#for col in indices:
				env = deepcopy(env)
				tmpEnv = self.simulateMove(env, col, self.opponent.position)
				score = self.abPruning(tmpEnv, dep - 1, alpha, beta, isMax, self.position)[1]


				if score < minScore:
					minScore = score
					move = col
				
				beta = min(beta, minScore)
				if alpha >= beta:
					break
			
			return move, minScore

	def orderIndice(self, env):

		col = [0, 1, 2, 3, 4, 5, 6]
		score = [0, 0, 0, 0, 0, 0, 0]

		# evaluate the vertical score
		for c in range(0, 7):
			colArr = [i for i in list(env.board[:, c])]
			for r in range(0, 3):
				fourBlock = colArr[r:r+4]
				score[c] = self.evaluateFourBlock(fourBlock, colArr)

		for i in range(1, len(score)):

			key = score[i]
			index = col[i]
			j = i - 1
			while j>= 0 and key < score[j]:
				score[j + 1] = score[j]
				col[j + 1] = col[j]
				j -= 1
			score[j + 1] = key
			col[j + 1] = index
		return col

	# the evaluation function
	def evaluateState(self, env):

		# initialize score
		score = 0
		
		# evaluate the central column
		cenArr = [i for i in list(env.board[:, 3])]
		centerEmpty = cenArr.count(0)
		centerCount = cenArr.count(self.position)
		if centerEmpty >= 3:
			# The center column is important in early game so 
			# I'm trying to make my algorithm occupy more cells 
			# in the center in early game.
			score += centerCount * 3
		
		# evaluate the horizontal score
		for r in range(0, 6):
			rowArr = [i for i in list(env.board[r, :])]
			for c in range(0, 4):
				fourBlock = rowArr[c:c+4]
				score += self.evaluateFourBlock(fourBlock, rowArr)
			for c in range(0, 3):
				fiveBlock = rowArr[c:c+5]
				score += self.evaluateFiveBlock(fiveBlock, rowArr)

		# evaluate the vertical score
		for c in range(0, 7):
			colArr = [i for i in list(env.board[:, c])]
			for r in range(0, 3):
				fourBlock = colArr[r:r+4]
				score += self.evaluateFourBlock(fourBlock, colArr)
			for r in range(0, 2):
				fiveBlock = colArr[r:r+5]
				score += self.evaluateFiveBlock(fiveBlock, colArr)
		
		# evaluate the diagonal score
		for r in range(0, 2):
			for c in range(0, 3):
				fourBlock = [env.board[r + i][c + i] for i in range(4)]
				score += self.evaluateFourBlock(fourBlock, fourBlock)
		for r in range(0, 2):
			for c in range(0, 3):
				fiveBlock = [env.board[r + i][c + i] for i in range(5)]
				score += self.evaluateFiveBlock(fiveBlock, fiveBlock)

		for r in range(0, 2):
			for c in range(0, 3):
				fourBlock = [env.board[r + 3 - i][c + i] for i in range(4)]
				score += self.evaluateFourBlock(fourBlock, fourBlock)
		for r in range(0, 2):
			for c in range(0, 3):
				fiveBlock = [env.board[r + 4 - i][c + i] for i in range(5)]
				score += self.evaluateFiveBlock(fiveBlock, fiveBlock)
		
		return score

	def evaluateFourBlock(self, fourBlock, arr):

		score = 0
		reward = 0

		if arr.count(0) >= 3:
			reward = 1

		if fourBlock.count(self.position) == 4:
			score += 100 + reward
		elif fourBlock.count(self.position) == 3 and fourBlock.count(0) == 1:
			score += 10 + reward * 2
		elif fourBlock.count(self.position) == 2 and fourBlock.count(0) ==2:
			score += 4 + reward
		elif fourBlock.count(self.opponent.position) == 4:
			score -= 99 + reward
		elif fourBlock.count(self.opponent.position) == 3 and fourBlock.count(0) == 1:
			score -= 9 + reward * 2
		elif fourBlock.count(self.opponent.position) == 2 and fourBlock.count(0) == 2:
			score -= 3 + reward

		return score

	def evaluateFiveBlock(self, fiveBlock, arr):
		score = 0
		reward = 0

		if arr.count(0) >= 3:
			reward = 1

		if fiveBlock.count(self.position) == 3 and fiveBlock.count(0) == 2:
			score += 9 + reward * 2
		elif fiveBlock.count(self.position) == 2 and fiveBlock.count(0) == 3:
			score += 5 + reward
		elif fiveBlock.count(self.opponent.position) == 3 and fiveBlock.count(0) == 2:
			score -= 7 + reward *2
		elif fiveBlock.count(self.opponent.position) == 2 and fiveBlock.count(0) == 3:
			score -= 2 + reward

		return score


	def isTerminal(self, env):
		if len(env.history[0]) == 42:
			return True

		# check horizontal terminal condition
		for r in range(0, 6):
			rowArr = [i for i in list(env.board[r, :])]
			for c in range (0, 4):
				block = rowArr[c:c+4]
				if block.count(self.position) == 4:
					return True
				elif block.count(self.opponent.position) == 4:
					return True
				else:
					return False

		# check vertical terminal condition
		for c in range(0, 7):
			colArr = [i for i in list(env.board[:, c])]
			for r in range(0, 3):
				block = colArr[r:r+4]
				if block.count(self.position) == 4:
					return True
				elif block.count(self.opponent.position) == 4:
					return True
				else:
					return False

		# check diagonal terminal condition
		for c in range(0, 3):
			for r in range(0, 2):
				block = [env.board[r + i][c + i] for i in range(4)]
				if block.count(self.position) == 4:
					return True
				elif block.count(self.opponent.position) == 4:
					return True
				else:
					return False

		for c in range(0, 3):
			for r in range(0, 2):
				block = [env.board[r + 3 - i][c + i] for i in range(4)]
				if block.count(self.position) == 4:
					return True
				elif block.count(self.opponent.position) == 4:
					return True
				else:
					return False


	def simulateMove(self, env, move, player):

		env = deepcopy(env)
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)
		return env



SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)