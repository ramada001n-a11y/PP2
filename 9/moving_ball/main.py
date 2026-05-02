import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")


clock = pygame.time.Clock()

ball = Ball(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move(0, -1)
            elif event.key == pygame.K_DOWN:
                ball.move(0, 1)
            elif event.key == pygame.K_LEFT:
                ball.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                ball.move(1, 0)


    screen.fill((255, 255, 255))  
    ball.draw(screen)   

    pygame.display.flip()

    clock.tick(60)


pygame.quit()

