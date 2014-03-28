import pygame, sys

class Interface():
	"""
	"""
	def __init__(self, level, bg_color, windowSurfaceObj, pygame):

		self._level = level
		self._pygame = pygame
		self._bg_color = bg_color
		self._loadLevel()

		self._windowSurfaceObj = windowSurfaceObj
		self._windowSurfaceObj.fill(bg_color)

	def _loadLevel(self):

		#self._resolution = (1280,600)
		pass


	def update(self):

		self._pygame.display.update()