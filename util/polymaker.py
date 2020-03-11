from operator import pos

import pygame
import os

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
name = "rus.png"
image = pygame.image.load(os.path.join("../imgs", name))
image = pygame.transform.scale(image, (width, height))

points = []

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_ESCAPE]:
                run = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            points.append(pos)

    screen.fill((255, 255, 255))
    screen.blit(image, (0, 0))

    for pt in points:
        pygame.draw.circle(screen, (255, 0, 0), pt, 3)

    pygame.display.update()


pygame.quit()
