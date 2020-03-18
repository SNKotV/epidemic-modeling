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

    def set_position(self, pos):
        self.position = pos

    def set_polygon(self, points):
        self.country_shape_polygon = Polygon(points)

    def update(self, speed):
        if self.is_sick:
            sick = self.sick + 10000
            self.sick = min(self.population, sick)

            color = (128, 0, 0)
            return color

    def is_selected(self, x, y):
        x -= self.position[0]
        y -= self.position[1]
        point = Point((x, y))
        return self.country_shape_polygon.contains(point)

    def infect(self):
        if not self.is_sick:
            self.is_sick = True
            self.sick = 1
