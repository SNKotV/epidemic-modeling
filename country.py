from itertools import starmap

import pygame
import random
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import os
import cv2


class Country:

    def __init__(self, name):
        self.name = name
        self.population = 0
        self.position = ()
        self.country_shape_polygon = None
        self.sick = 0
        self.is_sick = False
        # Remove
        self.pol = []

    def set_position(self, pos):
        self.position = pos

    def set_polygon(self, points):
        self.country_shape_polygon = Polygon(points)
        # Remove
        self.pol = points

    def update(self, infection_probability, speed):
        if self.is_sick:
            sick = self.sick + max(1, int(self.sick * infection_probability / 100))
            self.sick = min(self.population, sick)

            ratio = int(self.sick / self.population * 255)
            color = (255, 255 - ratio, 255 - ratio)
            return color
        else:
            return (255, 255, 255)

    def is_selected(self, x, y):
        point = Point((x, y))
        return self.country_shape_polygon.contains(point)

    def infect(self):
        if not self.is_sick:
            self.is_sick = True
            self.sick = 1

    # Remove
    def show_polygon(self, win):
        pygame.draw.polygon(win, (0, 0, 255), self.pol)

    def show_point(self, win):
        pygame.draw.circle(win, (0, 255, 0), self.position, 3)
