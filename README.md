CMPUT275-Tank_Wars_Game
=======================

Authors:

	- Brandon Hayduk

	- Paulo H O Moreno


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