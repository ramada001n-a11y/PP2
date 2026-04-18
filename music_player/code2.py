import pygame
import os

class music_player:
    def __init__(self):
        self.playlist = []
        self.p = 0
        self.isplay = False


        for m in os.listdir("music"):
            if m.endswith(".mp3") or m.endswith(".wav"):
                self.playlist.append("music/" + m)

        pygame.mixer.music.load(self.playlist[self.p])
    
    def play(self):
        if len(self.playlist) > 0:
            pygame.mixer.music.play()
            self.isplay = True
    def stop(self):
        if len(self.playlist) > 0:
            pygame.mixer.music.stop()
            self.isplay = False

    def next(self):
        if len(self.playlist) > self.p + 1:
            self.p += 1
        else:
            self.p = 0 


        pygame.mixer.music.load(self.playlist[self.p])
        pygame.mixer.music.play()


    def pp(self):
        if self.p > 0:
            self.p -= 1
        elif len(self.playlist) > 1:
            self.p = len(self.playlist) - 1 
        

        pygame.mixer.music.load(self.playlist[self.p])
        pygame.mixer.music.play()


    def name(self):
        if len(self.playlist) == 0:
            return "no music"
        
        return self.playlist[self.p][6:]