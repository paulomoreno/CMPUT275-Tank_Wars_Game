import math

class Shot():

    def __init__(self, power, angle, my_tank, enemy_tank, map_height, map_width):
        self.power = power/5
        self.angle = angle

        self.my_tank = my_tank
        self.enemy_tank = enemy_tank

        self.map_width = map_width
        self.map_height = map_height

        self.path = []

        self._calculate_path()

    def _calculate_path(self):
        """
        Calculate the path your shot should follow.
        """

        gravity = 0.3

        x = self.my_tank.get_shot_start_position()[0]
        y = self.my_tank.get_shot_start_position()[1]

        #Append initial position of the shot
        self.path.append((x,y))

        #If the attacking tank is on the left side, the shot will go to the right
        if self.my_tank.get_team() == 1:

            #Calculate the initial horizontal (x) and vertical (y) velocity of the shot
            xvel = math.cos(math.radians(abs(self.angle))) * self.power
            yvel = math.sin(math.radians(abs(self.angle))) * -self.power

            #While the shot is above the ground, and didnt reach the vertical limit of the screen
            while x < self.map_width and y < self.map_height:

                x += xvel
                y += yvel

                yvel += gravity

                self.path.append((round(x),round(y)))

        #If the attacking tank is on the right, we have a different logic in order to make
        #the shot travel to the left
        else:



            #Calculate the initial horizontal (x) and vertical (y) velocity of the shot
            xvel = math.cos(math.radians(abs(self.angle))) * -self.power
            yvel = math.sin(math.radians(abs(self.angle))) * -self.power

            #While the shot is above the ground, and didnt reach the vertical limit of the screen
            while x > 0 and y < self.map_height:

                x += xvel
                y += yvel

                yvel += gravity

                self.path.append((round(x),round(y)))


    def get_path(self):
        """
        Returns the calculated path
        """
        return self.path

    def check_hit(self, tank=None):
        """
        Checks if the current path hits the enemy tank.
        If none defined, uses the enemy_tank as default
        """
        if not tank:
            tank_rect = self.enemy_tank.get_rect()
        else:
            tank_rect = tank.get_rect()

        for point in self.path:
            if tank_rect.collidepoint(point):
                return True

        return False
