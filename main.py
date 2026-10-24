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

def draw_gradient(width, height, color_top, color_bottom):
    bg_surface = pygame.Surface((1, 2))
    bg_surface.set_at((0, 0), color_top)
    bg_surface.set_at((0, 1), color_bottom)
    gradient_surface = pygame.transform.smoothscale(bg_surface, (width, height))
    return gradient_surface

#colors
LIGHT_BLUE = [135, 206, 235]
MIDNIGHT_BLUE = [25, 25, 112]
GREEN = [0, 255, 0]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
BROWN = [139, 69, 19]
GOLD = [225, 165, 30]
LIGHT_BROWN = [196, 164, 132]
LEAF_GREEN = [34, 139, 34]

#backgrounds
day_bg = draw_gradient(SCREEN_WIDTH, SCREEN_HEIGHT, MIDNIGHT_BLUE, LIGHT_BLUE)
sunset_bg = draw_gradient(SCREEN_WIDTH, SCREEN_HEIGHT, MIDNIGHT_BLUE, GOLD)
night_bg = draw_gradient(SCREEN_WIDTH, SCREEN_HEIGHT, MIDNIGHT_BLUE, BLACK)

#What each thing looks like: snow, trees, player, present, obstacle
particles = []
def draw_snow():
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(-20, 0)
    vel_x = random.uniform(-0.5, 0.5)
    vel_y = random.uniform(2.1, 4.4)
    radius = random.uniform(2, 7)
    return [[x, y], [vel_x, vel_y], radius]

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
    body_points = [(0, 0), (10, 50), (30, 60), (70, 60), (90, 50), (100, 0)]
    zigzag_points = [(5, 30), (20, 40), (35, 30), (50, 40), (65, 30), (80, 40), (95, 30), (95, 32), (80, 42), (65, 32), (50, 42), (35, 32), (20, 42), (5, 32)]
    bl2_points = [(0, 0), (0, 20), (100, 20), (100, 0)]
    player_surf = pygame.Surface((100, 60), pygame.SRCALPHA)
    pygame.draw.polygon(player_surf, LIGHT_BROWN, body_points)
    pygame.draw.polygon(player_surf, BLACK, zigzag_points)
    pygame.draw.polygon(player_surf, GOLD, bl2_points)
draw_player()
player = player_surf.get_rect(center=(250, 450))

def draw_present():
    global present_surf
    present_points = [(0, 10), (0, 30), (20, 30), (20, 10)]
    cross_points = [(0, 18), (0, 22), (8, 22), (8, 30), (12, 30), (12, 22), (20, 22), (20, 18), (12, 18), (12, 10), (8, 10), (8, 18)]
    left_ribbon_points = [(10, 7), (2, 1), (0, 3), (8, 5), (0, 7), (2, 9)]
    right_ribbon_points = [(10, 7), (18, 1), (20, 3), (12, 5), (20, 7), (18, 9)]
    present_surf = pygame.Surface((20, 30), pygame.SRCALPHA)
    color = [RED, GREEN, BLUE]
    present_color = color[random.randint(0, 2)]
    pygame.draw.polygon(present_surf, GREEN, present_points)
    pygame.draw.polygon(present_surf, RED, cross_points)
    pygame.draw.polygon(present_surf, RED, left_ribbon_points)
    pygame.draw.polygon(present_surf, RED, right_ribbon_points)
draw_present()
block_pos = present_surf.get_rect(center=((random.randint(0, SCREEN_WIDTH - 20)), 0))

def draw_obstacle():
    global obst_surf
    obst_points = [(0, 10), (3, 13), (1, 15), (7, 18), (10, 20), (13, 15), (20, 10), (18, 2), (10, 0), (8, 0)]
    obst_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.polygon(obst_surf, BLACK, obst_points)
draw_obstacle()
bad_block = obst_surf.get_rect(center=((random.randint(0, SCREEN_WIDTH - 20)), 0))
b_block2 = obst_surf.get_rect(center=((SCREEN_WIDTH - bad_block.x), 0))

def draw_light_circle(color, radius):
    global glow_surf
    global alpha
    glow_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    for i in range(radius, 0, -1):
        alpha = int((1 - (i / radius))**2.5 * 255)
        pygame.draw.circle(glow_surf, (*color, alpha), (radius, radius), i)
    return glow_surf
glow = draw_light_circle(GOLD, 20)

