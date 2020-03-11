from itertools import starmap

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
        self.image = None
        self.country_shape_polygon = None
        self.sick = 0
        self.is_sick = False

    def set_position(self, pos):
        self.position = pos

    def set_size(self, size):
        self.size = size

    def load_image(self, name):
        self.image = pygame.image.load(os.path.join("imgs", name))
        self.image = pygame.transform.scale(self.image, self.size)

    def set_polygon(self, points):
        self.country_shape_polygon = Polygon(points)

    def update(self, speed):
        if self.is_sick:
            sick = self.sick + 10000
            self.sick = min(self.population, sick)




    def draw(self, win):
        win.blit(self.image, self.position)

    def is_selected(self, x, y):
        x -= self.position[0]
        y -= self.position[1]
        point = Point((x, y))
        return self.country_shape_polygon.contains(point)

    def infect(self):
        if not self.is_sick:
            self.is_sick = True
            self.sick = 1
