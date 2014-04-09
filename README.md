CMPUT275-Tank_Wars_Game
=======================




CONTRIBUTORS / LICENSING
========================

Authors:
Paulo Moreno
Brandon Hayduk

Generally everything is LICENSE'D under Apache 2 by Paulo Moreno and Brandon Hayduk.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



Description
===========

Our project is a Tank Wars game. The game will consist on an interface and game developed using Python and will run on a computer. The game will be controlled with arduino controllers. Each arduino controller will have a joystick, two buttons, and a potentiometer, 5 LEDS.

The game will have three sections: player 1 area, scenario, and player 2 area. The game will run on turns, so one player can only play during his turn. Each player can walk around their area (using the arduino joystick) and setup the tank aim - such as angle of the barrel and the power of the shot. When the player is ready, he presses a button and shoots - If he hits the other player, the other player’s hp will be reduced according to the shot effectiveness . After the shot is performed the turn is over and it its the other player’s turn.

Specific Details:

- 2D game (think “worms” http://en.wikipedia.org/wiki/Worms_(series) )

	- “View” will be from the side, think cross section. 

	- Game will likely use pygame 



Milestones
==========

- 1 Choose game engine for graphics and implement game visuals, map layouts, as well as tank units. 

- 2 Create classes and add functionality for maps and players (tanks)
	- Moving units (tanks)
	- Moving tank barrels (for angle of shot) 

- 3 Implement physics and computer controller. Implement various game aspects and refine gameplay to encourage competitiveness. 
	- Create bullet shots and damage calculations
	- Test arc trajectories and projectile impacts 

- 4 Implement arduino controller.
	-Convert the power rating (how far projectile fires) to be controlled by the potentiometer 
	- Display the players unit health on the leds on the arduino board as a controller. 
		- For example ⅕ health would display ⅕ green leds lit. 
		- 5/5 health would display 5/5 leds lit. 
	- Implement the joystick left / right to control the tank forward and backward
	- implement the joystick up / down axis to control the angle of the fired projectile


Requirements
============

- pygame

	How to install pygame

```bash
#install dependencies
sudo apt-get install mercurial python3-dev python3-numpy ffmpeg \
    libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
    libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
 
# Grab source
hg clone https://bitbucket.org/pygame/pygame
 
# Finally build and install
cd pygame
python3 setup.py build
sudo python3 setup.py install
```

Sound Credits
-------------
All sounds are from FreeSound.org, released under public domain/Creative Commons
licenses. As such, they are free to use in this project assuming credit is
provided.

**Tank fire**
http://www.freesound.org/people/Cyberkineticfilms/sounds/127845/

**Generic explosion**
http://www.freesound.org/people/sarge4267/sounds/102734/
