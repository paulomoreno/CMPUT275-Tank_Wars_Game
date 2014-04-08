import pygame, sys
from pygame.locals import *
from interface import Interface

# Constants
SCREEN_SIZE = (1280, 720)
BG_COLOR = (50, 100, 255)


# Initialization
pygame.init()
fpsClock = pygame.time.Clock()

# Our main interface 
# Right now it uses the level 1
# 	TODO: make a code to read from the command line arguments 
# 		  and set the map as the command line arg
level = "1"
main_interface = Interface(level, BG_COLOR, pygame)

pygame.display.set_caption('Tank Wars')

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif (event.type == pygame.KEYDOWN and
              (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
            pygame.display.quit()
            sys.exit()

        #Movement left or right
        #elif (event.type == pygame.KEYDOWN and
        #      (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT)):
            #print(event.key)
        #    main_interface.move_event(event)

        #Shot angle change 
        #elif event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
            #print(event.type)
        #    main_interface.shot_angle_change_event(event)
        
        #Fire Shot
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
            #print(event.type)
            main_interface.select_power()
        
        #if keys[K_UP]:
        #    player.pos.top -= 10
        #if keys[K_DOWN]:
        #    player.pos.left += 10
        #if keys[K_SPACE]: 
        #    print 'firing gun'

    # get key current state
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        main_interface.move_tank("left")
    if keys[K_RIGHT]:
        main_interface.move_tank("right")
    if keys[K_UP]:
        main_interface.change_angle("up")
    if keys[K_DOWN]:
        main_interface.change_angle("down")



    main_interface.update()
    fpsClock.tick(60)
