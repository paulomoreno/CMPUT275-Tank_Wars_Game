import pygame, sys
from maps import Map

# The status bar (bottom bar) height
STATUS_BAR_HEIGHT = 120
STATUS_BAR_COLOR = (55,55,55)

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


        # Load the level information
        # This method also initialize the screen size
        #   according to the map size
        self._loadLevel()

        # The status bar
        self.status_bar = pygame.Rect(0, self._map_resolution[1],
                                     self._screen_resolution[0],
                                     STATUS_BAR_HEIGHT)

        #THIS IS ONLY FOR TEST PURPOSES
        self.cont = 0

        #Load the map information
        self._map = Map(level, bg_color)

        #Initialize the screen
        self._windowSurfaceObj = pygame.display.set_mode(self._screen_resolution)
        self._windowSurfaceObj.fill(bg_color)

        self._map.paintMountain(self._windowSurfaceObj)
        self.draw_bar()

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


        #TODO setup the interface
        # put the bar on the bottom, put the tanks,
        #


    def draw_bar(self):
        """
        Draws the info bar on the bottom of the screen. 
        """        
        #draw the background of the bar
        pygame.draw.rect(self._windowSurfaceObj, STATUS_BAR_COLOR, self.status_bar)
        
        #draw the outline of the bar
        '''outlineRect = self.bar_rect.copy()
        outlineRect.w -= 1
        outlineRect.h -= 1
        pygame.draw.rect(self.screen, OUTLINE_COLOR, outlineRect, 2)'''
