import pygame
import random
import heapq
import numpy
from sklearn import tree
from pygame.locals import *
from sys import exit
from warnings import warn
import time

size = wight, height =500,500
X=int(wight/10)
Y=int(height/10)
end = endx, endy = 5,4 ##cel smieciarki

## rodzaj pola zaleznie od jego wartosci w tabeli tab[][]
## -1,-2,-3 - wysypiska smieci. [0,1] - trawa, 2 - droga, - 3 domek, 4 - drzewa 

grass = 1
road = 2
home = 3
treee = 4
random.seed()

zapziel=0
zapzol=0
zapnieb=0
paliwo=1

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, allow_diagonal_movement = False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 2

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            warn("giving up on pathfinding too many iterations")
            return return_path(current_node)

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []

        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)


        # Loop through children
        for child in children:

            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            open_list.append(child)

'''
#heurystyka
#heurystyka odwoluje sie do Manhattan Distance miedzy start a end

def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

### implementacja kolejki priorytetowej
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

#generowanie i wybieranie sasiednich pol
def getneighbours(somepoint):
    x = 0
    y =0
    results = []
    if point[0]+1 < 8 and tabroad[point[0]+1][point[1]] != 'x':
        x=point[0]+1
        y=point[1]
        results.append(x)
        results.append(y)
    if point[0]-1 > 0 and tabroad[point[0]-1][point[1]] != 'x':
        x=point[0]-1
        y=point[1]
        results.append(x)
        results.append(y)
    if point[1]+1 < 8 and tabroad[point[0]][point[1]+1] != 'x':
        x=point[0]
        y=point[1]+1
        results.append(x)
        results.append(y)
    if point[1]-1 > 0 and tabroad[point[0]][point[1]-1] != 'x':
        x=point[0]
        y=point[1]-1
        results.append(x)
        results.append(y)
    return results

#A*

def a_star_search(taba, start, end):
    fringe = PriorityQueue()
    fringe.put(start,0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    explored = []
    while not fringe.empty():
        if fringe.empty():
            print("no solution")
        else:
            current = fringe.get()
        
            if current == end:
                break

            for next in getneighbours(current):                    #next jako int 
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(end, next)
                    fringe.put(next, priority)
                    came_from[next] = current
                explored.append(current)
    return came_from, cost_so_far
'''


pygame.init()
TrackSize = X,Y

tab =       [[0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0]]

#choosing the starting point and asseting junk collector to it
#randomizing the map

decider = random.randint(0,1)

if decider == 0:
    decider1 = random.randint(1,8)
    tab[0][decider1] = -2
    tab[0][decider1-1] = -1
    tab[0][decider1+1] = -3
    tab[1][decider1] = 2
    start = startx, starty = 1,decider1 ##Junk Collector starting point
    point = pointx, pointy = startx, starty #wskazanie na aktualny punkt
elif decider ==1:
    decider2 = random.randint(1,8)
    tab[decider2][0] = -2
    tab[decider2-1][0] = -1
    tab[decider2+1][0] = -3
    tab[decider2][1] = 2
    start = startx, starty = decider2,1 ##Junk Collector starting point
    point = pointx, pointy = startx, starty #wskazanie na aktualny punkt


def connect_roads(some_tab,start_point,end_point):
    some_tab[end_point[0]][end_point[1]] = 0
    path= astar(some_tab, start_point, end_point)
    for node in path:
        some_tab[node[0]][node[1]] = 2
    return some_tab

def count_roads(some_tab):
    counter = 0
    for i in range (0,10):
        for j in range (0,10):
            if some_tab[i][j] == road:
                counter = counter + 1
    return counter

def count_trees(some_tab):
    counter = 0
    for i in range (0,10):
        for j in range (0,10):
            if some_tab[i][j] == treee:
                counter = counter + 1
    return counter

def count_homes(some_tab):
    counter = 0
    for i in range (0,10):
        for j in range (0,10):
            if some_tab[i][j] == home:
                counter = counter + 1
    return counter

