import numpy as np

class Num:
	def __init__(self):
		self.x = 0
		self.ones = np.ones(5)

	def add(self):
		self.x += 1

	def sub(self):
		self.x -= 1

	def print(self):
		print(self.x)
		print(self.ones)
		print('numpy')
