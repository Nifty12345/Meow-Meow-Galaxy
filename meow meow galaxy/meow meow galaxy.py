import pygame
import random
import os

pygame.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Meow Meow Galaxy")
clock = pygame.time.Clock()

PLAYER_WIDTH = 250
PLAYER_HEIGHT = 205
GRAVITY = 0.5
JUMP_STRENGTH = -15
MAX_JUMPS = 2
PLAYER_SPEED = 17
PLAYER_MAX_SPEED = 25
PLAYER_ACCELERATION = 0.025

PLATFORM_WIDTHS = [400, 350, 450, 600]
PLATFORM_HEIGHT = 30
PLATFORM_GAP_X = 650
PLATFORM_GAP_Y = 250

VOLUME_SLIDER_WIDTH = 200
VOLUME_SLIDER_HEIGHT = 20
VOLUME_SLIDER_X = WIDTH - 260
VOLUME_SLIDER_Y = 50
VOLUME_HANDLE_WIDTH = 15
VOLUME_HANDLE_HEIGHT = 30

SLIDER_BG_COLOR = (70, 70, 70)        
SLIDER_BORDER_COLOR = (150, 150, 150)
SLIDER_FILL_COLOR = (255, 100, 100)    
HANDLE_COLOR = (255, 255, 255)        
HANDLE_BORDER_COLOR = (200, 200, 200)  

PLATFORM_SPRITES = {
    1: "meow meow galaxy/resources/sprites/platform_sprite/platform_type1",
    2: "meow meow galaxy/resources/sprites/platform_sprite/platform_type2",
    3: "meow meow galaxy/resources/sprites/platform_sprite/platform_type3"
}

BACKGROUND_FRAMES_PATH = "meow meow galaxy/resources/sprites/background_frames/New Piskel (13)"
BACKGROUND_ANIMATION_SPEED = 0.15

SPEEDBOOST_FRAMES_PATH = "meow meow galaxy/resources/sprites/background_frames/speedboost_background"

COIN_SPRITES_PATH = "meow meow galaxy/resources/sprites/coin_sprite"

MAGNET_RADIUS = 450
SPEEDBOOST_DURATION = 300  
MAGNET_SPRITE_PATH = "meow meow galaxy/resources/sprites/powerup_sprites/magnet"
SPEEDBOOST_SPRITE_PATH = "meow meow galaxy/resources/sprites/powerup_sprites/speedboost"

background_frames = []
background_frame_counter = 0
background_current_frame = 0

MENU_BACKGROUND_PATH = "meow meow galaxy/resources/sprites/background_frames/menu_frames"
FLYING_CAT_PATH = "meow meow galaxy/resources/sprites/background_frames/cat_menu"

PLATFORM_BREAK_PATH = "meow meow galaxy/resources/sprites/platform_sprite/platform_type3/broken_platform_sprite_type3"

RAINBOW_BAR_PATH = "meow meow galaxy/resources/sprites/powerup_sprites/rainbow_bar_frames"

TUTORIAL_SLIDES_PATH = "meow meow galaxy/resources/tutorial_slides"

SPRINT_ICON_READY_PATH = "meow meow galaxy/resources/sprites/powerup_sprites/speedboost_shift_icon/sprint_ready/sprint_ready.png"
SPRINT_ICON_COOLDOWN_PATH = "meow meow galaxy/resources/sprites/powerup_sprites/speedboost_shift_icon/sprint_cooldown/sprint_cooldown.png"

sprint_icon_ready = pygame.image.load(SPRINT_ICON_READY_PATH).convert_alpha()
sprint_icon_cooldown = pygame.image.load(SPRINT_ICON_COOLDOWN_PATH).convert_alpha()

SHOP_CAT_PATH = "meow meow galaxy/resources/sprites/skins/shop_cat_sprite"
CLOTHES_PATH = "meow meow galaxy/resources/sprites/skins"

VOLUME_ICON_PATH = "meow meow galaxy/resources/sprites/volume_sprite/volume.png"
volume_icon = pygame.image.load(VOLUME_ICON_PATH).convert_alpha()
volume_icon = pygame.transform.scale(volume_icon, (65, 60)) 

COIN_ICON_PATH = "meow meow galaxy/resources/sprites/coin_sprite/sprite_0.png"
coin_icon = pygame.image.load(COIN_ICON_PATH).convert_alpha()
coin_icon = pygame.transform.scale(coin_icon, (50, 50))

selected_outfit = None
selected_outfit_name = None 
shop_cat_frames = []

SPRINT_ICON_SIZE = (170, 150)
sprint_icon_ready = pygame.transform.scale(sprint_icon_ready, SPRINT_ICON_SIZE)
sprint_icon_cooldown = pygame.transform.scale(sprint_icon_cooldown, SPRINT_ICON_SIZE)

def load_animation_frames(folder_path, scale=None):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
            if scale:
                img = pygame.transform.scale(img, scale)
            frames.append(img)
    return frames

menu_bg_frames = load_animation_frames(MENU_BACKGROUND_PATH, (WIDTH, HEIGHT))
flying_cat_frames = load_animation_frames(FLYING_CAT_PATH, (230, 150))  

def load_powerup_frames(folder_path, size=(110, 120)):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            frame = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
            frame = pygame.transform.scale(frame, size)
            frames.append(frame)
    return frames

