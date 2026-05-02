import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

player = pygame.Rect(180, 500, 40, 60)
enemy = pygame.Rect(random.randint(0, 360), 0, 40, 60)
coin = pygame.Rect(random.randint(0, 380), 0, 20, 20)

enemy_speed = 5
score = 0
coin_weight = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: 
        player.x -= 5
    if keys[pygame.K_RIGHT]: 
        player.x += 5

    enemy.y += enemy_speed
    coin.y += 4

    if enemy.y > 600:
        enemy.y = 0
        enemy.x = random.randint(0, 360)
    
    if coin.y > 600:
        coin.y = 0
        coin.x = random.randint(0, 380) 
    if player.colliderect(coin):
        score += coin_weight
        coin.y = 0 
        coin.x = random.randint(0, 380)
        
        if random.randint(1, 10) > 8:
            coin_weight = 3 
        else:
            coin_weight = 1
            
        if score >= 5:
            enemy_speed = 5 + (score // 5)

    if player.colliderect(enemy):
        exit()

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), player) 
    pygame.draw.rect(screen, (255, 0, 0), enemy)  
    
    if coin_weight == 3:
        pygame.draw.rect(screen, (255, 255, 0), coin) 
    else:
        pygame.draw.rect(screen, (0, 255, 0), coin)   

    pygame.display.flip()
    clock.tick(60)