def check_if_empty(tab,x,y):
    if tab[x][y] == 0:
        return True
    else:
        return False

def add_road(tab,x,y):
    if check_if_empty(tab,x,y) == True:
        tab[x][y] = road
    return tab

def add_grass(tab,x,y):
    if check_if_empty(tab,x,y) == True:
        tab[x][y] = grass
    return tab

def add_home(tab,x,y):
    if check_if_empty(tab,x,y) == True:
        if tab[x+1][y] == road or tab[x-1][y] == road or tab[x][y-1] == road or tab[x][y+1] == road:
              tab[x][y] = home
    return tab

def add_tree(tab,x,y):
    if check_if_empty(tab,x,y) == True:
        tab[x][y] = treee
    return tab

def add_two_roadpoints(some_tab,start=start):
    deciderx1 = random.randint(0,4)
    decidery1 = random.randint(0,4)
    deciderx2 = random.randint(5,9)
    decidery2 = random.randint(5,9)
    if some_tab[deciderx1][decidery1] == 0 and some_tab[deciderx2][decidery2] == 0:
        some_tab[deciderx1][decidery1] = road
        some_tab[deciderx2][decidery2] = road
        point1 = point1x, point1y = deciderx1,decidery1
        point2 = point2x, point2y = deciderx2,decidery2
        connect_roads(some_tab,point1,start)
        connect_roads(some_tab,point2,start)
        if count_roads(some_tab) < 17:
            connect_roads(some_tab,point1,point2)

        return some_tab
    else:
        add_two_roadpoints(some_tab)


tab=add_two_roadpoints(tab)


def randomize_map(some_tab,number_of_homes = 16,number_of_trees = 20,number_of_roads = 40):
    roads_count = count_roads(some_tab)
    homes_counter = count_homes(some_tab)
    trees_counter = count_trees(some_tab)
    x_pos = random.randint(0,9)
    y_pos = random.randint(0,9)
    neighbour_xplus=None
    neighbour_xminus=None
    neighbour_yplus=None
    neighbour_yminus=None
    number_of_neighbours = 0
    if x_pos > 0:
        neighbour_xminus = some_tab[x_pos-1][y_pos]
        number_of_neighbours = number_of_neighbours + 1
    if x_pos < len(some_tab) - 2:
        neighbour_xplus = some_tab[x_pos+1][y_pos]
        number_of_neighbours = number_of_neighbours + 1
    if y_pos < len(some_tab[len(some_tab)-2]) -2:
        neighbour_yplus = some_tab[x_pos][y_pos+1]
        number_of_neighbours = number_of_neighbours + 1
    if y_pos > 0:
        neighbour_yminus = some_tab[x_pos][y_pos-1]
        number_of_neighbours = number_of_neighbours + 1
    if(roads_count<number_of_roads):
        adjacent_roads = 0
        if neighbour_xplus == road:
            adjacent_roads= adjacent_roads + 1
        if neighbour_yplus == road:
            adjacent_roads = adjacent_roads + 1
        if neighbour_yminus == road:
            adjacent_roads = adjacent_roads + 1
        if neighbour_xminus == road:
            adjacent_roads = adjacent_roads + 1
        if adjacent_roads>0:
            add_road(some_tab,x_pos,y_pos)
    elif(homes_counter<number_of_homes):
        add_home(some_tab,x_pos,y_pos)
    elif(trees_counter<number_of_trees):
        add_tree(some_tab,x_pos,y_pos)
    return some_tab

for i in range(0,500):
    randomize_map(tab)

#mapa smeci        
tabtrash = [[0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]]

#mapa drogi
tabroad =  [[0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]]

#mapa kosztow drogi
tabcost =  [[0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]]



#rysowanie mapy drogi


def generateroad(taba,tabb):
    for z1 in range(10):
     for z2 in range (10):
         if taba[z1][z2] != 2:
             tabb[z1][z2] = 'x'
         if taba[z1][z2] == 2 and z1 == int(posX/X) and z2 == int(posY/Y):
             tabb[z1][z2] = 1
         elif taba[z1][z2] == 2:
             tabb[z1][z2] = 0

