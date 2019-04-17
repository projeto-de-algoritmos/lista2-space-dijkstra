import pygame, sys
from pygame.locals import *
from collections import deque

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

pygame.mouse.set_visible(0)

ship = pygame.image.load('images/ship.png')
ship_top = screen.get_height() - ship.get_height()
ship_left = screen.get_width()/2 - ship.get_width()/2

screen.blit(ship, (ship_left, ship_top))

background = pygame.image.load('images/background.jpg')
shot = pygame.image.load('images/laser.png')
# node_1 = pygame.image.load('images/number1.png')
# node_3 = pygame.image.load('images/number3.png')
# node_5 = pygame.image.load('images/coin.png')

# class Node:
#     def __init__(self, value):
#         self.value = value
#         if value == 1:
#             self.image = node_1
#         elif value == 3:
#             self.image = node_3
#         else: self.image = node_5

#     def draw_node(self, pos_x, pos_y):
#         screen.blit(self.image, (pos_x, pos_y))


class Shot:
    def __init__(self):
        self.image = shot
        self.pos_x = 0
        self.pos_y = 500

    def draw_shot(self):
        screen.blit(self.image, (self.pos_x,self.pos_y))

class Game:
    def __init__(self):
        self.pos_x = screen.get_width()/2 # ship horizontal position

    def run(self):
        shot_list = deque([])

        # node = Node(5)

        while True:
            clock.tick(60)
            # node.draw_node(self.pos_x, 2*ship_top)
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
                i.draw_shot()
                i.pos_y -= 10
            
            if shot_list and shot_list[0].pos_y <= 0:
                shot_list.popleft()


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