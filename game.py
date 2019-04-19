import pygame, sys
from pygame.locals import *
from collections import deque
from os.path import abspath, dirname
from random import choice, randint



pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((1277, 689))

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1277, 689))

pygame.mouse.set_visible(0)

ship = pygame.image.load('images/ship.png')
ship_top = screen.get_height() - ship.get_height()
ship_left = screen.get_width()/2 - ship.get_width()/2

screen.blit(ship, (ship_left, ship_top))

posto = pygame.image.load('images/mystery.png')
portal = pygame.image.load('images/enemy2_1.png')
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
        if(pos_x_ini == 1060 and pos_y_ini == 0):
            self.coust = 'x'
        self.has_ipiranga = randint(0, 2)

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance

    def __str__(self):
        return str(self.pos_x_ini) + " " + str(self.pos_x_end) + " " + str(self.pos_y_ini) + " " + str(self.pos_y_end) + " " + str(self.coust) + " " + str(self.has_ipiranga)


def create_map():
    map = []
    for i in range(0, 1277, 212):
        for j in range(0, 689, 98):
            aux = Map(i, i+211, j, j+97)
            map.append(aux)
    return map



def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


class Game:
    def __init__(self):
        self.map = create_map()
        for i in self.map:
            print(i)
        self.pos_x = 100 # screen.get_width()/2 # ship horizontal position
        self.pos_y = ship_top
        self.combustivel = 50
        self.onde_eu_to = None

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

            # screen.blit(portal, (900, 25))

            self.draw_cousts()
            self.check_colisor()

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
    
    def draw_cousts(self):
        largeText = pygame.font.Font('freesansbold.ttf',25)
        TextSurf, TextRect = text_objects(str(self.combustivel), largeText)
        TextRect.center = ((30),(28))
        gameDisplay.blit(TextSurf, TextRect)
        for i in self.map:
            if(i.has_ipiranga == 1):
                screen.blit(posto, ((i.pos_x_ini),(i.pos_y_ini)))
            TextSurf, TextRect = text_objects(str(i.coust), largeText)
            TextRect.center = ((i.pos_x_ini+105),(i.pos_y_ini+48))
            gameDisplay.blit(TextSurf, TextRect)

    def check_colisor(self):
        for i in self.map:
            if(self.onde_eu_to != i and
                 self.pos_x >= i.pos_x_ini and 
                 self.pos_x < i.pos_x_end and 
                 self.pos_y >= i.pos_y_ini and 
                 self.pos_y < i.pos_y_end):
                print('funciona msm ' + str(i.coust))
                self.onde_eu_to = i
                self.combustivel -= i.coust
            


if __name__ == '__main__':
    game = Game()
    game.run()
