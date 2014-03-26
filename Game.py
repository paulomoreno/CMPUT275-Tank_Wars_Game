
class Game():
	"""
	This class defines the game. Here we have all information,
	such as the units properties (life, position),
	number of turns, and other important information
	"""

	def __init__(self, level):
		"""
		Lads the information according to the level
		"""
		self.p1_tank = Tank([100, 150], 0)
		self.p2_tank = Tank([400, 150], 1)

		self.turn = 0

		self.level = level
