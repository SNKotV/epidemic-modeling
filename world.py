from itertools import starmap

import pygame
import random
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import os
import cv2


class World:

    def __init__(self, countries):
        self.name = "Мир"
        self.countries = countries
        self.population = 0
        for country in self.countries:
            self.population += country.population
        self.country_shape_polygon = None
        self.sick = 0
        self.is_sick = False

    def set_polygon(self, points):
        self.country_shape_polygon = Polygon(points)

    def update(self):
        self.sick = 0
        for country in self.countries:
            self.sick += country.sick
