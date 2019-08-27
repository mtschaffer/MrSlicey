import os
import random

from pygame import mixer

class Audio:

    def __init__(self):
        self.audio_set = {}
        for audio_file in [os.path.splitext(os.path.basename(file))[0] for file in os.listdir('audio/sfx/') if file.endswith('.ogg')]:
            self.audio_set[audio_file] = mixer.Sound('audio/sfx/{}.ogg'.format(audio_file))

    def play_sfx(self, sfx_name):
        if sfx_name in self.audio_set:
            self.audio_set[sfx_name].play()

    def play_any_sfx(self, *sfx_names):
        self.play_sfx(random.choice(sfx_names))

    def play_bgm(self, bgm_name):
        mixer.music.load('audio/bgm/{}.ogg'.format(bgm_name))
        mixer.music.play()

    def stop_sfx(self):
        mixer.stop()
    
    def stop_bgm(self):
        mixer.music.stop()

    def stop_all(self):
        self.stop_sfx()
        self.stop_bgm()
        

audio = Audio()