#rysowanie mapy kosztow drogi
def generatecostroad(taba,tabb):
    for z1 in range(10):
     for z2 in range (10):
         if taba[z1][z2] == road:
             tabb[z1][z2] = 0
         else:
            tabb[z1][z2] = 1

#generowanie miejsca smieci##############################################
ldomek=0
mp=9
for i2 in range(0,10):
    print(tab[i2])
    for j2 in range(0,10):
        if tab[i2][j2]==3:
            ldomek=ldomek+1
lsmieci=ldomek/4

print(int(lsmieci))
def generatetrash(a,b):
    while a < 1:
        vx=random.randint(0,9)
        vy=random.randint(0,9)
        if tab[vx][vy]==3 and tabtrash[vx][vy]==0:
            tabtrash[vx][vy] = b
            a=a+1;
    a=0;

def dec():
    atrybuty=["czy_dom","przepelnienie","paliwo","zapelnienie_kolorem","typ_domku","czy_weekend"]
    #true=1, false=0
    # zbior uczacy
    A =[[1, 1, 1, 0, 1, 1], [1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 1], [0, 1, 1, 1, 0, 1], [0, 1, 0, 1, 1, 0], [1, 1, 1, 0, 0, 1], 
        [0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0], [1, 1, 1, 1, 0, 0], [0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1], 
        [1, 1, 0, 1, 0, 1], [1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 0, 0], [0, 1, 1, 1, 0, 1], [0, 1, 0, 1, 0, 1], [1, 1, 0, 0, 1, 0], 
        [0, 1, 0, 0, 0, 0], [1, 1, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1], [1, 1, 1, 0, 1, 1], [0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0], 
        [0, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 1], [0, 1, 0, 1, 1, 0], [1, 1, 0, 1, 1, 1], [0, 0, 1, 1, 1, 0], [0, 1, 1, 1, 0, 1], 
        [0, 0, 0, 1, 1, 0], [0, 0, 1, 0, 0, 1], [1, 1, 0, 1, 0, 1], [1, 1, 0, 1, 1, 1], [1, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 1], 
        [1, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 1], [0, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1], [1, 0, 0, 0, 0, 1], [0, 0, 1, 1, 0, 1], 
        [1, 1, 1, 1, 1, 1], [1, 1, 1, 0, 0, 1], [0, 0, 1, 0, 1, 0], [1, 1, 1, 0, 1, 1], [0, 0, 1, 0, 0, 1], [1, 1, 1, 0, 0, 1], 
        [0, 0, 0, 1, 0, 0], [1, 1, 0, 1, 1, 0], [1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [0, 1, 0, 0, 0, 0], [0, 1, 0, 1, 1, 0], 
        [1, 1, 0, 1, 0, 1], [0, 0, 1, 1, 1, 1], [1, 0, 0, 0, 1, 0], [1, 1, 1, 0, 1, 1], [1, 0, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1], 
        [0, 1, 0, 1, 0, 0], [0, 0, 0, 1, 1, 0], [1, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 0], [1, 0, 1, 1, 1, 1], [1, 0, 1, 0, 0, 1], 
        [1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 0], [1, 1, 0, 0, 1, 0], [1, 0, 1, 1, 1, 0], [1, 1, 0, 0, 1, 0], [1, 1, 0, 1, 1, 1], 
        [0, 0, 0, 0, 1, 0], [0, 1, 1, 1, 1, 0], [0, 1, 0, 0, 0, 1], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 1, 0], [1, 0, 0, 1, 1, 1], 
        [1, 0, 1, 1, 0, 1], [0, 0, 0, 0, 1, 1], [1, 1, 0, 1, 1, 0], [0, 1, 0, 0, 1, 0], [1, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1], 
        [0, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1], [0, 0, 0, 1, 1, 0], [0, 0, 1, 1, 0, 1], [0, 1, 1, 1, 1, 0], [1, 0, 0, 0, 1, 1], 
        [1, 0, 1, 1, 0, 1], [0, 1, 0, 0, 1, 1], [0, 0, 1, 1, 1, 1], [1, 1, 1, 0, 1, 0], [0, 1, 0, 0, 1, 1], [1, 1, 1, 0, 1, 0], 
        [0, 1, 1, 1, 0, 0], [0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1], [0, 1, 0, 1, 1, 1], 
        [1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 1, 0], [0, 1, 1, 0, 0, 1], [0, 0, 1, 1, 0, 0], [1, 1, 0, 1, 1, 0], [1, 0, 0, 1, 1, 0], 
        [1, 1, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1], 
        [1, 1, 1, 1, 0, 0], [0, 1, 0, 1, 1, 0], [0, 0, 0, 0, 0, 1], [0, 0, 1, 1, 0, 1], [1, 1, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1], 
        [1, 0, 1, 1, 0, 0], [1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 0, 0], [1, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 0, 0], 
        [0, 1, 1, 1, 0, 1], [1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 0, 1], [0, 1, 0, 0, 0, 1], [1, 0, 0, 1, 1, 1], 
        [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 1, 1], [0, 1, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0], [0, 1, 1, 0, 0, 0], [1, 1, 0, 0, 1, 0], 
        [0, 0, 1, 1, 0, 1], [0, 0, 1, 0, 1, 1], [1, 1, 1, 1, 0, 0], [0, 1, 0, 1, 1, 0], [1, 0, 1, 0, 0, 1], [0, 1, 0, 0, 1, 0], 
        [1, 1, 0, 1, 1, 0], [1, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 1], [0, 1, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 0], 
        [1, 0, 0, 0, 1, 1], [0, 1, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0], [1, 1, 0, 1, 1, 0], [1, 0, 1, 1, 0, 1], [0, 1, 1, 1, 0, 0], 
        [0, 1, 1, 0, 0, 1], [1, 0, 0, 0, 1, 1], [0, 1, 0, 1, 1, 1], [1, 1, 0, 0, 1, 0], [1, 1, 1, 0, 1, 0], [0, 1, 1, 0, 1, 1], 
        [0, 0, 1, 1, 1, 0], [0, 1, 0, 1, 0, 1], [1, 0, 1, 1, 1, 0], [0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0], 
        [1, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1], [1, 0, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0]]      
    
    B = [0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1,
         0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1,
         0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0,
         0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0]

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(A, B)
    return clf

