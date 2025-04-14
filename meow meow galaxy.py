import pygame
import random

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
JUMP_VELOCITY = -10
PLATFORM_WIDTH = [100, 90, 150, 80, 120]
PLATFORM_HEIGHT = 20
PLATFORM_GAP = 250  

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 30)
title_font = pygame.font.SysFont("Comic Sans MS", 50)

SKY_COLOR = (100, 100, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 100, 255))  
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.vel_y = 0
        self.on_ground = False
        self.jump_count = 0  

    def update(self, platforms):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat.rect) and self.vel_y > 0:
                self.rect.bottom = plat.rect.top
                self.vel_y = 0
                self.on_ground = True
                self.jump_count = 0 

    def jump(self):
        if self.jump_count < 3 :  
            self.vel_y = JUMP_VELOCITY
            self.jump_count += 1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((random.choice(PLATFORM_WIDTH), PLATFORM_HEIGHT))
        self.image.fill((255, 20, 147))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed):
        self.rect.x -= speed


player = Player()
platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

for i in range(5):
    x = i * PLATFORM_GAP + 200
    y = random.randint(200, 500)
    plat = Platform(x, y)
    platforms.add(plat)
    all_sprites.add(plat)

platform_timer = 0
score = 0
scroll_speed = 4

def menu():
    menu = True
    while menu:
        screen.fill((255, 182, 193))
        # title_text = title_font.render('MEOW MEOW Galaxy', True, (255, 255, 255))
menu()

running = True
boost_activate = False
boost_start_time = 0

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_LSHIFT:
                if not boost_activate:
                    boost_activate = True
                    boost_start_time = pygame.time.get_ticks()

    platform_timer += scroll_speed
    if platform_timer > PLATFORM_GAP:
        y = random.randint(200, 500)
        plat = Platform(WIDTH + random.choice(PLATFORM_WIDTH), y)
        platforms.add(plat)
        all_sprites.add(plat)
        platform_timer = 0
        score += 1

    player.update(platforms)
    for plat in platforms:
        plat.update(scroll_speed)

    for plat in platforms.copy():
        if plat.rect.right < 0:
            platforms.remove(plat)
            all_sprites.remove(plat)

    if boost_activate:
        current_time_ms = pygame.time.get_ticks() - boost_start_time
        current_time_sec = current_time_ms / 1000
        if current_time_sec <= 5:
            scroll_speed = 7
        else:
            boost_activate = False
            scroll_speed = 4
    else:
        scroll_speed = 4

    if player.rect.top > HEIGHT:
        running = False

    screen.fill(SKY_COLOR)
    all_sprites.draw(screen)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()


  


