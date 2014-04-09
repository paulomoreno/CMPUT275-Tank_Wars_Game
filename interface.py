import pygame, sys, math, time
from Tank import Tank
from maps import Map
from random import randrange
from shot import Shot
from sounds import SoundsController
# The status bar (bottom bar) height
STATUS_BAR_HEIGHT = 120

#Other status bar information
STATUS_BAR_COLOR = (155,155,155)
OUTLINE_COLOR = (55,55,55)
COLUMN_WIDTH = 425

POWER_BAR_HEIGHT = 20
POWER_BAR_COLOR = (150,150,0)

SHOT_RADIUS = 5
SHOT_COLOR = (20,20,20)

HIT_PERCENTAGE = 0.8

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
    Move, Firing, Draw_Shot, GameOver = range(4)

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

        #Load all the sounds
        self.sound_controller = SoundsController()

        # The status bar
        self.status_bar = pygame.Rect(0, self._map_resolution[1],
                                     self._screen_resolution[0],
                                     STATUS_BAR_HEIGHT)

        # The power bar
        self.power_bar = pygame.Rect(COLUMN_WIDTH + (COLUMN_WIDTH - 100)/2 , self._map_resolution[1] + 80,
                                     100,
                                     POWER_BAR_HEIGHT)

        self.power_outline = self.power_bar.copy()
        self.power_outline.w -= 1
        self.power_outline.h -= 1

        #Set friendly fire
        self.friendly_fire = True

        # Current power
        self.current_power = 20
        self.current_power_increasing = True

        #Initialize tanks
        self.p1_tank = Tank([70, 560], 1)
        self.p2_tank = Tank([1110, 560], 2)

        #Initilize turn number
        self.turn = 1
        #The first one to play is random (not always player 1)
        self.players_turn = randrange(2)+1

        #Set the number of turns
        self.num_teams = 2

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

        # draw the bar
        self.draw_bar()

        #Check if we are supposed to draw the shot
        if self.mode == Modes.Draw_Shot:

            if self.shot_path_index < len(self.shot_path):
                
                #Erase old bullet
                if self.shot_path_index > 0:
                    pos = self.shot_path[self.shot_path_index-1]
                    x = pos[0]
                    y = pos[1]
                    self.erase_shot(x,y)

                #Draw current shot position
                pos = self.shot_path[self.shot_path_index]
                x = pos[0]
                y = pos[1]

                #Check for bounds
                if x >= 0 and y >= 0 and x < self._map_resolution[0] and   y < self._map_resolution[1]:

                    #Get the circle inside the rectangle
                    circle_rect = self.draw_shot(x,y)

                    #Check if the shot hit an obstacle
                    #  For example: if it hit the mountain or a tank
                    if self.shot_path_index > 2 and circle_rect.colliderect(self.p1_tank.get_rect()):
                        self.erase_shot(x,y)
                        self.finish_shot_firing(False, did_hit_team=1)
                    elif self.shot_path_index > 2 and circle_rect.colliderect(self.p2_tank.get_rect()):
                        self.erase_shot(x,y)
                        self.finish_shot_firing(False, did_hit_team=2)
                    elif self._map.didShotHitMountain(circle_rect, self.current_power, self._windowSurfaceObj):
                        self.erase_shot(x,y)
                        self.finish_shot_firing(True, pos=(x,y))



                #Increase the index
                self.shot_path_index += 1

            #If this is the last time, erase the shot
            elif self.shot_path_index == len(self.shot_path) and self.shot_path_index > 0:
                pos = self.shot_path[self.shot_path_index-1]
                x = pos[0]
                y = pos[1]
                self.erase_shot(x,y)

                self.finish_shot_firing(False)

            #Redraw both tanks (just in case the shot hit the tank)
            self.erase_tank(self.p1_tank)
            self.draw_tank(self.p1_tank)
            self.erase_tank(self.p2_tank)
            self.draw_tank(self.p2_tank)

            #If game over
            if self.mode == Modes.GameOver:
                #Call animation to destroy the tank
                self.explode_tank(self.enemy_team)


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
        self.draw_info_text('Power:  {:10.1f}%'.format(self.p1_tank.get_power_as_percentage()), FONT, FONT_SIZE, y, 0)

        #draw game information
        y = 0
        if self.mode == Modes.GameOver:
            y += 5 + self.draw_info_text('Game Over!', BIG_FONT, BIG_FONT_SIZE, y, 1)
            y += self.draw_info_text('Player {} won!'.format(self.players_turn), MEDIUM_FONT, MEDIUM_FONT_SIZE, y, 1)
        else:
            y += 5 + self.draw_info_text('Day {}'.format(self.turn), BIG_FONT, BIG_FONT_SIZE, y, 1)
            y += self.draw_info_text('Player {}\'s turn'.format(self.players_turn), FONT, FONT_SIZE, y, 1)


        #If we are firing, draw the power bar
        if self.mode == Modes.Firing:
            
            self.calculate_power()
            self.power_bar.w = self.current_power
            
            pygame.draw.rect(self._windowSurfaceObj, (POWER_BAR_COLOR[0]+self.current_power,POWER_BAR_COLOR[1]-self.current_power,POWER_BAR_COLOR[2]) , self.power_bar)
            pygame.draw.rect(self._windowSurfaceObj, OUTLINE_COLOR, self.power_outline, 2)


        #draw player 2's information
        y = 0
        y += 5 + self.draw_info_text('Player 2', MEDIUM_FONT, MEDIUM_FONT_SIZE, y, 2)
        y += self.draw_info_text('HP:        {}%'.format(self.p2_tank.get_hp_as_percentage()), FONT, FONT_SIZE, y, 2)
        y += self.draw_info_text('Angle:    {}°'.format(abs(self.p2_tank.get_angle())), FONT, FONT_SIZE, y, 2)
        self.draw_info_text('Power:  {:10.1f}%'.format(self.p2_tank.get_power_as_percentage()), FONT, FONT_SIZE, y, 2)



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

        #Defines the x according to the tank and update the initial shot position
        if tank.team == 1:
            x = 0
            tank.set_shot_start_position(barrel_pos[0] + barrel_img.get_width(), barrel_pos[1]-y)
        else: 
            x = 56 - barrel_img.get_width()
            tank.set_shot_start_position(barrel_pos[0] + x, barrel_pos[1]-y)

        #Draw the tank and the barrel
        self._windowSurfaceObj.blit(tank.image, (pos[0],pos[1]))
        self._windowSurfaceObj.blit(barrel_img, (barrel_pos[0] + x,barrel_pos[1]-y))
        pygame.display.flip()

    def draw_shot(self, x,y):
        """
        Draw a shot on given positon
        """
        return pygame.draw.circle(self._windowSurfaceObj, SHOT_COLOR, (x,y), SHOT_RADIUS)

    def erase_shot(self, x,y):
        """
        Erase a shot on given position
        """
        pygame.draw.circle(self._windowSurfaceObj, self._bg_color, (x,y), SHOT_RADIUS)


    def calculate_power(self):
        """
        Calculates the new power.

        It should increase every frame until it reaches 100.
        After, it decreases until 20 - and keeps going like this until
        the user hits space again
        """
        if self.current_power > 80:
            rate = 3.5
        elif self.current_power > 60:
            rate = 2.3
        elif self.current_power > 40:
            rate = 1.8
        elif self.current_power > 20:
            rate = 1.1
        else:
            rate = 0.5

        if self.current_power_increasing:
            self.current_power += rate

            if self.current_power >= 100:
                self.current_power = 100
                self.current_power_increasing = False

        else:
            self.current_power -= rate

            if self.current_power <= 0:
                self.current_power = 0
                self.current_power_increasing = True

        self.cur_team.update_power(self.current_power)

    def erase_tank(self, tank):
        """
        Erases tank
        """
        pygame.draw.rect(self._windowSurfaceObj, self._bg_color, (tank.position[0],tank.position[1]-45,103,85))
        #pygame.draw.rect(self._windowSurfaceObj, self._bg_color, tank.get_rect())
    
    def explode_tank(self, tank):
        """
        Animation to destroy tank
        """
        self.erase_tank(tank)

    @property
    def cur_team(self):
        """
        Returns the string name of the tank who's turn it currently is. 
        """
        if self.players_turn == 1:
            return self.p1_tank
        else:
            return self.p2_tank
       
    @property
    def enemy_team(self):
        """
        Returns the string name of the tank who's turn it currently is. 
        """
        if self.players_turn == 1:
            return self.p2_tank
        else:
            return self.p1_tank


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
        if self.mode != Modes.Move:
            return

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
        if self.mode != Modes.Move:
            return

        self.change_mode(Modes.Firing)
        
        #self.draw_power_bar()
        #self.


    def release_power(self):
        if self.mode != Modes.Firing:
            return

        self.fire_shot()
        self.current_power = 20
        self.current_power_increasing = True


    def fire_shot(self):
        """
        Creates a shot according toa power value given
        Then creates the effects that follow a shot being fired
        """
        
        self.change_mode(Modes.Draw_Shot)

        enemy_tank = self.enemy_team
        current_tank = self.cur_team

        self.current_shot = Shot(self.current_power, current_tank.get_angle(), current_tank, enemy_tank, self._map_resolution[1], self._map_resolution[0])
        self.shot_path = self.current_shot.get_path()
        self.shot_path_index = 0 

        #play shot sound
        self.sound_controller.play("TankFire");
        #self.sound_controller.play("BombDrop");
         

    def finish_shot_firing(self, didHitMountain, did_hit_team=0, pos=None):
        """
        This method is called after we finish drawing the shot and need to finish the player's turn
        """

        enemy_tank = self.enemy_team
        current_tank = self.cur_team


        if self.players_turn == 1:
            enemy_team_number = 2
        else:
            enemy_team_number = 1

        if pos:
            self.explosion(pos[0], pos[1], 15)
        elif did_hit_team != 0:
            if did_hit_team == 1:
                pos = [(self.p1_tank.get_rect().x + (self.p1_tank.get_rect().w/2)),(self.p1_tank.get_rect().y + (self.p1_tank.get_rect().h/2))]
            elif did_hit_team == 2:
                pos = [(self.p2_tank.get_rect().x + (self.p2_tank.get_rect().w/2)),(self.p2_tank.get_rect().y + (self.p2_tank.get_rect().h/2))]

            self.explosion(pos[0], pos[1], 25)
            

        #If we didn't hit the mountain and did hit the other tank, decrease his hp
        if not didHitMountain and did_hit_team == enemy_team_number:
            enemy_tank.take_damage(self.current_power*HIT_PERCENTAGE)

            #If the enemy was killed, game over!
            if not enemy_tank.active:
                self.change_mode(Modes.GameOver)
                self.erase_tank(enemy_tank)
                return

        #If we didn't hit the mountain, friendly fire is on and we did hit ourselves
        if not didHitMountain and self.friendly_fire and did_hit_team == self.players_turn:
            current_tank.take_damage(self.current_power*HIT_PERCENTAGE)

            #If the played killed himself, game over!
            if not current_tank.active:
                if self.players_turn == 1:
                    self.players_turn = 2
                else:
                    self.players_turn = 1

                self.change_mode(Modes.GameOver)
                self.erase_tank(current_tank)
                return

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

    def explosion(self, x, y, radius):
        """
        Creates an explosion animation centered at x,y with a radius
        """
        self.sound_controller.play("Explosion")

        for i in range(1,10):
            pygame.draw.circle(self._windowSurfaceObj, ( round(100+(i*10)),round(100-(i*10)),0) , (round(x),round(y)), round((radius/10)*i))
            self._pygame.display.update()

        for i in range(10,1):
            pygame.draw.circle(self._windowSurfaceObj, ( round(100+(i*10)),round(100-(i*10)),0) , (round(x),round(y)), round((radius/10)*i))
            self._pygame.display.update()
        
        pygame.draw.circle(self._windowSurfaceObj, self._bg_color, (round(x),round(y)), round(radius))



    
