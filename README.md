CMPUT275-Tank_Wars_Game
=======================




CONTRIBUTORS / LICENSING
========================

Authors:
- Paulo Moreno
- Brandon Hayduk

Generally everything is LICENSE'D under Apache 2 by Paulo Moreno and Brandon Hayduk.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



Description
===========

Our project is a Tank Wars game. The game consists features two tanks wich move around a map and attempt to fire shots and destroy eachother. Players start on oppsing sides of the map and turns alternate between players. Each player on their turn has the opportunity to move their tank, adjust the angle of the barrel of the tank,and then fire a shot. After firing the turn changes to the other player. 
Each player begins with 100% hp and each shot that hits a players tank will decrease its hp until it goes to zero percent, at this time the game will end and the other player wins. 
The game can be played with an arduino controller or the keyboard. 


Game Instructions
=================
To Start the game make sure the requirements in the next section are satisfied. To begin the game run: 
'''bash
python3 TankWars.py
'''

*Please note the game has two modes, control with arduino over port: ACM0
or control via the keyboard

Keyboard Mode:
 
- To play the game with the keyboard, use the arrow keys to move the tank left and right. 
- Use the up/down arrows to adjust the angle of the tanks barrel and the subsequent shot. 
- Hold down the spacebar to begin the power selection for the shot. 
- You will notice a powerbar in the bottom center of the screen that will fluctuate back and forth. 
- Release the spacebar when the image shows the desired power level. This will fire the shot, note that the more full the power bar the further the shot will fire. 



Instructions for playing in Arduino Mode:

- Controller setup: SEE WIRING DIAGRAM
	- JOYSTICK DIGITAL PIN 4 & 
	- VER = A1 (anaolog 1 )
	- HOR = A0 (analog 0 
	- PUSHBUTTON = DIGITAL PIN 3
	
- Connect the Arduino to ACMO
- Run the command make upload in the client folder to upload client.cpp to arduino
- Run the game client with python3 TankWars.py

- Use the joystick to move the tank left / right and the barrel up /down
- Click the joystick or use the button on digital 3 to begin power selectio for the shot
- You will see the power bar at the bottom cycling back and forth, click the joystick again or use the button on digital pin3 to fire the shot at the desired power level according to power level displayed on the bower bar in the bottom center



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





Sound Credits
-------------
All sounds are from FreeSound.org, released under public domain/Creative Commons
licenses. As such, they are free to use in this project assuming credit is
provided.

**Tank fire**
http://www.freesound.org/people/Cyberkineticfilms/sounds/127845/

**Generic explosion**
http://www.freesound.org/people/sarge4267/sounds/102734/
