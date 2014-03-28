import pygame, sys

class Interface():
	def __init__(self, resolution, color):
		self.resolution = resolution
		windowSurfaceObj = pygame.display.set_mode(resolution)
		windowSurfaceObj.fill(color)
