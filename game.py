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
    def __init__(self):
        self.pos_x = screen.get_width()/2

    def run(self):
        shoot_y = 0
        while True:
            clock.tick(60)
            screen.fill((0, 0, 0))
            screen.blit(background, [0, 0])
            screen.blit(ship, (self.pos_x-ship.get_width()/2, ship_top))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    shoot_y = 500
                    shoot_x = self.pos_x

            key = pygame.key.get_pressed()
            self.keyboard_manager(key)
            
            if shoot_y > 0:
                screen.blit(shot, (shoot_x, shoot_y))
                shoot_y -= 10

            pygame.display.update()
    
    def keyboard_manager(self, key):
        if key[pygame.K_ESCAPE]:
            sys.exit()
        elif key[pygame.K_LEFT]:
            self.pos_x -= 3
        elif key[pygame.K_RIGHT]:
            self.pos_x += 3

if __name__ == '__main__':
    game = Game()
    game.run()