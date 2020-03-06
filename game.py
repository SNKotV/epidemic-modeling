import pygame
import os
import country


def countries_init():
    return []


class Game:
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.win = pygame.display.set_mode((self.width, self.height))
        self.countries = countries_init()
        self.days_passed = 0
        self.speed = 1

    def run(self):
        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()
                    if pressed_keys[pygame.K_F4] and pressed_keys[pygame.K_LALT]:
                        run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())

            self.update()
            self.draw()

        pygame.quit()

    def update(self):
        for cntry in self.countries:
            cntry.update()

    def draw(self):

        for cntry in self.countries:
            cntry.draw(self.win)

        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
