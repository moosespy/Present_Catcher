import pygame
import random
import sys
import time

pygame.init()
font = pygame.font.SysFont(None, 36)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Pong")


BG = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
counter = 30
pygame.time.set_timer(pygame.USEREVENT, 1000)

player_speed = 8
block_speed = 0
block_accel = 0.05
score = 0

gamestate = "playing"
    
block_pos = pygame.math.Vector2(float(random.randint(0, SCREEN_WIDTH - 20)), float(0.0))
block_width = 20.0
block_height = 20.0

player = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 40, 100, 20)
block = pygame.Rect(block_pos.x, block_pos.y, block_width, block_height)
bad_block = pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), 0, 20, 20)
run = True
while run:
    screen.fill(BG)
    key = pygame.key.get_pressed()
    if gamestate == "playing":
        if key[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        elif key[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
            player.x += player_speed

        block_speed += block_accel
        block_pos.y += block_speed
        bad_block.y += block_speed
        if player.colliderect(block):
            score += 1
            block_accel += 0.01
            bad_block.y = 0
            block_pos.y = 0
            block_speed = 0
            block_pos.x = random.randint(0, SCREEN_WIDTH - 20)
            bad_block.x = random.randint(0, SCREEN_WIDTH - 20)
        if player.colliderect(bad_block):
            score -= 1
            block_accel -= 0.02
            bad_block.y = 0
            block_pos.y = 0
            block_speed = 0
            block_pos.x = random.randint(0, SCREEN_WIDTH - 20)
            bad_block.x = random.randint(0, SCREEN_WIDTH - 20)

        if block.top > SCREEN_HEIGHT:
            block_pos.y = 0
            bad_block.y = 0
            block_speed = 0
            block_pos.x = random.randint(0, SCREEN_WIDTH - 20)
            bad_block.x = random.randint(0, SCREEN_WIDTH - 20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if gamestate == "game_over" and key[pygame.K_SPACE]:
            gamestate = "playing"
            counter = 30
            score = 0
            block_speed = 0
            block_accel = 0.05
        if event.type == pygame.USEREVENT and gamestate == "playing":
            counter -= 1
            if counter <= 0:
                gamestate = "game_over"
    block.topleft = (block_pos.x, block_pos.y)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, GREEN, block)
    pygame.draw.rect(screen, RED, bad_block)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    if gamestate == "playing":
        time_text = font.render(f"Time: {counter}", True, WHITE)
        screen.blit(time_text, (10, 30))
    elif gamestate == "game_over":
        game_over_text = font.render("Game Over! Press space to play again!", True, WHITE)
        screen.blit(game_over_text, (10, 30))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()