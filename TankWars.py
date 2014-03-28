import pygame, sys
from pygame.locals import *
from Interface import Interface

# Constants
SCREEN_SIZE = (1280, 720)
BG_COLOR = (50, 100, 255)


# Initialization
pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((1280,720))
windowSurfaceObj.fill(BG_COLOR)

# Our main interface 
# Right now it uses the level 1
# 	TODO: make a code to read from the command line arguments 
# 		  and set the map as the command line arg
level = "1"
main_interface = Interface(level, BG_COLOR, windowSurfaceObj, pygame)

pygame.display.set_caption('Tank Wars')

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
                pygame.quit()
                sys.exit()

    main_interface.update()
    fpsClock.tick(60)