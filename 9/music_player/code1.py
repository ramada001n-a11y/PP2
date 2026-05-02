import pygame
from code2 import music_player


pygame.init()
font = pygame.font.Font(None, 30)
screen = pygame.display.set_mode((600,600))

run = True
music_players = music_player()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                music_players.play()
            if event.key == pygame.K_s:
                music_players.stop()
            if event.key == pygame.K_n:
                music_players.next()
            if event.key == pygame.K_b:
                music_players.pp()
            if event.key == pygame.K_q:
                run = False
    screen.fill((255,255,255))
    name = music_players.name()
    name_text = font.render("music name: " + name, True, (0,200,50))
    screen.blit(name_text, (20,80))
    if music_players.isplay:
        s_text = font.render("Статус: Играет", True, (200, 255, 200))
    else:
        s_text = font.render("Статус: Стоп", True, (255, 200, 200))
    screen.blit(s_text, (20, 60))
    h_text = font.render("P-играть, S-стоп, N-след, B-пред, Q-выход", True, (150, 150, 150))
    screen.blit(h_text, (20, 200))
    

    pygame.display.update()