magnet_frames = load_powerup_frames(MAGNET_SPRITE_PATH)
speedboost_frames = load_powerup_frames(SPEEDBOOST_SPRITE_PATH)

def load_background_frames():
    frames = []
    if os.path.exists(BACKGROUND_FRAMES_PATH):
        for filename in sorted(os.listdir(BACKGROUND_FRAMES_PATH)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(BACKGROUND_FRAMES_PATH, filename)).convert()
                img = pygame.transform.scale(img, (WIDTH, HEIGHT))
                frames.append(img)
    return frames

background_frames = load_background_frames()

def load_platform_sprites():
    sprites = {}
    for platform_type, folder_path in PLATFORM_SPRITES.items():
        images = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                image = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                images.append(image)
        sprites[platform_type] = images
    return sprites

def load_image_frames(folder_path, scale=None, convert_alpha=True):
    frames = []
    if os.path.exists(folder_path):
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename))
                img = img.convert_alpha() if convert_alpha else img.convert()
                if scale:
                    img = pygame.transform.scale(img, scale)
                frames.append(img)
    return frames

coin_frames = load_image_frames(COIN_SPRITES_PATH)
speedboost_background_frames = load_image_frames(SPEEDBOOST_FRAMES_PATH, scale=(WIDTH, HEIGHT), convert_alpha=False)
platform_break_frames = load_image_frames(PLATFORM_BREAK_PATH)

platform_textures = load_platform_sprites()

rainbow_bar_frames = load_animation_frames(RAINBOW_BAR_PATH, scale=(400, 25))
rainbow_frame_counter = 0

def load_tutorial_slides(folder_path):
    slides = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
            img = pygame.transform.scale(img, screen.get_size())
            slides.append(img)
    return slides

def show_tutorial(slides, sound=None):
    index = 0
    tutorial_active = True

    if sound and os.path.exists(sound):
        slide_sound = pygame.mixer.Sound(sound)
    else:
        slide_sound = None

    while tutorial_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    index = min(index + 1, len(slides) - 1)
                    if slide_sound:
                        slide_sound.play()
                elif event.key == pygame.K_LEFT:
                    index = max(index - 1, 0)
                    if slide_sound:
                        slide_sound.play()
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    tutorial_active = False

        screen.blit(slides[index], (0, 0))
        pygame.display.update()
        clock.tick(60)