def dec_smieciarka(point,zapziel,zapnieb,zapzol,paliwo):
    clf=dec()    
    direction=point
    primpoint=point
    a=1
    b=-1
    mzpx=[-1,0,1]
    mzpy=[-1,0,1]
    czy_dom=0
    czy_weekend=0
    typ_domku=0
    if zapziel==5 and zapnieb==5 and zapzol==5:
        przepelnienie=1
        zap_kol=1
    else:
        przepelnienie=0
        zap_kol=0
    
    dec_table=[czy_dom,przepelnienie,paliwo,zap_kol,typ_domku,czy_weekend]
    while True:
        for x in mzpx:
            for y in mzpy:
                newpoint=point[0]+(mzpx[x]),point[1]+(mzpy[y])
                if newpoint[0]>=0 and newpoint[0]<=9 and newpoint[1]>=0 and newpoint[1]<=9 and newpoint!=primpoint:
                    if tab[newpoint[0]][newpoint[1]]>2:
                        dec_table[0]=1 #czy_dom
                        if tab[newpoint[0]][newpoint[1]]==3:
                            dec_table[4]=0 #typ_domku
                        if tab[newpoint[0]][newpoint[1]]==4:
                            dec_table[4]=1 
                        if tabtrash[newpoint[0]][newpoint[1]]>0 and przepelnienie==0:
                            if tabtrash[newpoint[0]][newpoint[1]]==1:
                                if zapziel<5:
                                    dec_table[3]=0  #zap_kol
                                else:
                                    dec_table[3]=1 
                                prediction=clf.predict([dec_table])
                                if prediction==[1]:
                                    direction=newpoint
                                    return direction
                                    break
                                else:
                                    pass
                            elif tabtrash[newpoint[0]][newpoint[1]]==2:
                                if zapnieb<5:
                                    dec_table[3]=0
                                else:
                                    dec_table[3]=1
                                prediction=clf.predict([dec_table])
                                if prediction==[1]:
                                    direction=newpoint
                                    return direction
                                    break
                                else:
                                    pass
                            elif tabtrash[newpoint[0]][newpoint[1]]==3:
                                if zapzol<5:
                                    dec_table[3]=0
                                else:
                                    dec_table[3]=1
                                prediction=clf.predict([dec_table])
                                if prediction==[1]:
                                    direction=newpoint
                                    return direction
                                    break
                                else:
                                    pass
                        else:
                            pass
                    elif tab[newpoint[0]][newpoint[1]]<0:
                        dec_table[0]=0
                        prediction=clf.predict([dec_table])
                        if prediction==[1]:
                            direction=newpoint
                            return direction
                            break
                        else:
                            pass                     
                else:
                    pass
        a=a+1
        b=b-1
        mzpx.append(a)
        mzpx.insert(0,b)
        mzpy.append(a)
        mzpy.insert(0,b)
   

