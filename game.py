import pygame
import random
import os
import json

# Initialize pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombies Survival")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game variables
score = 0
player_health = 3
game_over = False
wave_number = 1
player_speed = 5

spaceship_img = pygame.image.load("spaceship.png")  # Replace with your spaceship image path
spaceship_img = pygame.transform.scale(spaceship_img, (60, 60))  # Resize spaceship to a better fit
asteroid_img = pygame.image.load("asteroid.png")  # Replace with your asteroid image path
asteroid_img = pygame.transform.scale(asteroid_img, (60, 60))  # Resize asteroid to a more fitting size
background_img = pygame.image.load("background_space.PNG")  # Space background image
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize background

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Initialize high score
high_score = 0
if os.path.exists("highscore.json"):
    with open("highscore.json", "r") as file:
        high_score = json.load(file).get("high_score", 0)

# Game objects
player_img = pygame.Surface((50, 50))
player_img.fill(WHITE)
bullet_img = pygame.Surface((5, 10))
bullet_img.fill(RED)
enemy_img = pygame.Surface((50, 50))
enemy_img.fill(RED)

# Sounds
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")
pygame.mixer.music.load("background_music.mp3")

# Game clock
clock = pygame.time.Clock()

spaceship_img = pygame.image.load("spaceship.png")  # Ensure you have a spaceship image
spaceship_img = pygame.transform.scale(spaceship_img, (60, 60))  # Resize to fit the player
asteroid_img = pygame.image.load("asteroid.PNG")  # Ensure you have an asteroid image
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))  # Resize to fit the enemy

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = player_speed
        self.health = player_health

    def update(self):
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.speed
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += self.speed

    def shoot(self):
        if not game_over:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 5)
        self.health = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
            self.rect.y = random.randint(-100, -40)

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Spawn enemies function
def spawn_enemies(num_enemies):
    for _ in range(num_enemies):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

# Update high score
def update_high_score():
    global high_score
    if score > high_score:
        high_score = score
        with open("highscore.json", "w") as file:
            json.dump({"high_score": high_score}, file)




# Draw UI (score, health)
def draw_ui():
    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f"Health: {player_health}", True, WHITE)
    wave_text = font.render(f"Wave:{wave_number}",True,WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (SCREEN_WIDTH - health_text.get_width() - 10, 10))
    screen.blit(wave_text,(SCREEN_WIDTH//2-wave_text.get_width()//2,10))

    heart_icon = pygame.Surface((20, 20))
    heart_icon.fill(RED)
    for i in range(player_health):
        screen.blit(heart_icon, (SCREEN_WIDTH - (i + 1) * 25 - 10, 40))

# Game over screen
def game_over_screen():
    text = font.render("Game Over! Press R to Restart", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
    pygame.display.flip()

#Score increment
class Enemy(pygame.sprite.Sprite):
    def __init__(self,type = "basic"):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,SCREEN_WIDTH - 50)
        self.rect.y = random.randint(-100,-40)
        self.speed = random.randint(3,7)
        self.type = type
        self.health = 1
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0,SCREEN_WIDTH-50)
            self.rect.y = random.randint(-100,-40)
            global score
            score +=1

time_elapsed = 0
speed_increase_interval = 3000

def increase_speed():
    global time_elapsed, enemies
    time_elapsed += 1
    if time_elapsed >= speed_increase_interval:
        for enemy in enemies:
            enemy.speed +=2
        time_elapsed = 0




# Game loop
pygame.mixer.music.play(-1, 0.0)
player = Player()
all_sprites.add(player)
spawn_enemies(wave_number * 5)
running = True
while running:
    clock.tick(60)
    
    increase_speed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()
            if event.key == pygame.K_r and game_over:
                player = Player()
                all_sprites.add(player)
                enemies.empty()
                bullets.empty()
                player = Player()
                all_sprites.add(Player)

                score = 0
                player.health = 3
                wave_number = 1
                game_over = False

                spawn_enemies(wave_number*5)

    if not game_over:
        all_sprites.update()
        # Check for bullet-enemy collisions
        for bullet in bullets:
            enemy_hit = pygame.sprite.spritecollide(bullet, enemies, True)
            if enemy_hit:
                bullet.kill()
                explosion_sound.play()
                for _ in enemy_hit:
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)

        # Check for player-enemy collisions
        enemy_hit = pygame.sprite.spritecollide(player, enemies, True)
        for _ in enemy_hit:
            player_health -= 1
            if player_health <= 0:
                game_over = True
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Spawn new enemies at wave intervals
        if len(enemies) == 0:
            wave_number += 1
            spawn_enemies(wave_number * 5)

        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_ui()
    else:
        update_high_score()
        game_over_screen()

    pygame.display.flip()

pygame.quit()
