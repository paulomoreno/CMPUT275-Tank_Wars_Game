import pygame
from pygame.sprite import Sprite

#Constant values
TANK_MAXHP = 50
TANK_MAXPWR = 100
TANK_WIDTH = 100
TANK_HEIGHT = 40 
MAX_ANGLE = 90
MIN_ANGLE = 0


active_units = pygame.sprite.LayeredUpdates()

class Tank(Sprite):
    """
    This class defines a tank unit

    #TODO LIST:
    -still need function for barrel movement, which will call _update_image
    and update self._angle
    """

    def __init__(self, position, team):
        """
        """
        Sprite.__init__(self)

        self.position = position
        self.team = team
        self.health = TANK_MAXHP
        self._barrel_angle = 45.0
        self._alive = True 
        self._barrel_power = TANK_MAXPWR
    

        if team == 1:
            self.image = pygame.image.load("tank/tank.png")
            self.image_barrel = pygame.image.load("tank/tank_barrel.png")
            self.shot_initial_pos = [self.position[0]+96, self.position[1]+6]
            self.bounds = (0, 240)
        else:
            self.image = pygame.image.load("tank/tank_p2.png")
            self.image_barrel = pygame.image.load("tank/tank_barrel_p2.png")
            self.shot_initial_pos = [self.position[0]+36, self.position[1]+6]
            self.bounds = (1040, 1280)

        #self.image_barrel = None #Barrel Image
        #REQUIRED PYGAME Items
        #self.image = None
        self.rect = pygame.Rect(position[0],position[1],TANK_WIDTH, TANK_HEIGHT) #define outer size
        self._update_image()
        
        #if activate:
        #    self.activate()


    def get_hp_as_percentage(self):
        """
        Returns the hp as percentage
        """
        return (self.health / TANK_MAXHP) * 100

    def set_shot_start_position(self, x, y):
        """
        Updates the initial shot position (this is called when we rotate the barrel)
        """
        self.shot_initial_pos[0] = round(x)
        self.shot_initial_pos[1] = round(y)

    def get_shot_start_position(self):
        """
        Returns the initial position for the shot
        """
        return self.shot_initial_pos

    def get_power_as_percentage(self):
        """
        Returns the hp as percentage
        """
        return (self._barrel_power / TANK_MAXPWR) * 100

    def get_angle(self):
        """
        Returns barrel angle
        """
        if self.team == 1:
            return self._barrel_angle
        else:
            return -self._barrel_angle

    def get_position(self):
        """
        Returns the tank position
        """
        return self.position

    def get_barrel_position(self):
        """
        Returns the tank's barrel position
         - depending on the team, its a different position, because 
        """
        if self.team == 1:
            return (self.position[0]+52, self.position[1]+6)
        else:
            return (self.position[0]-8, self.position[1]+6)
    
    def get_team(self):
        """
        What is my team
        """
        return self.team  

    def get_rect(self):
        """
        Returns a rectangle that contains the tank
        """
        return self.rect

    @staticmethod
    def get_unit(cur_team):
        """
        Return the unit at given position with help of 
        sprite class
        """
        for u in Tank.active_units:
            if(u.team) == cur_team:
                return u
        return None

    @property
    def active(self):
        """
        is the unit active?
        """
        return self._alive

    def move_tank(self, distance):
        """
        This method moves the tank to a new position,
        takes a distance change list [delta x, delta y] 
        """
        #Check bounds for team 1
        if (self.position[0] + distance[0]) > self.bounds[0] and (self.position[0] + distance[0] + TANK_WIDTH) < self.bounds[1]:
            self.position[0] += distance[0]
            self.position[1] += distance[1]
            self.rect.move_ip(distance[0],distance[1])

    def change_barrel_angle(self, value):
        if self._barrel_angle + value >= MIN_ANGLE and self._barrel_angle + value <= MAX_ANGLE:
            self._barrel_angle += value

    def update_power(self, power):
        """
        Updates the power
        """
        if power >= TANK_MAXPWR:
            self._barrel_power = 100
        elif power <= 0:
            self._barrel_power = 0
        else:
            self._barrel_power = power

    def is_hit(self, location):
        """
        Calculates if a tank will be hit 
        when given the location of a projectile's shot in
        the form [x,y] of the shot
        """ 
        
        if(abs(shot[0]-position[0]) <10):
            if(abs(shot[1]-self.position[1]) < 10):
                return True
        else:
            return False
        

    def take_damage(self, damage):
        """
        Removes HP from the tank
        """
        self.health -= damage

        if self.health <= 0:
            self.health = 0
            self.deactivate
            self._alive = False

    def angel(self):
        return self._barrel_angle


    def _update_image(self):
        """
        Re-creates the units image
        Note that tanks will need to be composed of two 
        sub images. The first will be the body of the tank
        which will not rotate. 
        The second image component will need to be the barrel, 
        this part of the image will need to be rotated according
        to changing barrel angle directions. 
        """
        try:
            subsurf = self._base_image.subsurface(subrect)
        except ValueError:
            print("Unable to evalute tank")
        except AttributeError:
            return
        #Rotate Barrel
        self.image = pygame.transform.rotate(subsurf, self._barrel_angle)
        #Display Health
        health_surface = BaseUnit.health_font.render(str(int(self.health)))
        image_rect = self.image.get_rect()
        health_rect = health_surf.get_rect()
        health_rect.move_ip(image_rect.w - health_rect.w,
                    image_rect.h - health_rect.h)
        self.image.blit(health_surace, health_rect)

    def activate(self):
        """
        adds this unit to the active roster.
        """
        if not self._active:
            self._active = True
            BaseUnit.active_units.add(self)

    def deactivate(self):
        if self._active:
            self._active = False
            BaseUnit.active_units.remove(self)

