import pygame
import random

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

obstacles = []
for i in range(16):
    obstacle_rect = pygame.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)
    obstacles.append(obstacle_rect) 
player = pygame.Rect((300, 250, 50, 50))

BG = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.mouse.set_visible(False)

run = True
while run:

    screen.fill(BG)

    col = GREEN
    if player.collidelist(obstacles) >= 0:
        print(player.collidelist(obstacles))
        col = RED

    pygame.draw.rect(screen, col, player)
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, obstacle)

    pos = pygame.mouse.get_pos()
    player.center = pos
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    elif key[pygame.K_d] == True:
        player.move_ip(1, 0)
    elif key[pygame.K_w] == True:
        player.move_ip(0, -1)
    elif key[pygame.K_s] == True:
        player.move_ip(0, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()