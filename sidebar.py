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
        self.country_population = ""
        self.country_population_pos = (self.position[0] + int(545 / 800 * self.width),
                                       self.position[1] + int(255 / 600 * self.height))
        self.country_sick = ""
        self.country_sick_pos = (self.position[0] + int(545 / 800 * self.width),
                                 self.position[1] + int(1 / 2 * self.height))

        pygame.font.init()
        self.country_name_font = pygame.font.SysFont("Times New Roman", 40)
        self.country_population_font = pygame.font.SysFont("Times New Roman", 30)

    def update(self, country):
        self.country_name = country.name
        self.country_population = str(country.population - country.sick)
        self.country_sick = str(country.sick)

    def draw(self, win):
        win.blit(self.bg, self.position)

        country_name = self.country_name_font.render(self.country_name, False, (0, 0, 0))
        width, height = self.country_name_font.size(self.country_name)
        country_name_pos = (self.country_name_pos[0] - int(width / 2), self.country_name_pos[1])
        win.blit(country_name, country_name_pos)

        country_population = self.country_population_font.render(self.country_population, False, (0, 110, 0))
        width, height = self.country_population_font.size(self.country_population)
        country_population_pos = (self.country_population_pos[0] - int(width / 2), self.country_population_pos[1])
        win.blit(country_population, country_population_pos)

        country_sick = self.country_population_font.render(self.country_sick, False, (130, 0, 0))
        width, height = self.country_population_font.size(self.country_sick)
        country_sick_pos = (self.country_sick_pos[0] - int(width / 2), self.country_sick_pos[1])
        win.blit(country_sick, country_sick_pos)




    def is_button_pressed(self, x, y):
        x -= self.position[0]
        y -= self.position[1]
        point = Point((x, y))
        return self.infect_button.contains(point)