#timer settings
clock = pygame.time.Clock()
counter = 60
pygame.time.set_timer(pygame.USEREVENT, 1000)

player_speed = 8
block_speed = 0
block_accel = 0.05
score = 0
background = day_bg
gamestate = "menu"
run = True
while run:
    key = pygame.key.get_pressed()
    prev_score = score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #needed to make pygame work
            run = False
        if gamestate == "menu" and key[pygame.K_SPACE]:
            #restart code/start code
            gamestate = "playing"
            counter = 60
            score = 0
            block_speed = 0
            block_pos.y = 0
            bad_block.y = 0
            b_block2.y = 0
            block_accel = 0.05
        if event.type == pygame.KEYDOWN:
            #pause state
            if event.key == pygame.K_p:
                if gamestate == "paused":
                    gamestate = "playing"
                elif gamestate == "playing":
                    gamestate = "paused"
            #backgrounds
            elif event.key == pygame.K_1:
                background = day_bg
            elif event.key == pygame.K_2:
                background = sunset_bg
            elif event.key == pygame.K_3:
                background = night_bg
        if event.type == pygame.USEREVENT and gamestate == "playing":
            #timer
            counter -= 1
            if 20 < counter < 41:
                background = sunset_bg
            if counter < 21:
                background = night_bg
            if counter <= 0:
                gamestate = "menu"
                background = day_bg
    
    screen.blit(background, (0, 0))
    
    #glow_rect = glow.get_rect(center=((block_pos.x + 10), (block_pos.y + 17)))

    #snow
    for _ in range(1):
        particles.append(draw_snow())
    new_particles = []
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        if particle[0][1] <= SCREEN_HEIGHT:
            new_particles.append(particle)
            position = (int(particle[0][0]), int(particle[0][1]))
            radius = int(particle[2])
            pygame.draw.circle(screen, WHITE, position, radius)
    particles = new_particles
    
    #main animations: player movement, present/coal movement, collision detection
    if gamestate == "playing":
        if key[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        elif key[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
            player.x += player_speed

        block_speed += block_accel
        block_pos.y += block_speed
        bad_block.y += block_speed
        b_block2.y += block_speed
        if player.colliderect(block_pos):
            score += 1
            if block_accel < 0.11:
                block_accel += 0.01
            bad_block.y = 0
            b_block2.y = 0
            block_pos.y = 0
            block_speed = 0
            block_pos.x = random.randint(0, SCREEN_WIDTH - 20)
            bad_block.x = random.randint(0, SCREEN_WIDTH - 20)
            b_block2.x = SCREEN_WIDTH - bad_block.x
        if player.colliderect(bad_block) or player.colliderect(b_block2):
            score -= 1
            if block_accel > 0.01:
                block_accel -= 0.01
            bad_block.y = 0
            b_block2.y = 0
            block_pos.y = 0
            block_speed = 0
            block_pos.x = random.randint(0, SCREEN_WIDTH - 20)
            bad_block.x = random.randint(0, SCREEN_WIDTH - 20)
            b_block2.x = SCREEN_WIDTH - bad_block.x

        if block_pos.top > SCREEN_HEIGHT:
            block_pos.y = 0
            bad_block.y = 0
            b_block2.y = 0
            block_speed = 0
            block_pos.x = random.randint(0, SCREEN_WIDTH - 20)
            bad_block.x = random.randint(0, SCREEN_WIDTH - 20)
            b_block2.x = SCREEN_WIDTH - bad_block.x

    #Drawing everything
    pygame.draw.circle(screen, WHITE, (250, 1000), 600, width=0)
    for i in range(5):
        draw_tree(screen, tree_xs[i], tree_ys[i])
    screen.blit(player_surf, player)
    screen.blit(present_surf, block_pos)
    screen.blit(obst_surf, bad_block)
    screen.blit(obst_surf, (b_block2))
    #screen.blit(glow, glow_rect, special_flags=pygame.BLEND_RGBA_ADD)
    #On-screen text
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    if gamestate == "playing":
        time_text = font.render(f"Time: {counter}", True, WHITE)
        screen.blit(time_text, (10, 30))
    elif gamestate == "menu":
        menu_text = font.render("Press space to start!", True, WHITE)
        screen.blit(menu_text, (10, 30))
    elif gamestate == "paused":
        paused_text = font.render("Game Paused", True, BLACK)
        screen.blit(paused_text, (170, 230))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()