tabz=1,2,3
for i in tabz:
    num=0
    generatetrash(num,i)

    ############################################################
#grafiki
glasfull = pygame.image.load("glasfull.png")
glasfull = pygame.transform.scale(glasfull,(X,Y))
paperfull = pygame.image.load("paperfull.png")
paperfull = pygame.transform.scale(paperfull,(X,Y))
plasticfull = pygame.image.load("plasticfull.png")
plasticfull = pygame.transform.scale(plasticfull,(X,Y))
cursorSrcLeft = pygame.image.load("cursorLeft.png")
cursorSrcLeft = pygame.transform.scale(cursorSrcLeft,(TrackSize))
cursorSrcUp = pygame.image.load("cursorUp.png")
cursorSrcUp = pygame.transform.scale(cursorSrcUp,(TrackSize))
cursorSrcRight = pygame.image.load("cursorRight.png")
cursorSrcRight = pygame.transform.scale(cursorSrcRight,(TrackSize))
cursorSrcDown = pygame.image.load("cursorDown.png")
cursorSrcDown = pygame.transform.scale(cursorSrcDown,(TrackSize))
cursorSrc=cursorSrcLeft
treeimg = pygame.image.load("tree.png")
treeimg = pygame.transform.scale(treeimg,(X,Y))
houseempty = pygame.image.load("houseempty.png")
houseempty = pygame.transform.scale(houseempty,(X,Y))
housefull = pygame.image.load("housefull.png")
housefull = pygame.transform.scale(housefull,(X,Y))
housefull2 = pygame.image.load("housefull2.png")
housefull2 = pygame.transform.scale(housefull2,(X,Y))
housefull3 = pygame.image.load("housefull3.png")
housefull3 = pygame.transform.scale(housefull3,(X,Y))
glass = pygame.image.load("glass.png")
glass = pygame.transform.scale(glass,(X,Y))
paper = pygame.image.load("paper.png")
paper = pygame.transform.scale(paper,(X,Y))
plastic = pygame.image.load("plastic.png")
plastic = pygame.transform.scale(plastic,(X,Y))
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg,(X,Y))
bg2 = pygame.image.load("bg2.png")
bg2 = pygame.transform.scale(bg2,(size))

