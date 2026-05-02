import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
screen.fill((255, 255, 255)) # Сразу заливаем белым фоном


mode = "1" # 1-квадрат, 2-прямоуг.треуг, 3-равностор.треуг, 4-ромб
color = (0, 0, 0) 


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        # Кнопки 1, 2, 3, 4 для смены фигур
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: mode = "1"
            if event.key == pygame.K_2: mode = "2"
            if event.key == pygame.K_3: mode = "3"
            if event.key == pygame.K_4: mode = "4"

        # Рисуем только по клику мышки
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos # Получаем координаты клика
            
            if mode == "1":
                # Квадрат (Draw square)
                pygame.draw.rect(screen, color, (x, y, 50, 50), 2)
            
            elif mode == "2":
                # Прямоугольный треугольник (Draw right triangle)
                pygame.draw.polygon(screen, color, [[x, y], [x, y+50], [x+50, y+50]], 2)
            
            elif mode == "3":
                # Равносторонний треугольник (Draw equilateral triangle)
                pygame.draw.polygon(screen, color, [[x, y], [x-30, y+50], [x+30, y+50]], 2)
            
            elif mode == "4":
                # Ромб (Draw rhombus)
                pygame.draw.polygon(screen, color, [[x, y-30], [x+30, y], [x, y+30], [x-30, y]], 2)

    pygame.display.flip()