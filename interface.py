import pygame, sys, math
from Tank import Tank
from maps import Map
from random import randrange
#from Shot import Shot

# The status bar (bottom bar) height
STATUS_BAR_HEIGHT = 120

#Other status bar information
STATUS_BAR_COLOR = (155,155,155)
OUTLINE_COLOR = (55,55,55)
COLUMN_WIDTH = 425

# Set the fonts
pygame.font.init()
FONT_SIZE = 15
MEDIUM_FONT_SIZE = 28
BIG_FONT_SIZE = 40
FONT = pygame.font.SysFont("Arial", FONT_SIZE)
MEDIUM_FONT = pygame.font.SysFont("Arial", MEDIUM_FONT_SIZE)
BIG_FONT = pygame.font.SysFont("Arial", BIG_FONT_SIZE)
BIG_FONT.set_bold(True)

FONT_COLOR = (55,55,55)

# padding for left and top side of the bar
PAD = 6

class Modes:
    Move, Firing, GameOver = range(3)

class Interface():
    """
    """
    def __init__(self, level, bg_color, pygame):
        """
        Initialize the game's interface
        """
        # Setup variables
        self._level = level
        self._pygame = pygame
        self._bg_color = bg_color

        #Start in player 1 move mode
        self.mode = Modes.Move

        # Load the level information
        # This method also initialize the screen size
        #   according to the map size
        self._loadLevel()

        # The status bar
        self.status_bar = pygame.Rect(0, self._map_resolution[1],
                                     self._screen_resolution[0],
                                     STATUS_BAR_HEIGHT)

        #Initialize tanks
        self.p1_tank = Tank([70, 560], 1)
        self.p2_tank = Tank([1110, 560], 2)

        #Initilize turn number
        self.turn = 1
        #The first one to play is random (not always player 1)
        self.players_turn = randrange(2)+1

        #Set the number of turns
        self.num_teams = 2

        #THIS IS ONLY FOR TEST PURPOSES
        self.cont = 0

        #Load the map information
        self._map = Map(level, bg_color)

        #Initialize the screen
        self._windowSurfaceObj = pygame.display.set_mode(self._screen_resolution)
        self._windowSurfaceObj.fill(bg_color)

        self._map.paintMountain(self._windowSurfaceObj)
        self.draw_bar()
        self.draw_tank(self.p1_tank)
        self.draw_tank(self.p2_tank)

    def _loadLevel(self):
        """
        Load the level information
        """
        #gets the filename
        filename = "maps/" + self._level + ".lvl"
        
        map_file = open(filename, 'r')
        
        # Move up to the line with the size of the map
        line = map_file.readline()
        while line.find("Size: ") < 0:
            line = map_file.readline()
            if line == "":
                raise Exception ("Expected Map Size.")

        # Get the size of the map
        line = line.lstrip("Size: ")
        line = line.strip()
        size = line.split('x')
        map_width, map_height = size
        map_width = int(map_width)
        map_height = int(map_height)

        # Move up to the line with the tank area
        line = map_file.readline()
        while line.find("TankArea: ") < 0:
            line = map_file.readline()
            if line == "":
                raise Exception ("Expected Tank Area.")

        # Get the size of the map
        line = line.lstrip("TankArea: ")
        self._tank_area = line.strip()

        self._map_resolution = (map_width, map_height)
        self._screen_resolution = (map_width, map_height+STATUS_BAR_HEIGHT)

    def update(self):
        """
        Update the interface. This method is called on every frame.
        """
        #Update the display
        self._pygame.display.update()

        # THIS IS ONLY FOR TEST PURPOSES
        # Here Im testing the "destory mountain" thing.
        # Im pretty sure this is not how we do it, because it's really slow
        self.cont += 1
        if self.cont > 50:
            self._map.didShotHitMountain( (200+self.cont-40,200+self.cont-40), 1, self._windowSurfaceObj)


        # draw the bar
        self.draw_bar()

    def draw_bar(self):
        """
        Draws the info bar on the bottom of the screen. 
        """        
        #draw the background of the bar
        pygame.draw.rect(self._windowSurfaceObj, STATUS_BAR_COLOR, self.status_bar)
        
        #draw the outline of the bar
        outlineRect = self.status_bar.copy()
        outlineRect.w -= 1
        outlineRect.h -= 1
        pygame.draw.rect(self._windowSurfaceObj, OUTLINE_COLOR, outlineRect, 2)

        #draw lines between players information
        pygame.draw.line(
            self._windowSurfaceObj,
            OUTLINE_COLOR,
            (COLUMN_WIDTH, self._map_resolution[1]),
            (COLUMN_WIDTH, self._map_resolution[1]+STATUS_BAR_HEIGHT))

        pygame.draw.line(
            self._windowSurfaceObj,
            OUTLINE_COLOR,
            (2*COLUMN_WIDTH, self._map_resolution[1]),
            (2*COLUMN_WIDTH, self._map_resolution[1]+STATUS_BAR_HEIGHT))

        #draw player 1's information
        y = 0
        y += 5 + self.draw_info_text('Player 1', MEDIUM_FONT, MEDIUM_FONT_SIZE, y, 0)
        y += self.draw_info_text('HP:        {}%'.format(self.p1_tank.get_hp_as_percentage()), FONT, FONT_SIZE, y, 0)
        y += self.draw_info_text('Angle:    {}°'.format(self.p1_tank.get_angle()), FONT, FONT_SIZE, y, 0)
        y += self.draw_info_text('Power:  {}%'.format(self.p1_tank.get_power_as_percentage()), FONT, FONT_SIZE, y, 0)

        #draw game information
        y = 0
        y += 5 + self.draw_info_text('Day {}'.format(self.turn), BIG_FONT, BIG_FONT_SIZE, y, 1)
        y += self.draw_info_text('Player {}\'s turn'.format(self.players_turn), FONT, FONT_SIZE, y, 1)

        #TODO
        #draw the button


        #draw player 2's information
        y = 0
        y += 5 + self.draw_info_text('Player 2', MEDIUM_FONT, MEDIUM_FONT_SIZE, y, 2)
        y += self.draw_info_text('HP:        {}%'.format(self.p2_tank.get_hp_as_percentage()), FONT, FONT_SIZE, y, 2)
        y += self.draw_info_text('Angle:    {}°'.format(self.p2_tank.get_angle()), FONT, FONT_SIZE, y, 2)
        y += self.draw_info_text('Power:  {}%'.format(self.p2_tank.get_power_as_percentage()), FONT, FONT_SIZE, y, 2)



    def draw_info_text(self, text, font, font_size, y, column):
        """
        Draws given text with given information.
        """
        line_text = font.render(text, True, FONT_COLOR)
        self._windowSurfaceObj.blit(
            line_text,
            (column*COLUMN_WIDTH + PAD, self._map_resolution[1] + y + PAD))
        return font_size + PAD

    def draw_tank(self, tank):
        """
        Draws given tank
        """
        pos = tank.get_position()
        barrel_pos = tank.get_barrel_position()

        #Rotate the barrel image
        barrel_img = pygame.transform.rotate(tank.image_barrel, tank.get_angle())

        #Calculate the barrel's fixed position - because of the rotation
        y = math.sin(math.radians(abs(tank.get_angle())))*44
        if tank.team == 1:
            x = 0
        else: 
            x = 56 - barrel_img.get_width()

        #Draw the tank and the barrel
        self._windowSurfaceObj.blit(tank.image, (pos[0],pos[1]))
        self._windowSurfaceObj.blit(barrel_img, (barrel_pos[0] + x,barrel_pos[1]-y))
        pygame.display.flip()
    
    def erase_tank(self, tank):
        """
        Erases tank
        """
        pygame.draw.rect(self._windowSurfaceObj, self._bg_color, (tank.position[0],tank.position[1]-45,103,85))
    

    @property
    def cur_team(self):
        """
        Returns the string name of the tank who's turn it currently is. 
        """
        if self.players_turn == 1:
            return self.p1_tank
        else:
            return self.p2_tank
       

    def move_event(self, event):
        """
        Move the tank according to if the left or right arrow was pressed

        """
        if self.mode != Modes.Move:
            return
        
        # team = self.cur_team
        #current_tank = Tank.get_unit(team)
        current_tank = self.cur_team

        self.erase_tank(current_tank)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            current_tank.move_tank([-1,0])

        else:
            current_tank.move_tank([1,0])
        
        self.draw_tank(current_tank)
	


    def shot_angle_change_event(self, event):
        """
        Change the angle of the tank barrel according to if the up 
        or down arrow key was pressed
        """
        current_tank = self.cur_team
        self.erase_tank(current_tank)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            current_tank.change_barrel_angle(1)

        else:
            current_tank.change_barrel_angle(-1)
            
        self.draw_tank(current_tank)

    def move_tank(self, value):
        """
        Move the tank according to if the left or right arrow was pressed

        """
        if self.mode != Modes.Move:
            return
        
        #Get the current tank
        current_tank = self.cur_team

        #Erase it
        self.erase_tank(current_tank)

        #Move it accordingly
        if value == "left":
            current_tank.move_tank([-3,0])

        else:
            current_tank.move_tank([3,0])
        
        #Redraw it
        self.draw_tank(current_tank)

    def change_angle(self, value):
        """
        Change the angle of the tank barrel according to if the up 
        or down arrow key was pressed
        """
        #Get the current tank
        current_tank = self.cur_team

        #Erase it
        self.erase_tank(current_tank)

        #Change the angle accordingly
        if value == "up":
            current_tank.change_barrel_angle(1)

        else:
            current_tank.change_barrel_angle(-1)
            
        #Redraw the tank
        self.draw_tank(current_tank)


    def select_power(self):
        """
        After hitting space to fire, we need to use a timer or somthing
        between events to calculate how hard the shot should be.
        This will eventually read from the arduino potentiometer value and pass that 
        to the shot class. 
        So maybe for now we will hard code it to be (0-100)

        """
        self.change_mode(Modes.Firing)
        shot_power = 50
            

        self.fire_shot(shot_power)
        

    def fire_shot(self,power):
        """
        Creates a shot according toa power value given
        Then creates the effects that follow a shot being fired
        """
        
        if (self.turn) % self.num_teams == 1:
            enemy_tank = self.p2_tank
        else:
            enemy_tank = self.p1_tank

        current_tank = self.cur_team

        new_shot = Shot(power, current_tank.get_angle(), current_tank.get_position()[0], current_tank.get_position()[1])
        if new_shot.check_hit():
            enemy_tank.take_damage(power/25)
         
        self.change_mode(Modes.Move)
        self.next_turn()


    def next_turn(self):
        self.turn +=1

        #Updates the the player's turn variable
        # Which is, whoever turn is it
        if self.players_turn == 1:
            self.players_turn = 2
        else:
            self.players_turn = 1


    def change_mode(self, mode):
        if self.mode == mode:
            return

        self.mode = mode



    
