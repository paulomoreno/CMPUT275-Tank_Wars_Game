import pygame, sys
from pygame.locals import *
from interface import Interface
import threading
import serial
import time


# Constants
SCREEN_SIZE = (1280, 720)
BG_COLOR = (50, 100, 255)

# Initialization
pygame.init()
fpsClock = pygame.time.Clock()

# Our main interface 
# Right now it uses the level 1
#
level = "1"
main_interface = Interface(level, BG_COLOR, pygame)
left = False

pygame.display.set_caption('Tank Wars')
NO_ARDUINO = False

"""
Try to use the Arduino for the game, if none present to connect to
resort to using the keyboard
"""

#Setup Connection For Serial Port
serialport = "/dev/ttyACM0"

print("Connecting to serial port: %s"% serialport)
#Try the Connection
try:
    serial_connection = serial.Serial(serialport,9600)
#If connection to Arduino  is unsucessful default to using keyboard input 
except:
    print("Failed Connection to Arduino, Starting Keyboard Mode")
    #Infinite Loop for game events
    while True:
        for event in pygame.event.get():
            #End game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #More options for ending the Game
            elif (event.type == pygame.KEYDOWN and
                  (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
                pygame.display.quit()
                sys.exit()
            
            #Begin power selection for tank shot
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                main_interface.select_power()
            #When spacebar is release fire the shot at selected power
            elif event.type == pygame.KEYUP and (event.key == pygame.K_SPACE):
                main_interface.release_power()

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


"""
Connection to arduino was successful so play the game with the arduino controller
"""
print("Connection to Arduino Successful")
start = True

while True:
    """
    Infinite Game loop for playing with the arduino controller
    """
    arduino_input = serial_connection.read().decode('ASCII')

    #Send various commands acccording to what was recieved from the arduino
    if(arduino_input=='R'):
        main_interface.move_tank("right")

    if(arduino_input=='L'):
        main_interface.move_tank("left")

    if(arduino_input=='U'):
        main_interface.change_angle("up")

    if(arduino_input=='D'):
        main_interface.change_angle("down")

    if((arduino_input=='F') and (start==True)):
        main_interface.select_power()
        start = False

    elif(arduino_input=='F' and start==False):
        main_interface.release_power()
        start = True
        
    main_interface.update()
    fpsClock.tick(60)


    


