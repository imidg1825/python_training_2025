import pygame
import random
import sys
import os

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический защитник - Улучшенная графика")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Создаем папку для изображений, если её нет
if not os.path.exists('images'):
    os.makedirs('images')

# Функция для загрузки изображения (с созданием заглушки, если нет файла)
def load_image(name, width, height, color=None):
    try:
        # Пытаемся загрузить реальное изображение
        image = pygame.image.load(f'images/{name}').convert_alpha()
        return pygame.transform.scale(image, (width, height))
    except:
        # Создаем красивое изображение программно
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        if name == 'player.png':
            # Корабль игрока
            points = [(0, height), (width//2, 0), (width, height)]
            pygame.draw.polygon(surface, (0, 255, 0), points)
            pygame.draw.polygon(surface, (100, 255, 100), points, 2)
            
        elif name == 'asteroid.png':
            # Астероид - неровный круг
            pygame.draw.circle(surface, (150, 75, 0), (width//2, height//2), width//2)
            # Добавляем неровности
            for i in range(8):
                angle = random.uniform(0, 6.28)
                dist = random.uniform(width//3, width//2)
                x = width//2 + dist * pygame.math.Vector2(1, 0).rotate(angle * 57.3).x
                y = height//2 + dist * pygame.math.Vector2(1, 0).rotate(angle * 57.3).y
                size = random.randint(5, 15)
                pygame.draw.circle(surface, (120, 60, 0), (int(x), int(y)), size)
            
        elif name == 'bullet.png':
            # Пуля
            pygame.draw.rect(surface, (255, 255, 0), (0, 0, width, height))
            pygame.draw.rect(surface, (255, 200, 0), (0, 0, width, height), 1)
            
        elif name == 'background.jpg':
            # Звездное небо
            surface.fill((10, 10, 40))
            for i in range(100):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                size = random.randint(1, 3)
                brightness = random.randint(150, 255)
                pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), size)
        
        return surface

# Загрузка изображений
player_img = load_image('player.png', 50, 40)
asteroid_img = load_image('asteroid.png', 40, 40)
bullet_img = load_image('bullet.png', 5, 15)
background_img = load_image('background.jpg', WIDTH, HEIGHT)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.health = 100
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250  # Задержка между выстрелами в мс
    
    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -8
        if keys[pygame.K_RIGHT]:
            self.speed_x = 8
        
        self.rect.x += self.speed_x
        
        # Ограничение движения в пределах экрана
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10
    
    def update(self):
        self.rect.y += self.speed_y
        # Удалить пулю, если она вышла за верхнюю границу экрана
        if self.rect.bottom < 0:
            self.kill()

# Класс астероида
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -50)
        self.speed_y = random.randrange(1, 5)
        self.speed_x = random.randrange(-2, 2)
        self.rotation = 0
        self.rotation_speed = random.randrange(-5, 5)
        self.original_image = self.image
    
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # Вращение астероида
        self.rotation = (self.rotation + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Если астероид упал за нижнюю границу или ушел за боковые
        if self.rect.top > HEIGHT or self.rect.left < -50 or self.rect.right > WIDTH + 50:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -50)
            self.speed_y = random.randrange(1, 5)
            self.speed_x = random.randrange(-2, 2)

# Класс взрыва
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.size = 50
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        # Создаем простую анимацию взрыва
        pygame.draw.circle(self.image, (255, 165, 0), (self.size//2, self.size//2), self.size//2)
        pygame.draw.circle(self.image, (255, 255, 0), (self.size//2, self.size//2), self.size//3)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # скорость анимации
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 8:  # продолжительность анимации
                self.kill()
            else:
                # Увеличиваем и затемняем взрыв
                self.size = 50 + self.frame * 5
                self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                alpha = 255 - self.frame * 30
                color = (255, max(0, 165 - self.frame * 20), 0)
                pygame.draw.circle(self.image, (*color, alpha), (self.size//2, self.size//2), self.size//2)
                pygame.draw.circle(self.image, (255, 255, 0, alpha), (self.size//2, self.size//2), self.size//3)
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center

# [Остальной код остается таким же, как в предыдущей версии...]
# Функции show_start_screen, show_game_over, game_loop, main

def show_start_screen():
    screen.blit(background_img, (0, 0))
    
    title_font = pygame.font.SysFont('Arial', 48)
    instruction_font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 24)
    
    title_text = title_font.render("КОСМИЧЕСКИЙ ЗАЩИТНИК", True, (255, 255, 0))
    instruction1 = instruction_font.render("Управление:", True, (255, 255, 255))
    instruction2 = small_font.render("← →  - Движение влево/вправо", True, (0, 255, 0))
    instruction3 = small_font.render("ПРОБЕЛ - Стрельба", True, (0, 255, 0))
    start_text = instruction_font.render("Нажми ЛЮБУЮ КЛАВИШУ для старта", True, (0, 100, 255))
    
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
    screen.blit(instruction1, (WIDTH//2 - instruction1.get_width()//2, 200))
    screen.blit(instruction2, (WIDTH//2 - instruction2.get_width()//2, 250))
    screen.blit(instruction3, (WIDTH//2 - instruction3.get_width()//2, 280))
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, 400))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over(score):
    screen.blit(background_img, (0, 0))
    
    font = pygame.font.SysFont('Arial', 48)
    small_font = pygame.font.SysFont('Arial', 36)
    
    game_over_text = font.render("ИГРА ОКОНЧЕНА", True, (255, 0, 0))
    score_text = small_font.render(f"Ваш счет: {score}", True, (255, 255, 255))
    restart_text = small_font.render("Нажми ЛЮБУЮ КЛАВИШУ для новой игры", True, (0, 100, 255))
    
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 200))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 280))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 350))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def game_loop():
    global all_sprites, asteroids, bullets, player
    
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for i in range(8):
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

    score = 0
    font = pygame.font.SysFont('Arial', 36)

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        
        all_sprites.update()
        
        # Проверка столкновений пуль и астероидов
        hits = pygame.sprite.groupcollide(bullets, asteroids, True, True)
        for hit in hits:
            score += 10
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            explosions.add(explosion)
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroids.add(asteroid)
        
        # Проверка столкновений игрока и астероидов
        hits = pygame.sprite.spritecollide(player, asteroids, True)
        for hit in hits:
            player.health -= 20
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            explosions.add(explosion)
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroids.add(asteroid)
            if player.health <= 0:
                running = False
        
        # Рендеринг
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        
        # Отображение счета и здоровья
        score_text = font.render(f'Счет: {score}', True, (255, 255, 255))
        health_text = font.render(f'Здоровье: {player.health}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))
        
        controls_text = font.render("← → двигаться, ПРОБЕЛ стрелять", True, (255, 255, 0))
        screen.blit(controls_text, (WIDTH//2 - controls_text.get_width()//2, HEIGHT - 40))
        
        pygame.display.flip()
    
    return score

def main():
    while True:
        show_start_screen()
        final_score = game_loop()
        show_game_over(final_score)

if __name__ == "__main__":
    main()