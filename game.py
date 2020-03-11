import pygame
import os
import country
import sidebar


def countries_init():
    cntrs = []
    rus = country.Country("RUS")
    rus.set_size((400, 200))
    rus.set_position((50, 50))
    rus.load_image("rus.png")
    rus.set_polygon([(0, 0), (0, 600), (600, 600), (600, 0)])
    # cntrs.append(rus)

    rus2 = country.Country("RUS")
    rus2.set_size((400, 200))
    rus2.set_position((150, 150))
    rus2.load_image("rus.png")
    rus2.set_polygon([(600, 300), (1200, 300), (1200, 600), (600, 600)])
    # cntrs.append(rus2)
    return cntrs


class Game:
    def __init__(self):
        self.width = 1380
        self.height = 600
        self.border_width = 15
        self.paint_area_width = int(self.width * 2 / 3 - 2 * self.border_width)
        self.paint_area_height = int(self.height - 2 * self.border_width)

        self.win = pygame.display.set_mode((self.width, self.height))

        #self.border = pygame.image.load(os.path.join("imgs", "border.png"))
        self.sidebar = sidebar.Sidebar(self.width / 3, self.height, (self.width * 2 / 3, 0))
        self.bg = pygame.image.load(os.path.join("imgs", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.paint_area_width, self.paint_area_height))
        self.county_borders = pygame.image.load(os.path.join("imgs", "country_borders.png"))
        self.county_borders = pygame.transform.scale(self.county_borders, (self.paint_area_width, self.paint_area_height))

        self.countries = countries_init()
        self.selected_county = None
        self.is_country_infected = False
        self.days_passed = 0
        self.speed = 1

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
                    for cntry in self.countries:
                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]
                        if cntry.is_selected(x, y):
                            #
                            cntry.infect()
                            self.is_country_infected = True
                            #
                            self.selected_county = cntry
                            break

            self.update()
            self.draw()

            clock.tick(30)

        pygame.quit()

    def update(self):
        if self.is_country_infected:
            self.days_passed += self.speed

            self.sidebar.update(self.selected_county)

            for cntry in self.countries:
                cntry.update(self.speed)



    def draw(self):

        self.win.blit(self.bg, (self.border_width, self.border_width))

        self.sidebar.draw(self.win)

        for cntry in self.countries:
            cntry.draw(self.win)

        self.win.blit(self.county_borders, (self.border_width, self.border_width))

        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
