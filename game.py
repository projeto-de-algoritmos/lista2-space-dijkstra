import pygame, sys
from pygame.locals import *

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

pygame.mouse.set_visible(0)

ship = pygame.image.load('images/ship.png')
ship_top = screen.get_height() - ship.get_height()
ship_left = screen.get_width()/2 - ship.get_width()/2

screen.blit(ship, (ship_left, ship_top))

background = pygame.image.load('images/background.jpg')
shot = pygame.image.load('images/laser.png')


class Game:
    def run(self):
        shoot_y = 0
        while True:
            clock.tick(60)
            screen.fill((0, 0, 0))
            x, y = pygame.mouse.get_pos()
            screen.blit(background, [0, 0])
            screen.blit(ship, (x-ship.get_width()/2, ship_top))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    shoot_y = 500
                    shoot_x = x

            if shoot_y > 0:
                screen.blit(shot, (shoot_x, shoot_y))
                shoot_y -= 10

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()