def draw_volume_slider(surface, volume):
    icon_rect = volume_icon.get_rect(center=(VOLUME_SLIDER_X - 40, VOLUME_SLIDER_Y + VOLUME_SLIDER_HEIGHT//2))
    surface.blit(volume_icon, icon_rect)
    
    slider_rect = pygame.Rect(VOLUME_SLIDER_X, VOLUME_SLIDER_Y, 
                            VOLUME_SLIDER_WIDTH, VOLUME_SLIDER_HEIGHT)
    pygame.draw.rect(surface, SLIDER_BG_COLOR, slider_rect)
    pygame.draw.rect(surface, SLIDER_BORDER_COLOR, slider_rect, 2)
    
    fill_width = int(VOLUME_SLIDER_WIDTH * volume)
    fill_rect = pygame.Rect(VOLUME_SLIDER_X, VOLUME_SLIDER_Y, 
                           fill_width, VOLUME_SLIDER_HEIGHT)
    pygame.draw.rect(surface, SLIDER_FILL_COLOR, fill_rect)
    
    handle_x = VOLUME_SLIDER_X + int(VOLUME_SLIDER_WIDTH * volume) - VOLUME_HANDLE_WIDTH//2
    handle_rect = pygame.Rect(handle_x, VOLUME_SLIDER_Y - (VOLUME_HANDLE_HEIGHT - VOLUME_SLIDER_HEIGHT)//2,
                            VOLUME_HANDLE_WIDTH, VOLUME_HANDLE_HEIGHT)
    pygame.draw.rect(surface, HANDLE_COLOR, handle_rect)
    pygame.draw.rect(surface, HANDLE_BORDER_COLOR, handle_rect, 2)
    
    return slider_rect

def load_background_frames_from(path):
        frames = []
        for filename in sorted(os.listdir(path)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(path, filename)).convert()
                img = pygame.transform.scale(img, (WIDTH, HEIGHT))
                frames.append(img)
        return frames

def load_shop_cat_animation():
    frames = []
    if os.path.exists(SHOP_CAT_PATH):
        for filename in sorted(os.listdir(SHOP_CAT_PATH)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(SHOP_CAT_PATH, filename)).convert_alpha()
                img = pygame.transform.scale(img, (450, 350))
                frames.append(img)
    return frames

shop_cat_frames = load_shop_cat_animation()
shop_cat_frame_counter = 0
shop_cat_anim_speed = 0.2

outfits = []
if os.path.exists(CLOTHES_PATH):
    for filename in sorted(os.listdir(CLOTHES_PATH)):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(CLOTHES_PATH, filename)).convert_alpha()
            img = pygame.transform.scale(img, (100, 100))
            outfits.append((filename, img))

def preload_outfit_animations():
    """
    Предзагружает анимации для всех костюмов.
    
    Returns:
        dict: Словарь с именами костюмов и их анимациями
    """
    outfit_animations = {}
    for name, _ in outfits:
        folder_name = name.split('.')[0]
        outfit_path = os.path.join(CLOTHES_PATH, folder_name, "run") 
        frames = load_animation_frames(outfit_path, (450, 350))
        outfit_animations[folder_name] = frames
    return outfit_animations

outfit_animations = preload_outfit_animations() 

OUTFIT_PRICES = {
    "bow": 10,
    "clown": 20,
    "conus": 30,
    "cowboy_hat": 40,
    "flower": 50,
    "glass": 50,
    "hat-1": 50,
    "hat-2": 50
}
unlocked_outfits = {"default": True}  

def open_shop():
    """
    Магазин
    - При клике на костюм проверяется, разблокирован ли он (unlocked_outfits).
    - Если костюм заблокирован, отображается его цена (OUTFIT_PRICES).
    """
    global selected_outfit, selected_outfit_name, unlocked_outfits, player
    
    shop_open = True
    shop_cat_frame_counter = 0
    shop_cat_anim_speed = 0.2

    outfit_preview_frames = []
    current_outfit_path = None

    outfit_cell_size = 150
    outfit_margin = 15
    outfit_columns = 3
    outfit_rows = 2
    
    lock_surface = pygame.Surface((outfit_cell_size, outfit_cell_size), pygame.SRCALPHA)
    lock_surface.fill((0, 0, 0, 180))
    
    price_font = pygame.font.Font(font_path, 30)

    while shop_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if selected_outfit_name:
                        player.change_outfit(selected_outfit_name)
                    shop_open = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                for i, (name, img) in enumerate(outfits):
                    col = i % outfit_columns
                    row = i // outfit_columns
                    x = WIDTH - 550 + col * (outfit_cell_size + outfit_margin)
                    y = 100 + row * (outfit_cell_size + outfit_margin)
                    rect = pygame.Rect(x, y, outfit_cell_size, outfit_cell_size)
                    
                    if rect.collidepoint(mouse_x, mouse_y):
                        outfit_folder_name = name.split('.')[0]
                        
                        if unlocked_outfits.get(outfit_folder_name, False):
                            selected_outfit = img
                            selected_outfit_name = outfit_folder_name
                            outfit_preview_frames = load_animation_frames(
                                os.path.join(CLOTHES_PATH, outfit_folder_name, "run"),
                                (450, 350)
                            )
                        else:
                            price = OUTFIT_PRICES.get(outfit_folder_name, 0)
                            if player.coins_collected >= price:
                                player.coins_collected -= price
                                unlocked_outfits[outfit_folder_name] = True
                                selected_outfit_name = outfit_folder_name
                                outfit_preview_frames = load_animation_frames(
                                    os.path.join(CLOTHES_PATH, outfit_folder_name, "run"),
                                    (450, 350)
                                )
                                if outfit_preview_frames:
                                    player.change_outfit(selected_outfit_name)

        screen.fill((120, 120, 120)) 
        cat_x = 150
        cat_y = HEIGHT // 2 - 150

        if outfit_preview_frames:
            shop_cat_frame_counter += shop_cat_anim_speed
            if shop_cat_frame_counter >= len(outfit_preview_frames):
                shop_cat_frame_counter = 0
            cat_img = outfit_preview_frames[int(shop_cat_frame_counter)]
        elif shop_cat_frames:
            shop_cat_frame_counter += shop_cat_anim_speed
            if shop_cat_frame_counter >= len(shop_cat_frames):
                shop_cat_frame_counter = 0
            cat_img = pygame.transform.scale(shop_cat_frames[int(shop_cat_frame_counter)], (450, 350))
        else:
            cat_img = pygame.Surface((400, 300))
            cat_img.fill((255, 0, 255))  

        screen.blit(cat_img, (cat_x, cat_y))

        for i, (name, img) in enumerate(outfits):
            col = i % outfit_columns
            row = i // outfit_columns
            x = WIDTH - 550 + col * (outfit_cell_size + outfit_margin)
            y = 100 + row * (outfit_cell_size + outfit_margin)
            rect = pygame.Rect(x, y, outfit_cell_size, outfit_cell_size)
            
            pygame.draw.rect(screen, (80, 80, 80), rect)
            
            outfit_folder_name = name.split('.')[0]
            if outfit_folder_name == selected_outfit_name:
                pygame.draw.rect(screen, (255, 255, 0), rect, 4)
            else:
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            
            screen.blit(pygame.transform.scale(img, (outfit_cell_size, outfit_cell_size)), (x, y))
            
            if not unlocked_outfits.get(outfit_folder_name, False):
                screen.blit(lock_surface, (x, y))
                
                price = OUTFIT_PRICES.get(outfit_folder_name, 0)
                price_text = price_font.render(f"{price}", True, (255, 223, 0))
                price_rect = price_text.get_rect(center=(x + outfit_cell_size//2, y + outfit_cell_size//2))
                screen.blit(price_text, price_rect)
                
                coin_icon_small = pygame.transform.scale(coin_icon, (30, 30))
                screen.blit(coin_icon_small, (price_rect.right + 5, price_rect.y - 5))

        screen.blit(coin_icon, (30, 30))
        coin_count_text = font.render(str(player.coins_collected), True, (255, 255, 255))
        screen.blit(coin_count_text, (90, 40))

        instruction_text = font.render("Кликните на предмет, чтобы купить", True, (255, 255, 255))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)


class Camera:
    def __init__(self, target):
        self.target = target
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        self.offset_x = self.target.rect.centerx - WIDTH // 2
        self.offset_y = self.target.rect.centery - HEIGHT // 2

    def apply(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = {
            "run": [],
            "jump": [],
            "fall": [],
            "speed": []
        }
        self.state = "run"
        self.current_frame = 0
        self.animation_speed = 0.23
        self.frame_counter = 0
        self.speed_mode = False

        self.load_animations()

        if self.speed_mode and self.state == "run" and "speed" in self.animations and self.animations["speed"]:
            self.image = self.animations["speed"][self.current_frame]
        elif self.animations[self.state]:
            self.image = self.animations[self.state][self.current_frame]

        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT // 2
        self.vel_y = 0
        self.jump_count = 0
        self.base_speed = PLAYER_SPEED    
        self.speed = self.base_speed
        self.fall_timer = 0
        self.FALL_DELAY = 27
        self.coins_collected = 0  

        self.magnet_active = False
        self.speedboost_active = False
        self.magnet_timer = 0
        self.speedboost_timer = 0

        self.fly_mode = False
        self.fly_cooldown = 1200  
        self.fly_timer = 0
        self.fly_background = load_background_frames_from("meow meow galaxy/resources/sprites/background_frames/shift_speedboost_background")
        self.fly_animation = self.load_custom_animation("fly", "meow meow galaxy/resources/sprites/background_frames/cat_menu")

    def load_animations(self):
        """Загружает все анимации с учетом выбранного костюма"""
        if selected_outfit_name:
            # Пути к папкам с анимациями для выбранного костюма
            base_path = os.path.join(CLOTHES_PATH, selected_outfit_name)
            run_path = os.path.join(base_path, "run")
            jump_path = os.path.join(base_path, "jump")
            fall_path = os.path.join(base_path, "fall")
            speed_path = os.path.join(base_path, "speed")
        else:
            # Стандартные пути, если костюм не выбран
            run_path = "meow meow galaxy/resources/sprites/skins/shop_cat_sprite"
            jump_path = "meow meow galaxy/resources/sprites/cat_sprite/cat_jump/cat_jump"
            fall_path = "meow meow galaxy/resources/sprites/cat_sprite/cat_fall/cat_fall"
            speed_path = "meow meow galaxy/resources/sprites/cat_sprite/cat_speed/cat_speed"

        self.load_animation_frames("run", run_path)
        self.load_animation_frames("jump", jump_path)
        self.load_animation_frames("fall", fall_path)
        self.load_animation_frames("speed", speed_path)

    def load_animation_frames(self, state_name, folder_path):
        """
        Загружает кадры анимации из папки:
        - convert_alpha() — для корректной работы с прозрачностью PNG.
        - scale — опциональное масштабирование кадров.
        - Возвращает пустой список, если папка не существует.
        """
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                frame = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
                frames.append(frame)

            
            if state_name == "jump":
                default_path = "meow meow galaxy/resources/sprites/cat_sprite/cat_jump/cat_jump"
            elif state_name == "fall":
                default_path = "meow meow galaxy/resources/sprites/cat_sprite/cat_fall/cat_fall"
            elif state_name == "speed":
                default_path = "meow meow galaxy/resources/sprites/cat_sprite/cat_speed/cat_speed"
            else:  
                default_path = "meow meow galaxy/resources/sprites/skins/shop_cat_sprite"

        self.animations[state_name] = frames

    def load_custom_animation(self, state_name, folder_path):
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                frame = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
                frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
                frames.append(frame)
        return frames

    def update(self):
        """
        Обновляет состояние игрока:
        - Переключение анимаций (run/jump/fall) на основе скорости vel_y.
        - Режим полёта (fly_mode) активируется на 1200 кадров (20 сек при 60 FPS).
        - FALL_DELAY = 27 — задержка перед переходом в анимацию падения.
        - Магнит и ускорение (speedboost) имеют таймеры длительностью SPEEDBOOST_DURATION.
        """
        if self.vel_y < -2:
            self.state = "jump"
            self.fall_timer = 0
        elif self.vel_y > 2:
            self.fall_timer += 1
            if self.fall_timer >= self.FALL_DELAY:
                self.state = "fall"
        else:
            self.state = "run"
            self.fall_timer = 0

        if self.animations[self.state]:
            self.frame_counter += self.animation_speed
            if self.frame_counter >= len(self.animations[self.state]):
                self.frame_counter = 0
            self.current_frame = int(self.frame_counter)
            
            if self.speed_mode and "speed" in self.animations and self.animations["speed"]:
                self.image = self.animations["speed"][self.current_frame]
            else:
                self.image = self.animations[self.state][self.current_frame]

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.speedboost_active:
            self.speedboost_timer -= 1
            if self.speedboost_timer <= 0:
                self.speedboost_active = False
                self.speed = self.base_speed
                self.speed_mode = False
        elif not self.fly_mode:
            self.speed = min(self.speed + PLAYER_ACCELERATION, PLAYER_MAX_SPEED)

        self.rect.x += self.speed

        if self.magnet_active:
            self.magnet_timer -= 1
        if self.magnet_timer <= 0:
            self.magnet_active = False
        
        if self.fly_mode:
            keys = pygame.key.get_pressed()
            self.vel_y = 0
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.rect.y -= 12
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.rect.y += 12

            self.speed = PLAYER_MAX_SPEED + 20
            self.speed_mode = True

            self.fly_timer -= 1
            if self.fly_timer <= self.fly_cooldown - 180:
                self.fly_mode = False
                self.speed_mode = False
        else:
            if self.fly_timer > 0:
                self.fly_timer -= 1

        PLAYER_DEATH_HEIGHT_MULTIPLIER = 2
        if self.rect.top > HEIGHT * PLAYER_DEATH_HEIGHT_MULTIPLIER:
            main_menu()

    def jump(self):
        if self.jump_count < MAX_JUMPS:
            self.vel_y = JUMP_STRENGTH
            self.jump_count += 1
            self.state = "jump"
            self.fall_timer = 0

    def land(self):
        self.jump_count = 0
        self.vel_y = 0
        self.fall_timer = 0

    def activate_powerup(self, power_type):
        if power_type == "magnet":
            self.magnet_active = True
            self.magnet_timer = SPEEDBOOST_DURATION
        elif power_type == "speed":
            if not self.speedboost_active:
                self.speedboost_active = True
                Increasing_speed = 16
                self.speed = PLAYER_MAX_SPEED + Increasing_speed
                self.speedboost_timer = SPEEDBOOST_DURATION
                self.speed_mode = True
    
    def change_outfit(self, outfit_name):
        global selected_outfit_name
        selected_outfit_name = outfit_name
        self.load_animations()
        self.frame_counter = 0
        self.current_frame = 0

    def activate_fly_mode(self):
        if self.fly_timer <= 0:
            self.fly_mode = True
            self.fly_timer = self.fly_cooldown
            self.vel_y = 0


class Platform(pygame.sprite.Sprite):
    """Класс платформы, по которым перемещается игрок."""
    def __init__(self, x, y, platform_type):
        """
        Инициализирует платформу с указанными параметрами.
        
        Args:
            x (int): Координата X платформы
            y (int): Координата Y платформы
            platform_type (int): Тип платформы (1, 2 или 3)
        """
        super().__init__()
        self.platform_type = platform_type
        self.images = platform_textures[platform_type] or []
        width = random.choice(PLATFORM_WIDTHS)
        if self.images:
            self.image = pygame.transform.scale(random.choice(self.images), (width, PLATFORM_HEIGHT))

        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width

        self.broken = False
        self.break_timer = 0
        self.break_delay = 15
        self.breaking = False

        self.break_frames = platform_break_frames.copy()
        self.break_frame_index = 0
        self.break_anim_speed = 0.75
        self.break_anim_counter = 0


    def start_breaking(self):
        """Запускает анимацию разрушения платформы."""
        self.breaking = True
        self.break_timer = pygame.time.get_ticks()
        self.break_frame_index = 0
        self.break_anim_counter = 0

    def update(self):
        """Обновляет состояние платформы (анимацию разрушения)."""
        if self.breaking:
            if self.break_frames:
                self.break_anim_counter += self.break_anim_speed
                if self.break_anim_counter >= 1:
                    self.break_anim_counter = 0
                    self.break_frame_index += 1
                    if self.break_frame_index < len(self.break_frames):
                        frame = pygame.transform.scale(self.break_frames[self.break_frame_index], (self.width, PLATFORM_HEIGHT))
                        self.image = frame
                    else:
                        self.broken = True
                        self.kill()
            else:
                now = pygame.time.get_ticks()
                if now - self.break_timer >= self.break_delay:
                    self.broken = True
                    self.kill()


class Coin(pygame.sprite.Sprite):
    """Класс монеты, которую может собрать игрок."""
    def __init__(self, x, y):
        """
        Инициализирует монету с указанными координатами.
        
        Args:
            x (int): Координата X монеты
            y (int): Координата Y монеты
        """
        super().__init__()
        COIN_SIZE = (70, 70)  

        self.frames = [pygame.transform.scale(frame, COIN_SIZE) for frame in coin_frames]
        self.current_frame = 0
        self.animation_speed = 0.25
        self.frame_counter = 0

        if self.frames:
            self.image = self.frames[0]
        else:
            self.image = pygame.Surface(COIN_SIZE, pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 223, 0), (COIN_SIZE[0] // 2, COIN_SIZE[1] // 2), COIN_SIZE[0] // 2)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        """Обновляет анимацию монеты."""
        if not self.frames:
            return
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.frames):
            self.frame_counter = 0
        self.current_frame = int(self.frame_counter)
        self.image = self.frames[self.current_frame]

# Минимальное расстояние между платформами по X (чтобы не спавнились слишком близко)
min_dist_x = [650, 750]
min_dist_y = 200

class PowerUp(pygame.sprite.Sprite):
    """Класс бонуса, который может подобрать игрок."""
    def __init__(self, x, y, frames, power_type):
        """
        Инициализирует бонус с указанными параметрами.
        
        Args:
            x (int): Координата X бонуса
            y (int): Координата Y бонуса
            frames (list): Кадры анимации бонуса
            power_type (str): Тип бонуса ("magnet" или "speed")
        """
        super().__init__()
        self.frames = frames
        self.power_type = power_type
        self.current_frame = 0
        self.animation_speed = 0.2
        self.frame_counter = 0

        self.image = self.frames[0] if frames else pygame.Surface((60, 60))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if not self.frames:
            return
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.frames):
            self.frame_counter = 0
        self.current_frame = int(self.frame_counter)
        self.image = self.frames[self.current_frame]

def generate_platforms(platforms, player_x):
    """
    Генерирует новые платформы, учитывая:
    - Минимальные расстояния между ними (min_dist_x, min_dist_y).
    - Вероятность появления платформы (80%).
    - Типы платформ: 
      1 (обычная) — 50%, 2 (прыгучая) — 30%, 3 (ломающаяся) — 20%.
    - Расположение монет и power-ups на платформах.
    """
    max_x = max([p.rect.x for p in platforms]) if platforms else 0
    while max_x < player_x + WIDTH * 2:
        for _ in range(30):
            x = max_x + PLATFORM_GAP_X
            y = random.randint(-600, HEIGHT + 300)

            if random.random() < 0.8:
                too_close = False
                for p in platforms:
                    dx = abs(p.rect.x - x)
                    dy = abs(p.rect.y - y)
                    if dx < random.choice(min_dist_x) and dy < min_dist_y:
                        too_close = True
                        break

                if not too_close:
                    # Генерируются определенный тип платформы 
                    # Обычная (1) - 50%, прыгучая (2) - 30%, ломающаяся (3) - 20%
                    platform_type = random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2])[0]
                    platform = Platform(x, y, platform_type)
                    platform_group.add(platform)
                    platforms.append(platform)

                    if random.random() < 0.4:
                        coin_count = random.randint(2, 3)
                        spacing = (platform.width - 40) / (coin_count - 1) if coin_count > 1 else 0
                        for i in range(coin_count):
                            coin_x = x + 20 + spacing * i
                            coin_y = y - 50
                            coin = Coin(coin_x, coin_y)
                            coin_group.add(coin)
                    
                    if random.random() < 0.08:  
                        power_type = random.choice(["magnet", "speed"])
                        frames = magnet_frames if power_type == "magnet" else speedboost_frames
                        powerup = PowerUp(x + platform.width // 2, y - 70, frames, power_type)
                        powerup_group.add(powerup)


        max_x += PLATFORM_GAP_X

player = Player()
player_group = pygame.sprite.Group(player)
platform_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
camera = Camera(player)
powerup_group = pygame.sprite.Group()

platforms = []
generate_platforms(platforms, player.rect.x)

start_platform = min(platforms, key=lambda p: abs(p.rect.x - player.rect.x))
player.rect.bottom = start_platform.rect.top
player.rect.centerx = start_platform.rect.centerx
player.vel_y = 0
player.jump_count = 0

pygame.mixer.init()
pygame.mixer.music.load("meow meow galaxy/resources/music/Nyan Cat Remix.mp3")
pygame.mixer.music.play(-1)

font_path = "meow meow galaxy/resources/fonts/font_regular/EpilepsySans.ttf"
font_path_bold = "meow meow galaxy/resources/fonts/font_bold/EpilepsySansBold.ttf"
font = pygame.font.Font(font_path, 40)  
btn_font = pygame.font.Font(font_path, 50)
pause_font = pygame.font.Font(font_path, 70)

def draw_text(text, font, color, surface, x, y):
    """
    Рисует текст на указанной поверхности.
    
    Args:
        text (str): Текст для отображения
        font (pygame.font.Font): Шрифт для текста
        color (tuple): Цвет текста (R, G, B)
        surface (pygame.Surface): Поверхность для отрисовки
        x (int): Координата X центра текста
        y (int): Координата Y центра текста
    
    Returns:
        pygame.Rect: Прямоугольник, занимаемый текстом
    """
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
    return textrect

tutorial_shown = False

def main_menu():
    """Отображает главное меню игры и обрабатывает взаимодействие с пользователем."""
    global tutorial_shown
    menu = True
    menu_font = pygame.font.Font(font_path_bold, 80) 
    btn_font = pygame.font.Font(font_path, 65)
    title_color = (255, 255, 255)
    btn_color = (180, 180, 255)
    btn_hover = (255, 255, 255)

    current_volume = pygame.mixer.music.get_volume()
    dragging_volume = False
                                  
    bg_frame_counter = 0
    bg_animation_speed = 0.15

    cat_active = False
    cat_timer = 0
    cat_frame_counter = 0
    cat_animation_speed = 0.2
    flying_cat_pos = [0, 0]
    flying_cat_direction = 1  

    while menu:
        if menu_bg_frames:
            bg_frame_counter += bg_animation_speed
            if bg_frame_counter >= len(menu_bg_frames):
                bg_frame_counter = 0
            bg_frame = menu_bg_frames[int(bg_frame_counter)]

            current_width, current_height = screen.get_size()
            bg_scaled = pygame.transform.scale(bg_frame, (current_width, current_height))
            screen.blit(bg_scaled, (0, 0))
        else:
            screen.fill((10, 10, 50))  

        if not cat_active and random.random() < 0.005:  
            cat_active = True
            flying_cat_direction = random.choice([-1, 1])
            if flying_cat_direction == 1:
                flying_cat_pos = [-160, random.randint(100, HEIGHT - 150)]
            else:
                flying_cat_pos = [WIDTH + 160, random.randint(100, HEIGHT - 150)]
            cat_timer = 0

        if cat_active and flying_cat_frames:
            cat_frame_counter += cat_animation_speed
            if cat_frame_counter >= len(flying_cat_frames):
                cat_frame_counter = 0
            cat_image = flying_cat_frames[int(cat_frame_counter)]
            if flying_cat_direction == -1:
                cat_image = pygame.transform.flip(cat_image, True, False)
            screen.blit(cat_image, flying_cat_pos)

            flying_cat_pos[0] += 10 * flying_cat_direction
            cat_timer += 1
            if (flying_cat_direction == 1 and flying_cat_pos[0] > WIDTH + 160) or \
               (flying_cat_direction == -1 and flying_cat_pos[0] < -160):
                cat_active = False
    
        mouse_pos = pygame.mouse.get_pos()
        click = False
        mouse_pressed = pygame.mouse.get_pressed()[0]

        button_width, button_height = 300, 60
        button_gap = 80  
        start_y = HEIGHT // 2 - button_gap

        volume_slider_rect = draw_volume_slider(screen, current_volume)
        
        if mouse_pressed:
            if volume_slider_rect.collidepoint(mouse_pos):
                dragging_volume = True
        else:
            dragging_volume = False
            
        if dragging_volume:
            relative_x = mouse_pos[0] - VOLUME_SLIDER_X
            # Учитываем границы экрана при расчёте громкости, чтобы не выйти за 0-1
            current_volume = max(0.0, min(1.0, relative_x / VOLUME_SLIDER_WIDTH))
            pygame.mixer.music.set_volume(current_volume)

        title_text = draw_text("Meow Meow Galaxy", menu_font, title_color, screen, WIDTH // 2, HEIGHT // 2 - 150)
        start_btn = draw_text("Начать игру", btn_font, btn_hover if pygame.Rect(WIDTH//2 - button_width//2, start_y, button_width, button_height).collidepoint(mouse_pos) else btn_color, screen, WIDTH // 2, start_y + button_height // 2)
        shop_btn = draw_text("Магазин", btn_font, btn_hover if pygame.Rect(WIDTH//2 - button_width//2, start_y + button_gap, button_width, button_height).collidepoint(mouse_pos) else btn_color, screen, WIDTH // 2, start_y + button_gap + button_height // 2)
        quit_btn = draw_text("Выход", btn_font, btn_hover if pygame.Rect(WIDTH//2 - button_width//2, start_y + button_gap * 2, button_width, button_height).collidepoint(mouse_pos) else btn_color, screen, WIDTH // 2, start_y + button_gap * 2 + button_height // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
            if event.type == pygame.K_ESCAPE:
                paused = True
                pause_menu()
                paused = False
            if shop_btn.collidepoint(mouse_pos) and click:
                open_shop()
        
        if start_btn.collidepoint(mouse_pos) and click:
            if not tutorial_shown:
                tutorial_slides = load_tutorial_slides(TUTORIAL_SLIDES_PATH)
                show_tutorial(tutorial_slides)
                tutorial_shown = True
            menu = False
        
        screen.blit(coin_icon, (30, 30)) 
        coin_count_text = font.render(str(player.coins_collected), True, (255, 255, 255))
        screen.blit(coin_count_text, (100, 35))

        if start_btn.collidepoint(mouse_pos) and click:
            menu = False
        if quit_btn.collidepoint(mouse_pos) and click:
            pygame.quit()
            exit()

        pygame.display.update()
        clock.tick(60)  

main_menu()

def pause_menu():
    """Отображает меню паузы и обрабатывает взаимодействие с пользователем."""
    pause_font = pygame.font.Font(font_path, 70)
    btn_font = pygame.font.Font(font_path, 60)
    btn_color = (180, 180, 255)
    btn_hover = (255, 255, 255)

    current_volume = pygame.mixer.music.get_volume()
    dragging_volume = False

    while True:
        screen.fill((30, 30, 60))

        mouse_pos = pygame.mouse.get_pos()
        click = False
        mouse_pressed = pygame.mouse.get_pressed()[0]

        volume_slider_rect = draw_volume_slider(screen, current_volume)
        
        if mouse_pressed:
            if volume_slider_rect.collidepoint(mouse_pos):
                dragging_volume = True
        else:
            dragging_volume = False
            
        if dragging_volume:
            relative_x = mouse_pos[0] - VOLUME_SLIDER_X
            current_volume = max(0.0, min(1.0, relative_x / VOLUME_SLIDER_WIDTH))
            pygame.mixer.music.set_volume(current_volume)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  

        continue_btn = draw_text("Продолжить", btn_font, btn_hover if pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 300, 60).collidepoint(mouse_pos) else btn_color, screen, WIDTH // 2, HEIGHT // 2)
        menu_btn = draw_text("Выйти в меню", btn_font, btn_hover if pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 100, 300, 60).collidepoint(mouse_pos) else btn_color, screen, WIDTH // 2, HEIGHT // 2 + 100)

        if continue_btn.collidepoint(mouse_pos) and click:
            return
        if menu_btn.collidepoint(mouse_pos) and click:
            main_menu()
            return

        pygame.display.update()
        clock.tick(60)

paused = False
running = True
while running:

    background_frame_counter += BACKGROUND_ANIMATION_SPEED
    if player.fly_mode and player.fly_background:
        background_current_frame = int(background_frame_counter % len(player.fly_background))
        bg_img = player.fly_background[background_current_frame]
    elif player.speedboost_active and speedboost_background_frames:
        if background_frame_counter >= len(speedboost_background_frames):
            background_frame_counter = 0
        background_current_frame = int(background_frame_counter)
        bg_img = speedboost_background_frames[background_current_frame]
    else:
        if background_frame_counter >= len(background_frames):
            background_frame_counter = 0
        background_current_frame = int(background_frame_counter)
        bg_img = background_frames[background_current_frame]


    for i in range(-1, (WIDTH // bg_img.get_width()) + 2):
        for j in range(-1, (HEIGHT // bg_img.get_height()) + 2):
            screen.blit(bg_img, (
                i * bg_img.get_width() - camera.offset_x % bg_img.get_width(),
                j * bg_img.get_height() - camera.offset_y % bg_img.get_height()
            ))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_ESCAPE:
                paused = True
                pause_menu()
                paused = False
            elif event.key == pygame.K_LSHIFT:
                player.activate_fly_mode()


    player_group.update()
    coin_group.update()
    camera.update()
    powerup_group.update()
    generate_platforms(platforms, player.rect.x)

    if not player.fly_mode:
        for platform in platform_group:
            if platform.broken:
                continue
            
            # Проверка столкновения с платформой:
            # '+ 10' — небольшой допуск, чтобы персонаж не залипал на краю платформы.
            if player.vel_y > 0 and player.rect.colliderect(platform.rect) and \
            player.rect.bottom - player.vel_y <= platform.rect.top + 10:

                player.rect.bottom = platform.rect.top
                player.land()

                if platform.platform_type == 2:
                    player.vel_y = JUMP_STRENGTH * 1.3

                elif platform.platform_type == 3:
                    if not platform.breaking:
                        platform.start_breaking()


    platform_group.update()
    
    if player.magnet_active:
        for coin in coin_group:
            dist = pygame.math.Vector2(coin.rect.center) - pygame.math.Vector2(player.rect.center)
            if dist.length() < MAGNET_RADIUS:
                direction = (player.rect.centerx - coin.rect.centerx, player.rect.centery - coin.rect.centery)
                # Магнит притягивает монеты с разной скоростью по X (0.25) и Y (0.18)
                coin.rect.move_ip(direction[0] * 0.25, direction[1] * 0.18)

    collected_powerups = pygame.sprite.spritecollide(player, powerup_group, False)
    for p in collected_powerups:
        if p.power_type == "speed" and player.fly_mode:
            continue  
        player.activate_powerup(p.power_type)
        p.kill()


    for platform in platform_group:
        if player.rect.colliderect(platform.rect) and player.vel_y > 0:
            if player.rect.bottom <= platform.rect.top + 20:
                player.rect.bottom = platform.rect.top
                player.land()
                break

    collected_coins = pygame.sprite.spritecollide(player, coin_group, True)
    if collected_coins:
        player.coins_collected += len(collected_coins)

    if player.fly_mode and player.fly_background:
        background_frame_counter += BACKGROUND_ANIMATION_SPEED
        background_current_frame = int(background_frame_counter % len(player.fly_background))
        bg_img = player.fly_background[background_current_frame]

    for sprite in platform_group:
        screen.blit(sprite.image, camera.apply(sprite.rect))
    for sprite in coin_group:
        screen.blit(sprite.image, camera.apply(sprite.rect))
    for sprite in player_group:
        screen.blit(sprite.image, camera.apply(sprite.rect))

    screen.blit(coin_icon, (30, 30))

    coin_count_text = font.render(str(player.coins_collected), True, (255, 255, 255))
    screen.blit(coin_count_text, (90, 40))  


    for sprite in powerup_group:
        screen.blit(sprite.image, camera.apply(sprite.rect))

    if player.speedboost_active:
        bar_width = 400
        remaining_ratio = player.speedboost_timer / SPEEDBOOST_DURATION
        current_width = int(bar_width * remaining_ratio)
        bar_height = 20
        if rainbow_bar_frames:
            # Анимация радужной полосы:
            # - remaining_ratio — отношение оставшегося времени ускорения к SPEEDBOOST_DURATION.
            # - rainbow_frame_counter += 0.3 — скорость анимации (чем больше, тем быстрее).
            rainbow_frame_counter += 0.3
            if rainbow_frame_counter >= len(rainbow_bar_frames):
                rainbow_frame_counter = 0
            rainbow_img = rainbow_bar_frames[int(rainbow_frame_counter)]

            total_width = 400
            remaining_ratio = player.speedboost_timer / SPEEDBOOST_DURATION
            current_width = int(total_width * remaining_ratio)

            if current_width > 0:
                rainbow_cropped = rainbow_img.subsurface((0, 0, current_width, 25))
                screen.blit(rainbow_cropped, (WIDTH // 2 - total_width // 2, 20))

    if player.fly_timer <= 0:
        sprint_icon = sprint_icon_ready
    else:
        sprint_icon = sprint_icon_cooldown

    icon_margin = 60
    screen.blit(sprint_icon, (icon_margin, HEIGHT - SPRINT_ICON_SIZE[1] - icon_margin))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()