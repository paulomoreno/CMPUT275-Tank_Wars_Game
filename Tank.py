#Constant values
TANK_MAXHP = 50

class Tank():
	"""
	This class defines a tank unit
	"""

	def __init__(self, position, team):
		"""
		"""
		self._position = position
		self._team = team

		self._hp = TANK_MAXHP
		self._alive = True 

	def move_tank(self, new_position):
		"""
		This method moves the tank to a new position
		"""

	def take_damage(self, damage):
		"""
		Removes HP from the tank
		"""

		self._hp -= damage