###############################################################################################
                                # HIT137 SOFTWARE NOW – Assignment 3 #

# Lecturer name: Abhijith Beeravolu
# Group members: 
#        - Son Lam Nguyen (Justin) (Student ID: s377342) 
#        - Chirag Dudhat (Student ID: S374835)
# GitHub group link: https://github.com/son-lam-nguyen-s377342/HIT137_SOFTWARENOW_Assignment3.git

###############################################################################################

import pygame
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PLAYER_SIZE = (120, 120)
ENEMY_SIZE = (100, 100)
PROJECTILE_SIZE = (50, 50)
COLLECTIBLE_SIZE = (50, 50)
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooting")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load Images
background_image = pygame.image.load(r'C:\Users\lamng\Downloads\Question 2 - Shooting game\background.jpg')
player_image = pygame.image.load(r'C:\Users\lamng\Downloads\Question 2 - Shooting game\player.gif')
enemy_image = pygame.image.load(r'C:\Users\lamng\Downloads\Question 2 - Shooting game\enemy.png')
projectile_image = pygame.image.load(r'C:\Users\lamng\Downloads\Question 2 - Shooting game\shot.png')
collectible_image = pygame.image.load(r'C:\Users\lamng\Downloads\Question 2 - Shooting game\coin.png')

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_image, PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        self.speed = 5
        self.jump_speed = 10
        self.gravity = 0.5
        self.velocity_y = 0
        self.health = 100
        self.lives = 3
        self.is_jumping = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_speed
        
        if self.is_jumping:
            self.rect.y += self.velocity_y
            self.velocity_y += self.gravity
            if self.rect.y >= SCREEN_HEIGHT - self.rect.height - 10:
                self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
                self.is_jumping = False

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def shoot(self):
        projectile = Projectile(self.rect.right, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(projectile_image, PROJECTILE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.transform.scale(enemy_image, ENEMY_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        self.speed = random.randint(1, 3)
        self.health = 30

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, kind):
        super().__init__()
        self.image = pygame.transform.scale(collectible_image, COLLECTIBLE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind  # 'health' or 'life'

    def update(self):
        pass

# Game Functions
def draw_health_bar(surface, x, y, pct):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def show_game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    exit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 50)
    restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 110, 150, 50)
    pygame.draw.rect(screen, RED, exit_button_rect)
    pygame.draw.rect(screen, GREEN, restart_button_rect)
    exit_text = font.render("Exit", True, WHITE)
    restart_text = font.render("Restart", True, WHITE)
    screen.blit(exit_text, (exit_button_rect.x + 40, exit_button_rect.y + 10))
    screen.blit(restart_text, (restart_button_rect.x + 30, restart_button_rect.y + 10))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
                elif restart_button_rect.collidepoint(mouse_pos):
                    waiting = False

def show_level_complete_screen(level):
    screen.fill(BLACK)
    level_complete_text = font.render(f"Congratulations, Level {level} Complete!", True, WHITE)
    screen.blit(level_complete_text, (SCREEN_WIDTH // 2 - level_complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - level_complete_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Main Game Loop
def main():
    global all_sprites, projectiles
    player = Player()
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    all_sprites.add(player)

    score = 0
    level = 1
    running = True

    # Create initial enemies
    for _ in range(5):
        enemy = Enemy(SCREEN_WIDTH + random.randint(100, 300))
        all_sprites.add(enemy)
        enemies.add(enemy)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        for projectile in projectiles:
            enemy_hits = pygame.sprite.spritecollide(projectile, enemies, False)
            for enemy in enemy_hits:
                enemy.take_damage(10)
                projectile.kill()
                score += 1

        player_hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in player_hits:
            player.health -= 20
            if player.health <= 0:
                player.lives -= 1
                player.health = 100
                if player.lives <= 0:
                    show_game_over_screen(score)
                    main()
                    return

        collectible_hits = pygame.sprite.spritecollide(player, collectibles, True)
        for collectible in collectible_hits:
            if collectible.kind == 'health':
                player.health = min(100, player.health + 20)
            elif collectible.kind == 'life':
                player.lives += 1

        # Add new enemies periodically
        if random.randint(1, 100) <= 2:
            enemy = Enemy(SCREEN_WIDTH + random.randint(100, 300))
            all_sprites.add(enemy)
            enemies.add(enemy)

        if score >= level * 20:
            show_level_complete_screen(level)
            level += 1
            player.rect.x = 100
            player.rect.y = SCREEN_HEIGHT - player.rect.height - 10

        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        draw_health_bar(screen, 10, 10, player.health)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
