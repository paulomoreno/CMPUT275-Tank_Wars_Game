import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((640,480))
pygame.display.set_caption('Tank Wars')

while True:


	for event in pygame.event.get():
		if event.type == QUIT:
				pygame.quit()
				sys.exit()

	pygame.display.update()
	fpsClock.tick(30)