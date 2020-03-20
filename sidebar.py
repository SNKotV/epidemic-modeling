import pygame
import os

from shapely.geometry import Polygon, Point


class Sidebar:
    def __init__(self, width, height, pos):
        self.width = int(width)
        self.height = int(height)
        self.position = pos
        self.infect_button = Polygon([(int(205 / 800 * self.width), int(485 / 600 * self.height)),
                                      (int(595 / 800 * self.width), int(485 / 600 * self.height)),
                                      (int(595 / 800 * self.width), int(570 / 600 * self.height)),
                                      (int(205 / 800 * self.width), int(570 / 600 * self.height))])

        self.bg = pygame.image.load(os.path.join("imgs", "sidebar.jpg"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

        self.country_name = ""
        self.country_name_pos = (self.position[0] + int(1 / 2 * self.width),
                                 self.position[1] + int(1 / 20 * self.height))

        self.days_passed = ""
        self.days_passed_pos = (self.position[0] + int(250 / 800 * self.width),
                                self.position[1] + int(135 / 600 * self.height))

        self.country_population = ""
        self.country_population_pos = (self.position[0] + int(545 / 800 * self.width),
                                       self.position[1] + int(255 / 600 * self.height))
        self.country_sick = ""
        self.country_sick_pos = (self.position[0] + int(545 / 800 * self.width),
                                 self.position[1] + int(1 / 2 * self.height))

        pygame.font.init()
        self.country_name_font = pygame.font.SysFont("Times New Roman", 40)
        self.days_passed_font = pygame.font.SysFont("Times New Roman", 30)
        self.country_population_font = pygame.font.SysFont("Times New Roman", 30)

        self.speed = 1
        self.speed_border_width = int(70 / 940 * self.width + 1)
        self.speed_border_thickness = int(8 / 940 * self.width)
        self.speed_border_pos = [(self.position[0] + int(504 / 940 * self.width),
                                  self.position[1] + int(290 / 1220 * self.height)),
                                 (self.position[0] + int(600 / 940 * self.width),
                                  self.position[1] + int(290 / 1220 * self.height)),
                                 (self.position[0] + int(695 / 940 * self.width),
                                  self.position[1] + int(290 / 1220 * self.height)),
                                 (self.position[0] + int(794 / 940 * self.width),
                                  self.position[1] + int(290 / 1220 * self.height))
                                 ]

        self.speed_polygons = []
        for point in self.speed_border_pos:
            self.speed_polygons.append(Polygon([
                (point[0] - self.position[0], point[1] - self.position[1]),
                (point[0] - self.position[0] + self.speed_border_width, point[1] - self.position[1]),
                (point[0] - self.position[0] + self.speed_border_width,
                 point[1] + self.speed_border_width - self.position[1]),
                (point[0] - self.position[0], point[1] + self.speed_border_width - self.position[1])]))

    def update(self, country, days_passed, speed):
        self.country_name = country.name
        self.country_population = str(country.population - country.sick)
        self.country_sick = str(country.sick)
        self.days_passed = str(days_passed)

    def draw(self, win):
        win.blit(self.bg, self.position)

        country_name = self.country_name_font.render(self.country_name, False, (0, 0, 0))
        width, height = self.country_name_font.size(self.country_name)
        country_name_pos = (self.country_name_pos[0] - int(width / 2), self.country_name_pos[1])
        win.blit(country_name, country_name_pos)

        days_passed = self.days_passed_font.render(self.days_passed, False, (0, 0, 0))
        width, height = self.days_passed_font.size(self.country_name)
        days_passed_pos = (self.days_passed_pos[0] - int(width / 2), self.days_passed_pos[1])
        win.blit(days_passed, days_passed_pos)

        country_population = self.country_population_font.render(self.country_population, False, (0, 110, 0))
        width, height = self.country_population_font.size(self.country_population)
        country_population_pos = (self.country_population_pos[0] - int(width / 2), self.country_population_pos[1])
        win.blit(country_population, country_population_pos)

        country_sick = self.country_population_font.render(self.country_sick, False, (130, 0, 0))
        width, height = self.country_population_font.size(self.country_sick)
        country_sick_pos = (self.country_sick_pos[0] - int(width / 2), self.country_sick_pos[1])
        win.blit(country_sick, country_sick_pos)

        rect = pygame.Rect(self.speed_border_pos[self.speed - 1],
                           (self.speed_border_width - self.speed_border_thickness,
                            self.speed_border_width - self.speed_border_thickness))
        pygame.draw.rect(win, (235, 200, 50), rect, self.speed_border_thickness)

    def is_button_pressed(self, x, y):
        x -= self.position[0]
        y -= self.position[1]
        point = Point((x, y))
        return self.infect_button.contains(point)

    def speed_selector(self, x, y):
        x -= self.position[0]
        y -= self.position[1]
        point = Point((x, y))
        i = 1
        for sp in self.speed_polygons:
            if sp.contains(point):
                self.speed = i
                return int(i)
            i += 1
        return self.speed
