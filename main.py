import pygame
import random
import sys
import time

pygame.init()
font = pygame.font.SysFont(None, 36)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Block Catcher")

BG = (135, 206, 235)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
LIGHT_BROWN = (196, 164, 132)
LEAF_GREEN = (34, 139, 34)

def draw_tree(surf, x, y):
    pygame.draw.rect(surf, BROWN, [x-20, y-80, 40, 100])
    pygame.draw.polygon(surf, LEAF_GREEN, [[x-30, y-80], [x+30, y-80], [x, y-120]])
    pygame.draw.polygon(surf, LEAF_GREEN, [[x-40, y-60], [x+40, y-60], [x, y-100]])
    pygame.draw.polygon(surf, LEAF_GREEN, [[x-50, y-40], [x+50, y-40], [x, y-80]])
    pygame.draw.polygon(surf, LEAF_GREEN, [[x-60, y-20], [x+60, y-20], [x, y-60]])
tree_xs = []
tree_ys = []
for i in range(5):
    tree_xs.append(random.randint(50, 450))
    tree_ys.append(random.randint(400, 500))

def draw_player():
    global player_surf
    body_points = [(0, 0), (10, 60), (90, 60), (100, 0)]
    zigzag_points = [(5, 30), (7, 32), (93, 32), (95, 30)]
    bl2_points = [(2, 15), (3, 18), (97, 18), (98, 15)]
    bl3_points = [(8, 45), (9, 47), (91, 47), (92, 45)]
    player_surf = pygame.Surface((100, 60), pygame.SRCALPHA)
    pygame.draw.polygon(player_surf, LIGHT_BROWN, body_points)
    pygame.draw.polygon(player_surf, BLACK, zigzag_points)
    pygame.draw.polygon(player_surf, BLUE, bl2_points)
    pygame.draw.polygon(player_surf, BLUE, bl3_points)
draw_player()
player = player_surf.get_rect(center=(250, 450))

def draw_present():
    global present_surf
    present_points = [(0, 0), (0, 20), (20, 20), (20, 0)]
    ribbon_points = [(0, 8), (0, 12), (8, 12), (8, 20), (12, 20), (12, 12), (20, 12), (20, 8), (12, 8), (12, 0), (8, 0), (8, 8)]
    present_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
    color = [RED, GREEN, BLUE]
    present_color = color[random.randint(0, 2)]
    pygame.draw.polygon(present_surf, GREEN, present_points, width=0)
    pygame.draw.polygon(present_surf, BLUE, ribbon_points, width=0)
draw_present()
block_pos = present_surf.get_rect(center=((random.randint(0, SCREEN_WIDTH - 20)), 0))

clock = pygame.time.Clock()
counter = 60
pygame.time.set_timer(pygame.USEREVENT, 1000)

player_speed = 8
block_speed = 0
block_accel = 0.05
score = 0

gamestate = "playing"

bad_block = pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), 0, 20, 20)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if gamestate == "game_over" and key[pygame.K_SPACE]:
            gamestate = "playing"
            counter = 60
            score = 0
            block_speed = 0
            block_pos.y = 0
            bad_block.y = 0
            block_accel = 0.05
        if event.type == pygame.USEREVENT and gamestate == "playing":
            counter -= 1
            if counter <= 0:
                gamestate = "game_over"
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
        if player.colliderect(block_pos):
            score += 1
            block_accel += 0.01
            bad_block.y = 0
            block_pos.y = 0
            block_speed = 0
            block_pos.x = random.randint(0, SCREEN_WIDTH - 20)
            bad_block.x = random.randint(0, SCREEN_WIDTH - 20)
        if player.colliderect(bad_block):
            score -= 1
            block_accel -= 0.01
            bad_block.y = 0
            block_pos.y = 0
            block_speed = 0
            block_pos.x = random.randint(0, SCREEN_WIDTH - 20)
            bad_block.x = random.randint(0, SCREEN_WIDTH - 20)

        if block_pos.top > SCREEN_HEIGHT:
            block_pos.y = 0
            bad_block.y = 0
            block_speed = 0
            block_pos.x = random.randint(0, SCREEN_WIDTH - 20)
            bad_block.x = random.randint(0, SCREEN_WIDTH - 20)

    pygame.draw.circle(screen, WHITE, (250, 1000), 600, width=0)
    for i in range(5):
        draw_tree(screen, tree_xs[i], tree_ys[i])
    screen.blit(player_surf, player)
    screen.blit(present_surf, block_pos)
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