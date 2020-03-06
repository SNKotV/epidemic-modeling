import pygame
import random
import os

class Country:

    def __init__(self, name):
        self.name = name
        self.population = 0
        self.position = ()
        self.size = ()
        self.borders_image = ...
        self.colored_image = ...
        self.sick = 0
        self.is_sick = False

    def set_position(self, pos):
        self.position = pos

    def set_size(self, size):
        self.size = size

    def load_images(self, borders_img_name, colored_img_name):
        self.borders_image = pygame.image.load(os.path.join("imgs", borders_img_name))
        self.borders_image = pygame.transform.scale(self.borders_image, self.size)

        self.colored_image = pygame.image.load(os.path.join("imgs", colored_img_name)).convert()
        self.colored_image = pygame.transform.scale(self.colored_image, self.size)
        self.colored_image.set_alpha(0)

    def update(self):
        if self.is_sick:
            self.sick = min(self.population, self.sick + random.randint(0, self.sick))
            alpha = self.sick / self.population * 255
            self.colored_image.set_alpha(alpha)

    def draw(self, win):
        win.blit(self.borders_image, self.position)
        win.blit(self.colored_image, self.position)
