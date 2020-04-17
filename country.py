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
        self.stage = []

    def set_position(self, pos):
        self.position = pos

    def set_polygon(self, points):
        self.country_shape_polygon = Polygon(points)

    def update(self, infection_probability, speed):
        if self.is_sick:
            sick = self.sick + max(1, int(random.randint(0, self.sick) * infection_probability / 100))
            self.sick = min(self.population, sick)

        i = 0
        for population in self.stage:
            if self.sick < population:
                break
            i += 1

        col = 255 - int(255 * i / len(self.stage))
        color = (255, col, col)
        return color

    def is_selected(self, x, y):
        point = Point((x, y))
        return self.country_shape_polygon.contains(point)

    def infect(self):
        if not self.is_sick:
            self.is_sick = True
            self.sick = 1