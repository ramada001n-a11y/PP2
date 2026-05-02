import pygame

class Ball:
    def __init__(self, x, y, screen_w, screen_h):
        self.x = x
        self.y = y
        self.r = 25  
        self.screen_w = screen_w
        self.screen_h = screen_h
    def draw(self,surface): 
        pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), self.r)

    def move(self, dx, dy):
       
        
        new_x = self.x + (dx * 20)
        new_y = self.y + (dy * 20)

        if self.r < new_x < self.screen_w:
            self.x = new_x
        if self.r < new_y < self.screen_h :
            self.y = new_y