from random import randint
from pygame import *

# Инициализация
font.init()
mixer.init()

# Константы
WIN_WIDTH = 1200
WIN_HEIGHT = 700
MAX_LOST = 3
GOAL = 15
PLAYER_SPEED = 7
ENEMY_SPEED = 2
BULLET_SPEED = -15
ASTEROID_SPEED = 2
MAX_BULLETS = 10
RELOAD_COOLDOWN = 60  # 1 секунда (60 FPS)

# Цвета
WHITE = (255, 255, 255)
RED = (180, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)

# Шрифты
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)

# Тексты
win_text = font1.render('YOU WIN!!!', True, WHITE)
lose_text = font1.render('YOU LOST!', True, RED)
restart_text = font2.render('RESTART', True, WHITE)
reload_text = font2.render('RELOADING...', True, GOLD)

# Кнопка рестарта
restart_btn = Rect(WIN_WIDTH//2 - 100, WIN_HEIGHT//2 + 100, 200, 50)

# Звуки
mixer.music.load('space.ogg')
mixer.music.play(-1)  # -1 означает бесконечное повторение
fire_sound = mixer.Sound('fire.ogg')

# Изображения
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.bullets_left = MAX_BULLETS
        self.can_reload = True
        self.reload_timer = 0
    
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < WIN_WIDTH - 80:
            self.rect.x += self.speed
        
        if self.reload_timer > 0:
            self.reload_timer -= 1
        elif not self.can_reload:
            self.can_reload = True
    
    def fire(self):
        if self.bullets_left > 0:
            fire_sound.play()
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, BULLET_SPEED)
            bullets.add(bullet)
            self.bullets_left -= 1
            return True
        return False
    
    def reload(self):
        if self.can_reload and self.bullets_left < MAX_BULLETS:
            self.can_reload = False
            self.reload_timer = RELOAD_COOLDOWN
            self.bullets_left = MAX_BULLETS
            return True
        return False

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > WIN_HEIGHT:
            self.reinit()
            global lost
            lost += 1
    
    def reinit(self):
        self.rect.x = randint(80, WIN_WIDTH - 80)
        self.rect.y = -40

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > WIN_HEIGHT:
            self.reinit()
    
    def reinit(self):
        self.rect.x = randint(80, WIN_WIDTH - 80)
        self.rect.y = -40

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

def init_game():
    global ship, monsters, asteroids, bullets, score, lost, finish
    
    ship = Player(img_hero, 5, WIN_HEIGHT - 110, 80, 100, PLAYER_SPEED)
    
    monsters = sprite.Group()
    for _ in range(5):
        monster = Enemy(img_enemy, randint(80, WIN_WIDTH - 80), -40, 80, 50, ENEMY_SPEED)
        monsters.add(monster)
    
    asteroids = sprite.Group()
    for _ in range(2):
        asteroid = Asteroid(img_asteroid, randint(80, WIN_WIDTH - 80), -40, 80, 50, ASTEROID_SPEED)
        asteroids.add(asteroid)
    
    bullets = sprite.Group()
    score = 0
    lost = 0
    finish = False

# Основной код
window = display.set_mode((WIN_WIDTH, WIN_HEIGHT))
display.set_caption("Space Shooter")
background = transform.scale(image.load(img_back), (WIN_WIDTH, WIN_HEIGHT))

init_game()

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                if ship.bullets_left > 0:
                    ship.fire()
                else:
                    ship.reload()
        elif e.type == MOUSEBUTTONDOWN and e.button == 1 and finish:
            if restart_btn.collidepoint(e.pos):
                init_game()
    
    # Проверяем, играет ли музыка, и перезапускаем если нет
    if not mixer.music.get_busy():
        mixer.music.play()
    
    if not finish:
        window.blit(background, (0, 0))
        
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        text_score = font2.render(f'Score: {score}', 1, WHITE)
        text_lost = font2.render(f'Missed: {lost}', 1, WHITE)
        text_ammo = font2.render(f'Ammo: {ship.bullets_left}/{MAX_BULLETS}', 1, WHITE)
        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 50))
        window.blit(text_ammo, (10, 80))
        
        if ship.reload_timer > 0:
            window.blit(reload_text, (WIN_WIDTH - 200, 20))
        
        colides = sprite.groupcollide(monsters, bullets, True, True)
        for _ in colides:
            score += 1
            monster = Enemy(img_enemy, randint(80, WIN_WIDTH - 80), -40, 80, 50, ENEMY_SPEED)
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or lost >= MAX_LOST:
            finish = True
        elif score >= GOAL:
            finish = True
            window.blit(win_text, (WIN_WIDTH//2-150, WIN_HEIGHT//2-40))
    else:
        window.blit(background, (0, 0))
        if score >= GOAL:
            window.blit(win_text, (WIN_WIDTH//2-150, WIN_HEIGHT//2-40))
        else:
            window.blit(lose_text, (WIN_WIDTH//2-150, WIN_HEIGHT//2-40))
        
        # Рисуем кнопку рестарта
        draw.rect(window, BLUE, restart_btn)
        window.blit(restart_text, (restart_btn.x + 50, restart_btn.y + 10))
    
    display.update()
    time.delay(25)

quit()