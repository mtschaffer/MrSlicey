import os
import random

from pygame import mixer

class Audio:

    def __init__(self):
        self.audio_set = {}
        self.active_loops = {}
        for audio_file in [os.path.splitext(os.path.basename(file))[0] for file in os.listdir('audio/sfx/') if file.endswith('.ogg')]:
            self.audio_set[audio_file] = mixer.Sound('audio/sfx/{}.ogg'.format(audio_file))

    def play_sfx(self, sfx_name, volume=1, loops=0):
        if sfx_name in self.audio_set:
            self.audio_set[sfx_name].set_volume(volume)
            self.audio_set[sfx_name].play(loops=loops)

    def play_any_sfx(self, *sfx_names):
        self.play_sfx(random.choice(sfx_names))

    def play_infinite_sfx(self, sfx_name, volume=1):
        if sfx_name in self.audio_set:
            self.audio_set[sfx_name].set_volume(volume)

            #Only play the sound if the sound isn't already active.
            if sfx_name not in self.active_loops:
                self.active_loops[sfx_name] = self.audio_set[sfx_name].play(loops=-1)

    def play_bgm(self, bgm_name):
        mixer.music.load('audio/bgm/{}.ogg'.format(bgm_name))
        mixer.music.play()

    def set_volume_sfx(self, sfx_name, volume):
        if sfx_name in self.audio_set:
            self.audio_set[sfx_name].set_volume(volume)

    def stop_sfx(self, sfx_name):
        if sfx_name in self.audio_set:
            self.audio_set[sfx_name].stop()

    def stop_infinite_sfx(self, sfx_name):
        if sfx_name in self.active_loops:
            self.active_loops[sfx_name].stop()
            del self.active_loops[sfx_name]

    def stop_all_sfx(self):
        mixer.stop()
        for sfx_name, channel in self.active_loops.items():
            channel.stop()
        active_loops = {}
    
    def stop_bgm(self):
        mixer.music.stop()

    def stop_all(self):
        self.stop_all_sfx()
        self.stop_bgm()
        

audio = Audio()