import pygame
import random
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import os


class Country:

    def __init__(self, name):
        self.name = name
        self.population = 0
        self.position = ()
        self.size = ()
        self.borders_image = None
        self.colored_image = None
        self.country_shape_polygon = None
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

    def set_polygon(self, points):
        self.country_shape_polygon = Polygon(points)

    def update(self, speed):
        if self.is_sick:
            sick = self.sick + 10000
            self.sick = min(self.population, sick)
            alpha = self.sick / self.population * 255
            self.colored_image.set_alpha(alpha)

            print(alpha)

    def draw(self, win):
        win.blit(self.borders_image, self.position)
        win.blit(self.colored_image, self.position)

    def is_selected(self, x, y):
        x -= self.position[0]
        y -= self.position[1]
        point = Point((x, y))
        return self.country_shape_polygon.contains(point)

    def infect(self):
        self.is_sick = True
        self.sick = 1
