import pygame, sys
from pygame.locals import *
from collections import deque
from collections import defaultdict
from os.path import abspath, dirname
from random import choice, randint
import heapq



pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((1277, 689))
# solutionDisplay = pygame.display.set_mode((1277, 689))

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


class Shot:
    def __init__(self):
        self.image = shot
        self.pos_x = 0
        self.pos_y = 500

    def draw_shot(self):
        screen.blit(self.image, (self.pos_x,self.pos_y))


class Map:
    def __init__(self, id, pos_x_ini, pos_x_end, pos_y_ini, pos_y_end):
        self.id = id
        self.pos_x_ini = pos_x_ini
        self.pos_x_end = pos_x_end
        self.pos_y_ini = pos_y_ini
        self.pos_y_end = pos_y_end
        self.cost = randint(1, 11)
        if(pos_x_ini == 1060 and pos_y_ini == 0):
            self.cost = 'x' # posicao final
        if(pos_x_ini == 0 and pos_y_ini == 588):
            self.cost = 0 # posicao inicial
        if self.id == 7:
            self.has_ipiranga = 0
        else:
            self.has_ipiranga = randint(0, 2)
        self.neighbors = []
        self.visited = False

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance

    def __str__(self):
        return 'id = ' + str(self.id) + ' ' + str(self.pos_x_ini) + " " + str(self.pos_x_end) + " " + str(self.pos_y_ini) + " " + str(self.pos_y_end) + " " + str(self.cost) + " " + str(self.has_ipiranga)


def dijsktra(graph):
    # id, origin, cost
    nodes_cost = defaultdict(list)
    to_visit = []

    '''
    procura o nó com custo zero, posição inical da nave
    '''
    for i in graph:
        if i.cost == 0:
            first = i
            break

    first.visited = True
    
    '''
    coloca os 2 primeiros vizinhos no heap
    '''
    for i in first.neighbors:
        if i.has_ipiranga == 1:
            cost = i.cost - 5
        else:
            cost = i.cost
        heapq.heappush(to_visit, (cost, first.id, i.id))
    
    '''
    enquanto houver nós no heap, prossegue com dijkstra
    '''
    while to_visit:
        to_verify = heapq.heappop(to_visit)
        id = str(to_verify[2])
        origin = to_verify[1]
        cost = to_verify[0]

        '''
        busca o nó que corresponde ao to_verify
        '''
        # id, (origin, cost)
        node = [x for x in graph if (x.id == to_verify[2])][0]
        node.visited = True
            
        '''
        verifica se já existe o peso para chegar no nó e atualiza
        '''
        if nodes_cost[id]:
            if cost < nodes_cost[id][1]:
                nodes_cost[id] = (origin, cost)
        else:
            nodes_cost[id] = (origin, cost)
            # print(nodes_cost[id])

        '''
        verifica se o nó a ser retirado do heap é o destino final
        '''
        if id == '36':
            path = []
            # id, (origin, cost)
            while id != str(first.id):
                path.append((id, nodes_cost[id][0], nodes_cost[id][1]))
                # print(path)
                id = str(nodes_cost[id][0])
            # print (id)
            path.reverse()
            return path
        
        node_cost = nodes_cost[id][1]
        for i in node.neighbors:
            if not i.visited:
                if i.cost == 'x':
                    cost = node_cost
                else:
                    if i.has_ipiranga == 1:
                        cost = node_cost + i.cost - 5
                    else:
                        cost = node_cost + i.cost

                '''
                verifica se há o vizinho no heap e se precisa atualiza-lo
                '''
                found = False
                for j in to_visit:
                    if i.id == j[2] and cost < j[0]:
                        j = (cost, first.id, i.id)
                        heapq.heapify(to_visit)
                        found = True
                if not found:
                    heapq.heappush(to_visit, (cost, node.id, i.id))

def create_edges(mapa):
    for i in mapa:
        up = [x for x in mapa if(x.pos_y_end == i.pos_y_ini-1 and x.pos_x_ini == i.pos_x_ini )] # certo
        down = [x for x in mapa if(x.pos_y_ini == i.pos_y_end+1 and x.pos_x_ini == i.pos_x_ini )]
        right = [x for x in mapa if(x.pos_x_ini == i.pos_x_end+1 and x.pos_y_ini == i.pos_y_ini )]
        left = [x for x in mapa if(x.pos_x_end == i.pos_x_ini-1 and x.pos_y_ini == i.pos_y_ini )]

        if(up):
            i.neighbors.append(up[0])
        if(down):   
            i.neighbors.append(down[0])
        if(right):
            i.neighbors.append(right[0])
        if(left):
            i.neighbors.append(left[0])


def create_map():
    map = []
    id = 1
    for i in range(0, 1067, 212):
        # print(i)
        for j in range(0, 593, 98):
            # print(j)
            aux = Map(id, i, i+211, j, j+97)
            id += 1
            map.append(aux)
    return map



def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


class Game:
    def __init__(self):
        self.map = create_map()
        create_edges(self.map)
        self.best_path = dijsktra(self.map)
        while self.best_path[-1][2] < 45 or self.best_path[-1][2] > 50:
            self.map = create_map()
            create_edges(self.map)
            self.best_path = dijsktra(self.map)
        print('the real game = ' + str(self.best_path))
        # for i in self.map:
        #     print('pai ' + str(i))
        #     for j in i.neighbors:
        #         print('filho ' + str(j))
        #     print()
        self.pos_x = 100 # screen.get_width()/2 # ship horizontal position
        self.pos_y = ship_top
        self.combustivel = 50
        self.my_pos = None
        self.ativar_postos = True

    def run(self):
        shot_list = deque([])

        while True:
            if(self.combustivel <= 0):
                print('YOU LOSE')
                sys.exit()

            clock.tick(60)
            # node.draw_node(self.pos_x, 2*ship_top)
            # screen.fill((0, 0, 0))
            screen.blit(background, [0, 0])
            # self.scoreText.draw(screen)
            screen.blit(ship, (self.pos_x-ship.get_width()/2, self.pos_y))

            # screen.blit(portal, (900, 25))

            self.draw_costs()
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
        elif key[pygame.K_0]:
            self.ativar_postos = True

    # def draw_solution(self):
    #     pygame.draw.circle(solutionDisplay)
    #     pass

    def draw_costs(self):
        largeText = pygame.font.Font('freesansbold.ttf',25)
        TextSurf, TextRect = text_objects(str(self.combustivel), largeText)
        TextRect.center = ((30),(28))
        gameDisplay.blit(TextSurf, TextRect)
        for i in self.map:
            if(self.ativar_postos and i.has_ipiranga == 1):
                screen.blit(posto, ((i.pos_x_ini),(i.pos_y_ini)))
            TextSurf, TextRect = text_objects(str(i.cost), largeText)
            TextRect.center = ((i.pos_x_ini+105),(i.pos_y_ini+48))
            gameDisplay.blit(TextSurf, TextRect)

    def check_colisor(self):
        for i in self.map:
            if(self.my_pos != i and
                 self.pos_x >= i.pos_x_ini and 
                 self.pos_x < i.pos_x_end and 
                 self.pos_y >= i.pos_y_ini and 
                 self.pos_y < i.pos_y_end):
                if(i.cost == 'x'):
                    print('YOU WIN')
                    sys.exit()
                # print('funciona msm ' + str(i.cost))
                self.my_pos = i
                self.combustivel -= i.cost
                if(self.ativar_postos and i.has_ipiranga == 1):
                    i.has_ipiranga = 0
                    self.combustivel += 5
            


if __name__ == '__main__':
    game = Game()
    game.run()
