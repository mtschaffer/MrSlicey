import random

from pygame import mixer

class Audio:

    def __init__(self):
        #TODO:  load from file listing
        self.audio_set = {
            'pew': mixer.Sound('audio/pew.ogg'),
            'drumstick1': mixer.Sound('audio/drumstick1.ogg'),
            'drumstick2': mixer.Sound('audio/drumstick2.ogg'),
        }

    def play_sfx(self, sfx_name):
        if sfx_name in self.audio_set:
            self.audio_set[sfx_name].play()

    def play_any_sfx(self, *sfx_names):
        self.play_sfx(random.choice(sfx_names))

audio = Audio()