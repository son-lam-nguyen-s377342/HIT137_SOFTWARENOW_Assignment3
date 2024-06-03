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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREEN_SIZE = (800, 600)
PLAYER_SIZE = (100, 100)
COLLECTIBLE_SIZE = (30, 30)
FPS = 60
GAME_DURATION = 30

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Collecting Coins")

# Load Images
background_image = pygame.image.load(r'C:\Users\lamng\Downloads\Question 2 - Collecting coin\sky.png') 
player_image = pygame.image.load(r'C:\Users\lamng\Downloads\Question 2 - Collecting coin\guy.png')  
collectible_image = pygame.image.load(r'C:\Users\lamng\Downloads\Question 2 - Collecting coin\coin.png')

# Font
font = pygame.font.Font(None, 36)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_image, PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_SIZE[0] // 2 - self.rect.width // 2
        self.rect.y = SCREEN_SIZE[1] - self.rect.height - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(self.rect.x, SCREEN_SIZE[0] - self.rect.width))

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(collectible_image, COLLECTIBLE_SIZE)
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_SIZE[0] - self.rect.width)
        self.rect.y = random.randint(-500, -50)
        self.speed = random.randint(2, 10)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_SIZE[1]:
            self.reset_position()

# Game Over Screen
def game_over_screen(score):
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=screen.get_rect().center)
    exit_button_rect = pygame.Rect(325, 400, 150, 50)
    restart_button_rect = pygame.Rect(325, 475, 150, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button_rect.collidepoint(mouse_pos):
                    return False
                elif restart_button_rect.collidepoint(mouse_pos):
                    return True

        screen.blit(background_image, (0, 0))
        screen.blit(game_over_text, game_over_rect)
        pygame.draw.rect(screen, WHITE, exit_button_rect, 2)
        pygame.draw.rect(screen, WHITE, restart_button_rect, 2)
        exit_text = font.render("Exit", True, BLACK)
        screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2, exit_button_rect.centery - exit_text.get_height() // 2))
        restart_text = font.render("Restart", True, BLACK)
        screen.blit(restart_text, (restart_button_rect.centerx - restart_text.get_width() // 2, restart_button_rect.centery - restart_text.get_height() // 2))
        pygame.display.flip()

# Main Game Function
def play_game():
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    collectibles = pygame.sprite.Group()

    for _ in range(10):
        collectible = Collectible()
        all_sprites.add(collectible)
        collectibles.add(collectible)

    score = 0
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        # Check collisions
        for collectible in pygame.sprite.spritecollide(player, collectibles, True):
            score += 1
            new_collectible = Collectible()
            all_sprites.add(new_collectible)
            collectibles.add(new_collectible)

        # Draw everything
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        score_text = font.render(f"Score: {score}", True, BLACK)
        time_text = font.render(f"Time: {GAME_DURATION - elapsed_seconds}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (SCREEN_SIZE[0] - 120, 10))
        pygame.display.flip()

        if elapsed_seconds >= GAME_DURATION:
            running = False

        clock.tick(FPS)

    # Show game over screen
    if game_over_screen(score):
        play_game()
    else:
        pygame.quit()

# Start the game
play_game()
