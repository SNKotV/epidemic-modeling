import pygame
import os
import country


def countries_init():
    cntrs = []
    cnt = country.Country("Test country")
    cnt.population = 5000000
    cnt.is_sick = True
    cnt.set_position((100, 100))
    cnt.set_size((900, 600))
    cnt.load_images("test.png", "testcol.png")
    points = [(0, 0), (0, 500), (500, 500), (500, 0)]
    cnt.set_polygon(points)
    cntrs.append(cnt)
    return cntrs


class Game:
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.win = pygame.display.set_mode((self.width, self.height))
        self.bg = pygame.image.load(os.path.join("imgs", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
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

            for cntry in self.countries:
                cntry.update(self.speed)



    def draw(self):
        self.win.blit(self.bg, (0, 0))

        for cntry in self.countries:
            cntry.draw(self.win)

        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
