from operator import pos

import pygame
import os

width = 1200
height = 800
screen = pygame.display.set_mode((width, height))
name = "bg.jpg"
image = pygame.image.load(os.path.join("../imgs", name))
image = pygame.transform.scale(image, (width, height))

points = []
drawpol = False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_ESCAPE]:
                run = False
            elif pressed_key[pygame.K_KP_ENTER] or pressed_key[pygame.K_SPACE]:
                print(points)
            elif pressed_key[pygame.K_BACKSPACE]:
                if points:
                    points.pop()
            elif pressed_key[pygame.K_p]:
                drawpol = ~drawpol
            elif pressed_key[pygame.K_LCTRL] and pressed_key[pygame.K_q]:
                points = []

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            points.append(pos)

    screen.fill((255, 255, 255))
    screen.blit(image, (0, 0))

    for pt in points:
        pygame.draw.circle(screen, (255, 0, 0), pt, 3)

    if drawpol and len(points) > 2:
        pygame.draw.polygon(screen, (0, 0, 255), points)

    pygame.display.update()


pygame.quit()