#pozycja i szybkosc
speed = X
posX = startx*X
posY = starty*Y
screen = pygame.display.set_mode(size)
display = pygame.display.set_mode((size[0],int(size[1]+(size[1]/10)*3)),0,32) #rozmiar ekranu
generatecostroad(tab,tabcost)
print(tabcost)
#a_star_search(tabroad,start,end)
####################funkcje
def Ruch(pressedKeys):
    if pressedKeys[K_LEFT]:
        return "Left"
    elif pressedKeys[K_RIGHT]:
        return "Right"
    elif pressedKeys[K_UP]:
        return "Up"
    elif pressedKeys[K_DOWN]:
        return "Down"

def Ruch2(path,mj):
    if path[mj][0]==int(posX/X)-1 and path[mj][1]==int(posY/Y):
        return "Left"
    elif path[mj][0]==int(posX/X)+1 and path[mj][1]==int(posY/Y):
        return "Right"
    elif path[mj][0]==int(posX/X) and path[mj][1]==int(posY/Y)-1:
        return "Up"
    elif path[mj][0]==int(posX/X) and path[mj][1]==int(posY/Y)+1:
        return "Down"

#end2=dec_smieciarka(point,zapziel,zapnieb,zapzol,paliwo)
#print point
#print end2

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        pressedKeys = pygame.key.get_pressed()
        display.fill((255,255,255))##
        screen.blit(glass,(6*X,10*Y))
        screen.blit(paper,(6*X,11*Y))
        screen.blit(plastic,(6*X,12*Y))
        screen.blit(bg2,(0,0))
        screen.blit(glasfull,(zapziel*X,10*Y))
        screen.blit(paperfull,(zapnieb*X,11*Y))
        screen.blit(plasticfull,(zapzol*X,12*Y))



                
            
        

#########################ruch
        end2=dec_smieciarka(point,zapziel,zapnieb,zapzol,paliwo)
        print end2
        path = astar(tabcost, point, end2)
