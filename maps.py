import pygame


MOUNTAIN_COLOR = (50,255,50)

PIXEL_SKY = 0
PIXEL_MOUNTAIN = 1

EXPLOSION_RADIUS = 0.25

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

    def didShotHitMountain(self, shot_position, power, windowSurfaceObj):
        """
        Check if a given shot hitted the mountain. 
            If it did, return True and destroy the mountain according to
            a explosion radius
        """

        #If the pixel hitted is a mountain:
        if shot_position in self._pixels and self._pixels[shot_position] == PIXEL_MOUNTAIN:
            radius = round(EXPLOSION_RADIUS * power)

            # Run trhough a "kind of" cicrcle shape in order to
            # remove these pixels as mountain and set them as
            # sky pixels.
            for x in range(shot_position[0]-radius,shot_position[0]+radius):
                for y in range(shot_position[1]-radius,shot_position[1]+radius):
                    # Check if its close to the radio
                    if abs(x-shot_position[0])+abs(y-shot_position[1]) < 1.3*radius:
                        # Check if this is a mountain pixel
                        if  (x,y) in self._pixels and self._pixels[(x,y)] == PIXEL_MOUNTAIN:
                            self._pixels[(x,y)] = PIXEL_SKY
                            windowSurfaceObj.set_at((x,y), self._bg_color)
            return True
        else:
            return False

