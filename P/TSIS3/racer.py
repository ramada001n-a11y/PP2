import pygame
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
LANES = [65, 165, 265, 365] 

class Entity(pygame.sprite.Sprite):
    def __init__(self, image, lane, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(LANES[lane], y))
        self.lane = lane

    def update(self, speed):
        self.rect.y += speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        colors = {"red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0)}
        self.image = pygame.Surface((40, 70))
        self.image.fill(colors.get(color_name, (255, 0, 0)))
        self.lane = 1
        self.rect = self.image.get_rect(center=(LANES[self.lane], SCREEN_HEIGHT - 80))

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.rect.centerx = LANES[self.lane]

    def move_right(self):
        if self.lane < 3:
            self.lane += 1
            self.rect.centerx = LANES[self.lane]

class GameEngine:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        
        diff = self.settings.get("difficulty", "normal")
        self.base_speed = 2 if diff == "easy" else (4 if diff == "normal" else 6)
        self.speed = self.base_speed
        
        self.player = Player(self.settings.get("car_color", "red"))
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        
        self.score = 0
        self.coins_collected = 0
        self.distance = 0
        
        self.active_powerup = None
        self.powerup_timer = 0  
        self.shield_active = False
        self.lives = 1
        
        self.running = True
        self.bg_y = 0

    def spawn_entity(self):
        lane = random.randint(0, 3)
        y_pos = -50
        
        for sprite in self.all_sprites:
            if sprite != self.player and sprite.lane == lane and sprite.rect.y < 100:
                return

        rand_val = random.random()
        if rand_val < 0.5: 
            img = pygame.Surface((40, 70)); img.fill((100, 100, 255))
            e = Entity(img, lane, y_pos)
            self.enemies.add(e)
            self.all_sprites.add(e)
        elif rand_val < 0.7: 
            is_oil = random.random() < 0.5
            img = pygame.Surface((40, 40)); img.fill((139, 69, 19) if is_oil else (105, 105, 105))
            e = Entity(img, lane, y_pos)
            e.is_oil = is_oil
            self.obstacles.add(e)
            self.all_sprites.add(e)
        elif rand_val < 0.95: 
            img = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(img, (255, 215, 0), (10, 10), 10)
            e = Entity(img, lane, y_pos)
            e.value = random.choice([1, 1, 1, 5]) 
            self.coins.add(e)
            self.all_sprites.add(e)
        else: 
            types = ['nitro', 'shield', 'repair']
            p_type = random.choice(types)
            img = pygame.Surface((20, 20), pygame.SRCALPHA)
            color = (0, 255, 255) if p_type == 'nitro' else ((0, 255, 0) if p_type == 'shield' else (255, 105, 180))
            pygame.draw.polygon(img, color, [(10, 0), (20, 20), (0, 20)])
            e = Entity(img, lane, y_pos)
            e.p_type = p_type
            self.powerups.add(e)
            self.all_sprites.add(e)

    def run(self):
        SPAWN_EVENT = pygame.USEREVENT + 1
        spawn_rate = 1500 - (self.base_speed * 50)
        pygame.time.set_timer(SPAWN_EVENT, max(500, spawn_rate))

        while self.running:
            dt = self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.player.move_right()
                if event.type == SPAWN_EVENT:
                    self.spawn_entity()

    
            current_speed = self.speed
            if self.active_powerup == 'nitro':
                current_speed += 5
                self.powerup_timer -= 1
                if self.powerup_timer <= 0:
                    self.active_powerup = None
            
            self.distance += current_speed / 10
            self.speed = self.base_speed + int(self.distance / 500) 
            self.enemies.update(current_speed)
            self.coins.update(current_speed)
            self.obstacles.update(current_speed)
            self.powerups.update(current_speed)

            # Коллизии
            for coin in pygame.sprite.spritecollide(self.player, self.coins, True):
                self.coins_collected += coin.value
                self.score += coin.value * 10
            
            for p in pygame.sprite.spritecollide(self.player, self.powerups, True):
                if p.p_type == 'nitro':
                    self.active_powerup = 'nitro'
                    self.powerup_timer = 240    
                elif p.p_type == 'shield':
                    self.shield_active = True
                elif p.p_type == 'repair':
                    self.lives += 1

            
            hit_enemy = pygame.sprite.spritecollideany(self.player, self.enemies)
            hit_obs = pygame.sprite.spritecollideany(self.player, self.obstacles)
            
            if hit_enemy or hit_obs:
                if hit_obs and hit_obs.is_oil == True:
                    current_speed = max(2, current_speed - 5) 
                    hit_obs.kill()
                else:
                    if self.shield_active:
                        self.shield_active = False
                        if hit_enemy: hit_enemy.kill()
                        if hit_obs: hit_obs.kill()
                    else:
                        self.lives -= 1
                        if hit_enemy: hit_enemy.kill()
                        if hit_obs: hit_obs.kill()
                        if self.lives <= 0:
                            self.running = False 

            self.score = int(self.distance) + self.coins_collected * 10

            self.screen.fill((50, 50, 50))
            
            self.bg_y = (self.bg_y + current_speed) % 40
            for i in range(-40, SCREEN_HEIGHT, 40):
                for lane_x in LANES[:-1]:
                    pygame.draw.rect(self.screen, (255, 255, 255), (lane_x + 45, i + self.bg_y, 10, 20))

            self.all_sprites.draw(self.screen)

            ui_texts = [
                f"Score: {self.score}",
                f"Coins: {self.coins_collected}",
                f"Dist: {int(self.distance)}m",
                f"Lives: {self.lives}"
            ]
            for i, text in enumerate(ui_texts):
                surf = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(surf, (10, 10 + i * 30))

            if self.active_powerup == 'nitro':
                surf = self.font.render(f"NITRO: {self.powerup_timer//1000}s", True, (0, 255, 255))
                self.screen.blit(surf, (SCREEN_WIDTH - 120, 10))
            if self.shield_active:
                surf = self.font.render("SHIELD ACTIVE", True, (0, 255, 0))
                self.screen.blit(surf, (SCREEN_WIDTH - 150, 40))

            pygame.display.flip()

        pygame.time.set_timer(SPAWN_EVENT, 0)
        return {"score": self.score, "coins": self.coins_collected, "distance": int(self.distance)}