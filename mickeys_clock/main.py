import pygame 
import sys
from clock import Mik




pygame.init()

    
screen = pygame.display.set_mode((1200, 1200))
pygame.display.set_caption("Clock")

fps_clock = pygame.time.Clock()

mickey_clock = Mik(1200, 1200)
image = pygame.image.load("img/t.png")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        

    screen.fill((255, 255, 255)) 
    pygame.draw.circle(screen, (0,200,20), (600, 600), 220)

    mickey_clock.draw(screen)
    
    screen.blit(image, (383, 383))

    pygame.display.flip()

    fps_clock.tick(60) 


pygame.quit()
sys.exit()

