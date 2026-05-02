import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

# Змейка (список координат [x, y])
snake = [[100, 100], [80, 100], [60, 100]]
dx, dy = 20, 0 # Скорость по X и Y

# Еда
food_x = random.randint(0, 19) * 20
food_y = random.randint(0, 19) * 20
food_weight = 1
food_timer = 100 # Еда исчезнет через 100 шагов змейки

score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: dx, dy = 0, -20
            if event.key == pygame.K_DOWN: dx, dy = 0, 20
            if event.key == pygame.K_LEFT: dx, dy = -20, 0
            if event.key == pygame.K_RIGHT: dx, dy = 20, 0

    # Считаем таймер еды
    food_timer -= 1
    if food_timer <= 0:
        # Время вышло, меняем позицию еды
        food_x = random.randint(0, 19) * 20
        food_y = random.randint(0, 19) * 20
        food_timer = 100 # Сброс таймера

    # Движение (добавляем новую голову)
    head = [snake[0][0] + dx, snake[0][1] + dy]
    snake.insert(0, head)

    # Если съели еду
    if head[0] == food_x and head[1] == food_y:
        score += food_weight
        food_x = random.randint(0, 19) * 20
        food_y = random.randint(0, 19) * 20
        food_timer = 100 # Сброс таймера
        
        # Случайный вес для следующей еды
        if random.randint(1, 10) > 7:
            food_weight = 3
        else:
            food_weight = 1
        # Змея выросла, поэтому хвост НЕ удаляем
    else:
        # Если не ели, удаляем конец хвоста, чтобы змея двигалась
        snake.pop()

    # Отрисовка
    screen.fill((0, 0, 0))
    for s in snake:
        pygame.draw.rect(screen, (0, 255, 0), (s[0], s[1], 20, 20))
    
    if food_weight == 3:
        pygame.draw.rect(screen, (255, 0, 255), (food_x, food_y, 20, 20)) # Супер еда
    else:
        pygame.draw.rect(screen, (255, 0, 0), (food_x, food_y, 20, 20))   # Обычная

    pygame.display.flip()
    clock.tick(10)