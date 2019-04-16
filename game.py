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

class Shot:
    def __init__(self):
        self.image = shot
        self.pos_x = 0
        self.pos_y = 500

class Game:
    def __init__(self):
        self.pos_x = screen.get_width()/2 # ship horizontal position

    def run(self):
        shoot_y = 0
        shot_list = []
        while True:
            clock.tick(60)
            # screen.fill((0, 0, 0))
            screen.blit(background, [0, 0])
            screen.blit(ship, (self.pos_x-ship.get_width()/2, ship_top))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN and event.key == 32:
                    ship_shot = Shot()
                    ship_shot.pos_x = self.pos_x
                    shot_list.append(ship_shot)

            key = pygame.key.get_pressed()
            self.keyboard_manager(key)

            for i in shot_list:
                screen.blit(i.image, (i.pos_x,i.pos_y))
                i.pos_y -= 10

            pygame.display.update()
    
    def keyboard_manager(self, key):
        if key[pygame.K_ESCAPE]:
            sys.exit()
        elif key[pygame.K_LEFT] and self.pos_x >= ship.get_width()/2:
            self.pos_x -= 10
        elif key[pygame.K_RIGHT] and self.pos_x <= screen.get_width()-ship.get_width()/2:
            self.pos_x += 10

if __name__ == '__main__':
    game = Game()
    game.run()