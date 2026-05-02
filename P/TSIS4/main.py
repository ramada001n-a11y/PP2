import pygame
import sys
import random
import json
import db

pygame.init()
try:
    db.init_db() 
except Exception as e:
    print("Ошибка БД! Проверь пароль в db.py:", e)

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4: Advanced Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 20)

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)         
DARK_RED = (139, 0, 0)    
BLUE = (0, 100, 255)      
GRAY = (128, 128, 128)    

# Загрузка настроек JSON
with open("setting.json", "r") as f:
    settings = json.load(f)
    SNAKE_COLOR = tuple(settings["snake_color"])

state = "MENU"
username = ""
score = 0
level = 1
personal_best = 0

snake = []
dx, dy = BLOCK_SIZE, 0
food_pos = ()
poison_pos = ()
powerup_pos = ()
obstacles = []

# Таймеры и баффы
powerup_active_until = 0
base_fps = 10
current_fps = base_fps

def spawn_item(exclude_list):
    """Генерация координат, чтобы предмет не попал в змейку или стены"""
    while True:
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        if (x, y) not in exclude_list:
            return (x, y)

def reset_game():
    global snake, dx, dy, score, level, food_pos, poison_pos, powerup_pos, obstacles, current_fps, base_fps, personal_best
    snake = [(100, 100), (80, 100), (60, 100)]
    dx, dy = BLOCK_SIZE, 0
    score = 0
    level = 1
    base_fps = 10
    current_fps = base_fps
    obstacles = []
    food_pos = spawn_item(snake + obstacles)
    poison_pos = spawn_item(snake + obstacles + [food_pos])
    powerup_pos = spawn_item(snake + obstacles + [food_pos, poison_pos])
    try:
        personal_best = db.get_personal_best(username)
    except:
        personal_best = 0

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

while True:
    screen.fill(BLACK)
    
    if state == "MENU":
        draw_text("TSIS 4: SNAKE GAME", font, WHITE, 250, 150)
        draw_text("Enter Username: " + username, font, WHITE, 200, 250)
        draw_text("Press ENTER to Play", small_font, WHITE, 300, 350)
        draw_text("Press L for Leaderboard", small_font, WHITE, 300, 400)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username != "":
                    reset_game()
                    state = "GAME"
                elif event.key == pygame.K_l:
                    state = "LEADERBOARD"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.unicode.isalnum():
                    username += event.unicode
                    
    elif state == "GAME":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK_SIZE
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK_SIZE, 0

        head_x = snake[0][0] + dx
        head_y = snake[0][1] + dy
        new_head = (head_x, head_y)

        if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or 
            new_head in snake or new_head in obstacles):
            db.save_score(username, score, level)
            state = "GAME_OVER"

        snake.insert(0, new_head)

        if new_head == food_pos:
            score += 10
            food_pos = spawn_item(snake + obstacles + [poison_pos, powerup_pos])
            if score % 50 == 0:
                level += 1
                base_fps += 2
                current_fps = base_fps
                if level >= 3:
                    for _ in range(3):
                        obstacles.append(spawn_item(snake + [food_pos, poison_pos, powerup_pos]))
        else:
            snake.pop() 
            
        if new_head == poison_pos:
            if len(snake) > 2:
                snake.pop()
                snake.pop()
                poison_pos = spawn_item(snake + obstacles + [food_pos, powerup_pos])
            else:
                try: db.save_score(username, score, level)
                except: pass
                state = "GAME_OVER"
                
        if new_head == powerup_pos:
            current_fps = base_fps + 10 # ускорение
            powerup_active_until = pygame.time.get_ticks() + 5000
            powerup_pos = spawn_item(snake + obstacles + [food_pos, poison_pos])
            
        if pygame.time.get_ticks() > powerup_active_until:
            current_fps = base_fps

        for pos in snake: pygame.draw.rect(screen, SNAKE_COLOR, (*pos, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, (*food_pos, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, DARK_RED, (*poison_pos, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, BLUE, (*powerup_pos, BLOCK_SIZE, BLOCK_SIZE))
        for obs in obstacles: pygame.draw.rect(screen, GRAY, (*obs, BLOCK_SIZE, BLOCK_SIZE))

        draw_text(f"Score: {score} | Level: {level} | Best: {personal_best}", small_font, WHITE, 10, 10)

    elif state == "GAME_OVER":
        draw_text("GAME OVER", font, RED, 320, 200)
        draw_text(f"Final Score: {score} | Level: {level}", small_font, WHITE, 300, 250)
        draw_text("Press ENTER to Restart", small_font, WHITE, 300, 350)
        draw_text("Press M for Menu", small_font, WHITE, 320, 400)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    state = "GAME"
                elif event.key == pygame.K_m:
                    state = "MENU"

    elif state == "LEADERBOARD":
        draw_text("TOP 10 PLAYERS", font, WHITE, 300, 50)
        try:
            top_players = db.get_top_10()
            y_offset = 120
            for i, p in enumerate(top_players):
                draw_text(f"{i+1}. {p[0]} - Score: {p[1]} (Lvl {p[2]})", small_font, WHITE, 250, y_offset)
                y_offset += 30
        except:
            draw_text("DB Error! Check connection.", small_font, RED, 250, 120)
            
        draw_text("Press M for Menu", small_font, WHITE, 320, 500)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                state = "MENU"

    pygame.display.flip()
    

    if state == "GAME":
        clock.tick(current_fps)
    else:
        clock.tick(15) 