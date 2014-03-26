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
		
		

	def move_tank(self, distance):
		"""
		This method moves the tank to a new position
		"""
		self._position[0] += distance
		

	def is_hit(self, location)
		if(abs(shot[0]-position[0]) <10):
			if(abs(shot[1]-self._position[1]) < 10)
				return True
		
		

	def take_damage(self, damage):
		"""
		Removes HP from the tank
		"""
		
		self._hp -= damage
