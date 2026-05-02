import pygame
from datetime import datetime

class Mik:
    def __init__(self, w, h):
        self.center = (w // 2, h // 2)
        self.hand = pygame.image.load("img/mic.png")


        self.min_hand = pygame.transform.scale(self.hand, (int(self.hand.get_width() * 0.2), int(self.hand.get_height() * 0.2)))
        self.sec_hand = pygame.transform.scale(self.hand, (int(self.hand.get_width() * 0.2), int(self.hand.get_height() * 0.3)))

    def get_angles(self):

        now = datetime.now()

       
        sec = -(now.second * 6)
        min= -(now.minute * 6)

        return min, sec
    
    def draw(self, surface):
        min, sec = self.get_angles()


        self.rotate_around(surface, self.min_hand, min)
        self.rotate_around(surface, self.sec_hand, sec)
        
     

    def rotate_around(self, surface, image, angle):
        offset = pygame.math.Vector2(0, image.get_height() / 2)    
        rotated_offset = offset.rotate(-angle)
        
        
        rotated_image = pygame.transform.rotate(image, angle)
        
       
        rect_center = (self.center[0] - rotated_offset.x, self.center[1] - rotated_offset.y)
        new_rect = rotated_image.get_rect(center=rect_center)
        
        surface.blit(rotated_image, new_rect)