import pygame, os
from pygame.mixer import Sound

"""
This Class was inspired by the SoundManager from the Assignment 4.
"""


class SoundsController():
    """
    A class to manage sounds. Loads all the sounds and play when requested
    """
    
    def __init__(self):
        """
        Initialize all sounds on sounds folder.
        """
        self.sounds = {}
        self.load_sounds()                
    
    def play(self, sound):
        """
        Plays a requested sound. If the sound isn't already loaded then
        the sound is loaded first.
        """

        # If sound exists and it's in our sound list, play it
        if sound and sound in self.sounds:
            self.sounds[sound].play()
    
    def load_sounds(self):
        """
        Loads all sounds on the sounds directory
        """
        for file in os.listdir("sounds"):
            if file.endswith(".wav"):
                try:
                    # Construct the path
                    path = "sounds/" + file
                    
                    # Load from path and save to the dictionary
                    self.sounds[file[:-4]] = Sound(file = path)
                    self.sounds[file[:-4]].set_volume(1)
                
                # Problem loading the sound
                except pygame.error:
                    print("Exception loading sound file \"{}\".".format(name))
