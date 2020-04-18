import random

import cv2
import pygame
import os
import country
import sidebar
import world


def countries_init(screen_width, screen_height, border_width, number_of_stages):
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

        base = int(pow(population, 1.0 / number_of_stages))
        stage = []
        while population > 0:
            stage.append(population)
            population //= base
        stage.reverse()

        cnt.stage = stage

        cntrs.append(cnt)

    return cntrs


def create_infection():
    width = 600
    height = 280
    win = pygame.display.set_mode((width, height))

    textFont = pygame.font.SysFont("Times New Roman", 38, bold=True)
    infect_prob_label = textFont.render("Вероятность заражения", False, (20, 20, 20))
    lower_bound = textFont.render("0.01", False, (0, 0, 0))
    upper_bound = textFont.render("1.00", False, (0, 0, 0))
    button_text = textFont.render("Выбрать", False, (40, 40, 40))

    probability = 10
    xpos = 120
    dragging = False
    chosen = False

    while not chosen:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                pos = pygame.mouse.get_pos()
                if 200 <= pos[0] <= 440 and 150 <= pos[1] <= 230:
                    chosen = True
                elif 100 <= pos[0] <= 500 and 80 <= pos[1] <= 100:
                    xpos = pos[0]
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if dragging and 100 <= pos[0] <= 500 and 80 <= pos[1] <= 100:
                    xpos = pos[0]
                    probability = 1 + int((pos[0] - 100) * 99 / 400)

        win.fill((128, 32, 32))
        pygame.draw.line(win, (255, 255, 255), (100, 90), (500, 90), 5)
        win.blit(infect_prob_label, (110, 20))
        win.blit(lower_bound, (20, 75))
        win.blit(upper_bound, (520, 75))
        pygame.draw.circle(win, (40, 40, 40), (xpos, 90), 15)
        pygame.draw.rect(win, (0, 0, 0), pygame.rect.Rect((200, 150), (240, 80)), 3)
        win.blit(button_text, (245, 165))

        pygame.display.update()

    return probability


class Game:
    def __init__(self):
        self.width = 1380
        self.height = 600
        self.border_width = 15
        self.paint_area_width = int(self.width * 2 / 3 - 2 * self.border_width)
        self.paint_area_height = int(self.height - 2 * self.border_width)

        self.border = pygame.image.load(os.path.join("imgs", "border.png"))
        self.border = pygame.transform.scale(self.border, (self.border_width * 2 + self.paint_area_width,
                                                           self.border_width * 2 + self.paint_area_height))
        self.sidebar = sidebar.Sidebar(self.width / 3, self.height, (self.width * 2 / 3, 0))
        self.bg = pygame.image.load(os.path.join("imgs", "bg.jpg"))
        self.bg = pygame.transform.scale(self.bg, (self.paint_area_width, self.paint_area_height))

        self.countries = countries_init(self.paint_area_width, self.paint_area_height, self.border_width, 8)
        self.World = world.World(self.countries)
        self.selected_county = self.World
        self.is_country_infected = False
        self.has_healthy = True
        self.infection_probability = create_infection()
        self.country_index = 0
        self.days_passed = 0
        self.speed = 1

        self.win = pygame.display.set_mode((self.width, self.height))
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

            clock.tick(7 * self.speed)

        pygame.quit()

    def update(self):
        if self.is_country_infected and self.has_healthy:
            self.days_passed += 1
            self.World.update()

            for cntry in self.countries:
                if cntry.is_sick:
                    color = cntry.update(self.infection_probability, self.speed)
                    x = cntry.position[0] - self.border_width
                    y = cntry.position[1] - self.border_width
                    if self.bg.get_at((x, y)) != color:
                        self.fill(self.bg, (x, y), color)

                    if cntry.stage[6] <= cntry.sick <= cntry.stage[7] and random.randint(1, 100) <= self.infection_probability:
                        index = random.randint(0, len(self.countries) - 1)
                        self.countries[index].infect()

            self.sidebar.update(self.selected_county, self.days_passed, self.speed)
            if self.World.sick == self.World.population:
                self.has_healthy = False

    def draw(self):
        self.win.blit(self.bg, (self.border_width, self.border_width))
        self.sidebar.draw(self.win)
        self.win.blit(self.border, (0, 0))
        pygame.display.update()

    def fill(self, surface, point, color):
        arr = pygame.surfarray.array3d(surface)
        swap_point = (point[1], point[0])
        cv2.floodFill(arr, None, swap_point, color)
        pygame.surfarray.blit_array(surface, arr)


if __name__ == "__main__":
    game = Game()
    game.run()
