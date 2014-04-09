import pygame, math


MOUNTAIN_COLOR = (50,255,50,255)

PIXEL_SKY = 0
PIXEL_MOUNTAIN = 1

EXPLOSION_RADIUS = 1

class Map():
    """
    This class represents the map (including all graphics/tiles information)
    """
    def __init__(self, level, bg_color):
        """
        Initialize all the map information and functionality
        """
        # Initialize all necessary information
        self._mapName = level + '.gif'
        self._bg_color = bg_color
        self._pixels = dict()

        # Load the .gif map file
        self._loadMap()

    def _loadMap(self):
        """
        Load the .gif file and set the pixels dictionary accordingly
        """
        #gets the filename
        filename = 'maps/' + self._mapName

        # Load in the map image.
        map_image = pygame.image.load(filename)
        self._map_width, self._map_height = map_image.get_size()

        # Go through the image adding pixels
        for w in range(map_image.get_width()):
            for h in range(map_image.get_height()):

                # If this pixel is green, this is mountain
                if map_image.get_palette_at(map_image.get_at_mapped((w, h))).g > 250:
                    self._pixels[(w,h)] = PIXEL_MOUNTAIN
                # Otherwise, this is sky
                else:
                    self._pixels[(w,h)] = PIXEL_SKY


    def paintMountain(self, windowSurfaceObj):
        """
        Paint the mountain according to the list of pixels
        """
        for pos in self._pixels:
            if self._pixels[pos] == PIXEL_MOUNTAIN:
                windowSurfaceObj.set_at(pos, MOUNTAIN_COLOR)

    def didShotHitMountain(self, circle_rect, power, windowSurfaceObj):
        """
        Check if a given shot hitted the mountain. 
            If it did, return True and destroy the mountain according to
            a explosion radius
        """

        collide = False

        for x in range(circle_rect.x, (circle_rect.x + circle_rect.w)):
            for y in range(circle_rect.y, (circle_rect.y + circle_rect.h)):
                if windowSurfaceObj.get_at((x,y)) == MOUNTAIN_COLOR:
                    collide = True
                    radius = round(EXPLOSION_RADIUS * power)
                    pygame.draw.circle(windowSurfaceObj, self._bg_color, (x,y), radius)

        return collide

