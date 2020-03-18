import pygame
import os

class Sidebar:
    def __init__(self, width, height, pos):
        self.width = int(width)
        self.height = int(height)
        self.pos = pos
        self.bg = pygame.image.load(os.path.join("imgs", "sidebar.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

    def update(self, country):
        """"""

    def draw(self, win):
        win.blit(self.bg, self.pos)
