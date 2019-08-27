import os
import random

from pygame import mixer

class Audio:

    def __init__(self):
        self.audio_set = {}
        for audio_file in [os.path.splitext(os.path.basename(file))[0] for file in os.listdir('audio') if file.endswith('.ogg')]:
            self.audio_set[audio_file] = mixer.Sound('audio/{}.ogg'.format(audio_file))

    def play_sfx(self, sfx_name):
        if sfx_name in self.audio_set:
            self.audio_set[sfx_name].play()

    def play_any_sfx(self, *sfx_names):
        self.play_sfx(random.choice(sfx_names))

audio = Audio()