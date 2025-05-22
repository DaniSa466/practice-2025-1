# Документация

- Папка для размещения документации по практике в формате Markdown.
- README.md — основной файл с документацией, описывающий процесс выполнения практики.
- При необходимости могут добавляться дополнительные файлы Markdown.

# Выполнение базовой части
Выполнен статический веб-сайт о проекте Ecollapse. Верстка была выполнена с помощью языков разметки HTML и CSS. Подробная документация о создании сайта находится в репозитории.

## Сайт включает три основные вкладки:
- Главная страница (общая информация, новости, кратко о проекте)
- Новости (лента последних обновлений)
- О проекте (цели, концепт, техническое решение, команда)
# Структура и функционал сайта
## Главная страница
- Название игры 
- Блок с последними новостями
### Вкладка "Новости"
- Полный список новостей в хронологическом порядке
### Вкладка "О проекте"
- Цели проекта
- Концепт 
- Техническое решение
- Команда разработчиков

## Дизайн и визуальная часть
- Цветовая схема: черный фон + оранжевые акценты (текст, кнопки, рамки)
- Шрифты: Montserrat
## Техническая реализация
- Frontend: HTML5, CSS3

# Выполнение вариативной части
1. Архитектура проекта
Код использует объектно-ориентированный подход с наследованием классов. Основные компоненты:

python
class GameSprite(sprite.Sprite):  # Базовый класс для всех объектов
class Player(GameSprite):        # Класс игрока
class Enemy(GameSprite):         # Класс врагов
class Asteroid(GameSprite):      # Класс астероидов 
class Bullet(GameSprite):        # Класс пуль
2. Основные игровые механики
Движение игрока:

python
def update(self):
    keys = key.get_pressed()
    if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 5:
        self.rect.x -= self.speed
    if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < WIN_WIDTH - 80:
        self.rect.x += self.speed
Управление стрелками или WASD

Проверка границ экрана

Система стрельбы:

python
def fire(self):
    if self.bullets_left > 0:
        fire_sound.play()
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, BULLET_SPEED)
        bullets.add(bullet)
        self.bullets_left -= 1
Ограниченный боезапас (MAX_BULLETS = 10)

Визуализация и звук выстрела

Перезарядка:

python
def reload(self):
    if self.can_reload and self.bullets_left < MAX_BULLETS:
        self.can_reload = False
        self.reload_timer = RELOAD_COOLDOWN  # 60 кадров = 1 секунда
        self.bullets_left = MAX_BULLETS
Активация по пробелу

Визуальный индикатор перезарядки

3. Игровой цикл
Основные этапы:

Обработка ввода:

python
for e in event.get():
    if e.type == KEYDOWN:
        if e.key == K_SPACE:
            if ship.bullets_left > 0:
                ship.fire()
            else:
                ship.reload()
Обновление состояния:

python
ship.update()
monsters.update()
bullets.update()
asteroids.update()
Отрисовка:

python
window.blit(background, (0, 0))
ship.reset()
monsters.draw(window)
# ... остальная отрисовка
Проверка столкновений:

python
colides = sprite.groupcollide(monsters, bullets, True, True)
for _ in colides:
    score += 1
    # Создание нового врага
4. Особенности реализации
Музыкальный движок:

python
mixer.music.load('space.ogg')
mixer.music.play(-1)  # Бесконечное повторение
if not mixer.music.get_busy():  # Защита от остановки
    mixer.music.play()
Система перезапуска:

python
def init_game():  # Полная реинициализация игры
    global ship, monsters, bullets, score, lost
    ship = Player(...)
    monsters = sprite.Group()
    # ... создание новых объектов
    score = 0
    lost = 0
Интерфейс:

python
# Отображение счётчиков
text_score = font2.render(f'Score: {score}', 1, WHITE)
text_ammo = font2.render(f'Ammo: {ship.bullets_left}/{MAX_BULLETS}', 1, WHITE)

# Кнопка рестарта
draw.rect(window, BLUE, restart_btn)
window.blit(restart_text, (restart_btn.x + 50, restart_btn.y + 10))
5. Оптимизации
Группы спрайтов для эффективного управления:

python
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
Повторное использование объектов врагов:

python
def reinit(self):  # Вместо удаления/создания
    self.rect.x = randint(80, WIN_WIDTH - 80)
    self.rect.y = -40
Единый игровой цикл с фиксированным FPS:

python
clock = pygame.time.Clock()
while running:
    clock.tick(60)  # 60 FPS
Полный код представляет собой законченное игровое решение с:

Плавным управлением

Балансом сложности

Понятным интерфейсом

Системой перезапуска

Визуальной и звуковой обратной связью

Для дальнейшего развития проекта можно добавить систему уровней, различные типы оружия и бонусы.
