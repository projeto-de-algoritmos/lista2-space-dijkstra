import pygame, sys
from pygame.locals import *
from collections import deque
from os.path import abspath, dirname
from random import choice, randint


BASE_PATH = abspath(dirname(__file__))
FONT_PATH = BASE_PATH + '/fonts/'
IMAGE_PATH = BASE_PATH + '/images/'
SOUND_PATH = BASE_PATH + '/sounds/'

# Colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)

FONT = FONT_PATH + 'space_invaders.ttf'

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1277, 689))

pygame.mouse.set_visible(0)

ship = pygame.image.load('images/ship.png')
ship_top = screen.get_height() - ship.get_height()
ship_left = screen.get_width()/2 - ship.get_width()/2

screen.blit(ship, (ship_left, ship_top))

background = pygame.image.load('images/space.jpg')
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


class Map:
    def __init__(self, pos_x_ini, pos_x_end, pos_y_ini, pos_y_end):
        self.pos_x_ini = pos_x_ini
        self.pos_x_end = pos_x_end
        self.pos_y_ini = pos_y_ini
        self.pos_y_end = pos_y_end
        self.coust = randint(1, 11)
        self.has_ipiranga = randint(0, 1)

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


def create_map():
    map = []
    for i in range(0, 1277, 212):
        for j in range(0, 689, 98):
            aux = Map(i, i+211, j, j+97)
            map.append(aux)
    return map

class Game:
    def __init__(self):
        self.map = create_map()
        for i in self.map:
            print(i.has_ipiranga)
        self.pos_x = screen.get_width()/2 # ship horizontal position
        self.pos_y = ship_top
        # self.scoreText = Text(FONT, 20, 'Score', WHITE, 5, 5)

    def run(self):
        shot_list = deque([])

        # node = Node(5)

        while True:
            clock.tick(60)
            # node.draw_node(self.pos_x, 2*ship_top)
            # screen.fill((0, 0, 0))
            screen.blit(background, [0, 0])
            # self.scoreText.draw(screen)
            screen.blit(ship, (self.pos_x-ship.get_width()/2, self.pos_y))
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
        # print(self.pos_x, self.pos_y)
        if key[pygame.K_ESCAPE]:
            sys.exit()
        elif key[pygame.K_LEFT] and self.pos_x >= ship.get_width()/2:
            self.pos_x -= 10
        elif key[pygame.K_RIGHT] and self.pos_x <= screen.get_width()-ship.get_width()/2:
            self.pos_x += 10
        elif key[pygame.K_UP] and self.pos_y >= ship.get_height()/2:
            self.pos_y -= 10
        elif key[pygame.K_DOWN] and self.pos_y <= screen.get_height()-ship.get_height():
            self.pos_y += 10

if __name__ == '__main__':
    game = Game()
    game.run()