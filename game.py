import random

import cv2
import pygame
import os
import country
import sidebar
import world


def countries_init(screen_width, screen_height, border_width):
    cntrs = []

    info_file = open("countries.info")
    lines = info_file.readlines()

    width = int(lines[0].split(':')[0])
    height = int(lines[0].split(':')[1])

    for line in lines[1:]:
        split = line.split(':')
        name = split[0]
        population = int(split[1])
        position = [int((split[2].split(',')[0][1:])),
                    int(split[2].split(',')[1][1:-1])]

        position[0] = int(position[0] / width * screen_width + border_width)
        position[1] = int(position[1] / height * screen_height + border_width)

        points = []

        i = 1
        point = []
        for ch in split[3][1:-2].split():
            if i > 0:
                point.append(int(ch[1:-1]))
            else:
                point.append(int(ch[:-2]))
                point[0] = int(point[0] / width * screen_width + border_width)
                point[1] = int(point[1] / height * screen_height + border_width)
                points.append(tuple(point))
                point = []
            i *= -1

        cnt = country.Country(name)
        cnt.population = population
        cnt.set_position(tuple(position))
        cnt.set_polygon(points)

        cntrs.append(cnt)

    return cntrs


class Game:
    def __init__(self):
        self.width = 1380
        self.height = 600
        self.border_width = 15
        self.paint_area_width = int(self.width * 2 / 3 - 2 * self.border_width)
        self.paint_area_height = int(self.height - 2 * self.border_width)

        self.win = pygame.display.set_mode((self.width, self.height))

        self.border = pygame.image.load(os.path.join("imgs", "border.png"))
        self.border = pygame.transform.scale(self.border, (self.border_width * 2 + self.paint_area_width,
                                                           self.border_width * 2 + self.paint_area_height))
        self.sidebar = sidebar.Sidebar(self.width / 3, self.height, (self.width * 2 / 3, 0))
        self.bg = pygame.image.load(os.path.join("imgs", "bg.jpg"))
        self.bg = pygame.transform.scale(self.bg, (self.paint_area_width, self.paint_area_height))

        self.countries = countries_init(self.paint_area_width, self.paint_area_height, self.border_width)
        self.World = world.World(self.countries)
        self.selected_county = self.World
        self.is_country_infected = False
        self.has_healthy = True
        self.infection_probability = 20
        self.days_passed = 0
        self.speed = 1

        self.sidebar.update(self.selected_county, self.days_passed, self.speed)

    def run(self):
        run = True
        while run:
            clock = pygame.time.Clock()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()
                    if pressed_keys[pygame.K_F4] and pressed_keys[pygame.K_LALT]:
                        run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]

                    if (self.border_width < x) and (x < (self.paint_area_width + self.border_width)):
                        if (self.border_width < y) and (y < (self.paint_area_height + self.border_width)):

                            self.selected_county = self.World

                            for cntry in self.countries:
                                if cntry.is_selected(x, y):
                                    self.selected_county = cntry
                                    break

                    self.sidebar.update(self.selected_county, self.days_passed, self.speed)

                    if self.sidebar.is_button_pressed(x, y):
                        if self.selected_county != self.World:
                            self.selected_county.infect()
                            self.is_country_infected = True

                    self.speed = self.sidebar.speed_selector(x, y)

            self.update()
            self.draw()

            clock.tick(30)

        pygame.quit()

    def update(self):
        if self.is_country_infected and self.has_healthy:
            self.days_passed += 1
            self.World.update()

            for cntry in self.countries:
                color = cntry.update(self.infection_probability, self.speed)
                x = cntry.position[0] - self.border_width
                y = cntry.position[1] - self.border_width
                self.fill(self.bg, (x, y), color)


                if cntry.is_sick:
                    if random.randint(1, 100) <= self.infection_probability:
                        index = random.randint(0, len(self.countries) - 1)
                        self.countries[index].infect()

            self.sidebar.update(self.selected_county, self.days_passed, self.speed)
            if self.World.sick == self.World.population:
                self.has_healthy = False

    def draw(self):
        self.win.blit(self.bg, (self.border_width, self.border_width))
        self.sidebar.draw(self.win)
        self.win.blit(self.border, (0, 0))

        # Remove
        # for cnt in self.countries:
        #     cnt.show_polygon(self.win)

        # for cnt in self.countries:
        #     cnt.show_point(self.win)

        pygame.display.update()


    def fill(self, surface, point, color):
        arr = pygame.surfarray.array3d(surface)
        swap_point = (point[1], point[0])
        cv2.floodFill(arr, None, swap_point, color)
        pygame.surfarray.blit_array(surface, arr)


if __name__ == "__main__":
    game = Game()
    game.run()