#        print(path)
        print(len(path)-1)
        
        #######################
        num=0;

        for mi in range(0,len(path)):
            #rysowanie mapy
            for z1 in range(10):
                for z2 in range (10):
                    if tab[z1][z2] == -1:
                        screen.blit(glass,(z1*X,z2*Y))
                    elif tab[z1][z2] == -2:
                        screen.blit(paper,(z1*X,z2*Y))
                    elif tab[z1][z2] == -3:
                        screen.blit(plastic,(z1*X,z2*Y))
                    elif tab[z1][z2]  == 2:
                        screen.blit(bg,(z1*X,z2*Y))
                    elif tab[z1][z2]  == 3 and tabtrash[z1][z2]==0:
                        screen.blit(houseempty,(z1*X,z2*Y))
                    elif tab[z1][z2]  == 3 and tabtrash[z1][z2]==1:
                        screen.blit(housefull,(z1*X,z2*Y))
                    elif tab[z1][z2]  == 3 and tabtrash[z1][z2]==2:
                        screen.blit(housefull2,(z1*X,z2*Y))
                    elif tab[z1][z2]  == 3 and tabtrash[z1][z2]==3:
                        screen.blit(housefull3,(z1*X,z2*Y))
                    elif tab[z1][z2]  == 4:
                        screen.blit(treeimg,(z1*X,z2*Y))
            display.blit(cursorSrc, (posX, posY))
            pygame.display.update()
            print(int(posX/X),",",int(posY/Y))
            time.sleep(0.5)
            if Ruch2(path,mi)=="Left":
                if tab[int(posX/X)-1][int(posY/Y)] == 2:
                    posX -= speed
                cursorSrc=cursorSrcLeft
                if tab[int(posX/X)-1][int(posY/Y)] == 3:
                    if tabtrash[int(posX/X)-1][int(posY/Y)] == 1 and zapziel!=5:
                        tabtrash[int(posX/X)-1][int(posY/Y)] =0
                        zapziel=zapziel+1;
                        generatetrash(num,1)
                    elif tabtrash[int(posX/X)-1][int(posY/Y)] == 2 and zapnieb!=5:
                        tabtrash[int(posX/X)-1][int(posY/Y)] =0
                        zapnieb=zapnieb+1;
                        generatetrash(num,2)
                    elif tabtrash[int(posX/X)-1][int(posY/Y)] == 3 and zapzol!=5:
                        tabtrash[int(posX/X)-1][int(posY/Y)] =0
                        zapzol=zapzol+1;
                        generatetrash(num,3)
                        
            elif Ruch2(path,mi)=="Right":
                if tab[int(posX/X)+1][int(posY/Y)] == 2:
                    posX += speed
                cursorSrc=cursorSrcRight
                if tab[int(posX/X)+1][int(posY/Y)] == 3:
                    if tabtrash[int(posX/X)+1][int(posY/Y)] == 1 and zapziel!=5:
                        tabtrash[int(posX/X)+1][int(posY/Y)] =0
                        zapziel=zapziel+1;
                        generatetrash(num,1)
                    elif tabtrash[int(posX/X)+1][int(posY/Y)] == 2 and zapnieb!=5:
                         tabtrash[int(posX/X)+1][int(posY/Y)] =0
                         zapnieb=zapnieb+1;
                         generatetrash(num,2)
                    elif tabtrash[int(posX/X)+1][int(posY/Y)] == 3 and zapzol!=5:
                        tabtrash[int(posX/X)+1][int(posY/Y)] =0
                        zapzol=zapzol+1;
                        generatetrash(num,3)
                        
            if Ruch2(path,mi)=="Up":
                if tab[int(posX/X)][int(posY/Y)-1] == 2:
                    posY -= speed
                cursorSrc=cursorSrcUp
                if tab[int(posX/X)][int(posY/Y)-1] == 3:
                    if tabtrash[int(posX/X)][int(posY/Y)-1] == 1 and zapziel!=5:
                        tabtrash[int(posX/X)][int(posY/Y)-1] =0
                        zapziel=zapziel+1;
                        generatetrash(num,1)
                    elif tabtrash[int(posX/X)][int(posY/Y)-1] == 2 and zapnieb!=5:
                        tabtrash[int(posX/X)][int(posY/Y)-1] =0
                        zapnieb=zapnieb+1;
                        generatetrash(num,2)
                    elif tabtrash[int(posX/X)][int(posY/Y)-1] == 3 and zapzol!=5:
                        tabtrash[int(posX/X)][int(posY/Y)-1] =0
                        zapzol=zapzol+1;
                        generatetrash(num,3)
                if tab[int(posX/X)][int(posY/Y)-1] == -1:
                    zapziel=0;
                elif tab[int(posX/X)][int(posY/Y)-1] == -2:
                    zapnieb=0;
                elif tab[int(posX/X)][int(posY/Y)-1] == -3:
                    zapzol=0;
                        
            elif Ruch2(path,mi)=="Down":
                if tab[int(posX/X)][int(posY/Y)+1] == 2:
                    posY += speed
                cursorSrc=cursorSrcDown
                if tab[int(posX/X)][int(posY/Y)+1] == 3:
                    if tabtrash[int(posX/X)][int(posY/Y)+1] == 1 and zapziel!=5:
                        tabtrash[int(posX/X)][int(posY/Y)+1] =0
                        zapziel=zapziel+1;
                        generatetrash(num,1)
                    elif tabtrash[int(posX/X)][int(posY/Y)+1] == 2 and zapnieb!=5:
                        tabtrash[int(posX/X)][int(posY/Y)+1] =0
                        zapnieb=zapnieb+1;
                        generatetrash(num,2)
                    elif tabtrash[int(posX/X)][int(posY/Y)+1] == 3 and zapzol!=5:
                        tabtrash[int(posX/X)][int(posY/Y)+1] =0
                        zapzol=zapzol+1;
                        generatetrash(num,3)
                    
####################################################33                    
        if posX >wight-X:
            posX=wight-X
        elif posX < 0:
            posX=0
        if posY >height-Y:
            posY=height-Y
        elif posY <0:
            posY=0
        point = int(posX/X),int(posY/Y)
        
        pygame.display.update()
        
        
