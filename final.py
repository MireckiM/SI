import pygame
import random
import heapq
from pygame.locals import *
from sys import exit
from warnings import warn
import time
import numpy
from sklearn import tree

size = wight, height =500,500
X=int(wight/10)
Y=int(height/10)
end = endx, endy = 3,3 ##cel smieciarki

## rodzaj pola zaleznie od jego wartosci w tabeli tab[][]
## -1,-2,-3 - wysypiska smieci. [0,1] - trawa, 2 - droga, - 3 domek, 4 - drzewa

grass = 1
road = 2
home = 3
maps = 100
random.seed()

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
            #warn("giving up on pathfinding too many iterations")
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


pygame.init()
TrackSize = X,Y

tabinit =  [[0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]]


tab = [[0,0,0,0,0,0,0,0,0,0,0], #glowna mapa
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

def set_bins(some_tab):
    decider = random.randint(0,3)

    if decider == 0:
        decider1 = random.randint(1,8)
        some_tab[0][decider1] = -2
        some_tab[0][decider1-1] = -1
        some_tab[0][decider1+1] = -3
        some_tab[1][decider1] = 2
        some_tab[1][decider1-1] = 2
        some_tab[1][decider1+1] = 2
        return some_tab
   #start = startx, starty = 1,decider1 ##Junk Collector starting point
    #point = pointx, pointy = startx, starty #wskazanie na aktualny punkt
    elif decider ==1:
        decider2 = random.randint(1,8)
        some_tab[decider2][9] = -2
        some_tab[decider2-1][9] = -1
        some_tab[decider2+1][9] = -3
        some_tab[decider2][8] = 2
        some_tab[decider2-1][8] = 2
        some_tab[decider2+1][8] = 2
        return some_tab
    elif decider ==2:
        decider2 = random.randint(1,8)
        some_tab[decider2][0] = -2
        some_tab[decider2-1][0] = -1
        some_tab[decider2+1][0] = -3
        some_tab[decider2][1] = 2
        some_tab[decider2-1][1] = 2
        some_tab[decider2+1][1] = 2
        return some_tab
    if decider == 3:
        decider1 = random.randint(1,8)
        some_tab[9][decider1] = -2
        some_tab[9][decider1-1] = -1
        some_tab[9][decider1+1] = -3
        some_tab[8][decider1] = 2
        some_tab[8][decider1-1] = 2
        some_tab[8][decider1+1] = 2
        return some_tab
    #start = startx, starty = decider2,1 ##Junk Collector starting point
    #point = pointx, pointy = startx, starty #wskazanie na aktualny punkt

'''def add_roads_to_bins(some_tab):
    for i in range(10):
        for j in range (10):'''





def set_start(some_tab):
    begining = beginingx, beginingy = 0,0
    for i in range (0,10):
        for j in range (0,10):
            if some_tab[i][j] == -2:
                if some_tab[i][j+1] == 2:
                    begining = beginingx, beginingy = i,j+1
                elif some_tab[i+1][j] == 2:
                    begining = beginingx, beginingy = i+1,j
                elif some_tab[i-1][j] == 2:
                    begining = beginingx, beginingy = i-1,j
                elif some_tab[i][j-1] == 2:
                    begining = beginingx, beginingy = i,j-1
    return begining

def set_point(some_tab):
    for i in range (0,10):
        for j in range (0,10):
            if some_tab[i][j] == -2:
                if some_tab[i][j+1] == 2:
                    point = pointx, pointy = i,j+1
                elif some_tab[i+1][j] == 2:
                    point = pointx, pointy = i+1,j
                elif some_tab[i-1][j] == 2:
                    point = pointx, pointy = i-1,j
                elif some_tab[i][j-1] == 2:
                    point = pointx, pointy = i,j-1
    return point

                
def clear_tab(some_tab):
    some_tab = [[0,0,0,0,0,0,0,0,0,0,0],
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
    return some_tab

def connect_roads(some_tab,start_point,end_point):
    some_tab[end_point[0]][end_point[1]] = 0
    path= astar(some_tab, start_point, end_point)
    for point in path:
        some_tab[point[0]][point[1]] = 2
    return some_tab

def rate_road(some_tab,start_point,end_point): #must be a costroad
    path = astar(some_tab, start_point, end_point)
    if path is not None:
        return (len(path))
    else:
        return 0

def rate_map(some_tab):
    cost_tab = [[0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]]
    cost_tab=generatecostroad(some_tab,cost_tab) #NONE Error to fix // Fixed
    rating = 0
    end_point = set_start(some_tab)
   # print(cost_tab)#NONE
    for i in range (0,10):
        for j in range (0,10):
            if some_tab[i][j] == road or  some_tab[i][j] == home :
                this_point = this_pointx,this_pointy = i,j
                rating = rating + rate_road(cost_tab,this_point,end_point)
    return rating



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
            if some_tab[i][j] == 4:
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

def None_sum(*args):
    args = [a for a in args if not a is None]
    return sum(args) if args else None

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
        if tab[x+1][y] == road or tab[x-1][y] == road or tab[x][y+1] == road or tab[x][y-1] == road:
            tab[x][y] = home
    return tab

def add_tree(tab,x,y):
    if check_if_empty(tab,x,y) == True:
        tab[x][y] = 4
    return tab

#sorting
def bubble_sort_highest(nums):

    for i in range(0,len(nums)-1,1):
        for j in range(0,len(nums)-1-i,1):
            if nums[j]<nums[j+1]:
                swap(nums,j,j+1)
                swap(maps,j,j+1)
    return nums

def swap(nums,i,j):
    temp = nums[i]
    nums[i] = nums[j]
    nums[j] = temp

'''
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


tab=add_two_roadpoints(tab)'''

def cut_map(some_tab,number_of_homes = 16,number_of_trees = 20,number_of_roads = 40):
    roads = count_roads(some_tab)
    homes = count_homes(some_tab)
    trees = count_trees(some_tab)
    for i in range(20):
        x_pos = random.randint(0,9)
        y_pos = random.randint(0,9)
        if some_tab[x_pos][y_pos] == road and roads > number_of_roads:
            some_tab[x_pos][y_pos] = 0
        if some_tab[x_pos][y_pos] == home and homes > number_of_homes:
            some_tab[x_pos][y_pos] = 0
        if some_tab[x_pos][y_pos] == 4 and trees > number_of_trees:
            some_tab[x_pos][y_pos] = 0
    return some_tab


def randomize_map(some_tab,number_of_homes = 16,number_of_trees = 20,number_of_roads = 40):
    clear_tab(some_tab)
    set_bins(some_tab)
    for nothing in range(0,900):
        #tree_counts = count_trees(some_tab)
        roads_count = count_roads(some_tab)
        homes_counter = count_homes(some_tab)
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
        elif count_trees(some_tab)<number_of_trees:
            add_tree(some_tab,x_pos,y_pos)
    return some_tab
'''
def make_child(winner,loser):
    new_tab = winner
    return new_tab
'''
def make_child(winner,loser):
    new_tab = [[0,0,0,0,0,0,0,0,0,0,0],
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
    for i in range (0,10):
        for j in range (0,10):
            new_tab[i][j] = winner[i][j]
    #print(winner)
    for i in range (0,10):
        for j in range (0,10):
            neighbour_xplus=None
            neighbour_xminus=None
            neighbour_yplus=None
            neighbour_yminus=None
            if i > 0:
                neighbour_xminus = new_tab[i-1][j]
            if i < len(new_tab) - 2:
                neighbour_xplus = new_tab[i+1][j]
            if j > 0:
                neighbour_yminus = new_tab[i][j-1]
            if j < len(new_tab[len(new_tab)-2]) -2:
                neighbour_yplus = new_tab[i][j+1]
            decider = random.randint(1,100)
            if decider > 80:
                if loser[i][j] == home:
                    if new_tab[i][j] == 2 or new_tab[i][j] == 3 or new_tab[i][j] == 4:
                        new_tab[i][j] = 3
                elif loser[i][j] == road:
                    if new_tab[i][j] == 2 or new_tab[i][j] == 3 or new_tab[i][j] == 4:
                        new_tab[i][j] = 2
                elif loser[i][j] == 4:
                    if new_tab[i][j] == 2 or new_tab[i][j] == 3 or new_tab[i][j] == 4:
                        new_tab[i][j] = 4
    #print(new_tab)
    return new_tab
'''

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
            number_of_neighbours = number_of_neighbours + 1'''


def compare_maps(left_tab,right_tab):
    left_result = rate_map(left_tab)
    right_result = rate_map(right_tab)
    if left_result>=right_result:
        #print("Left map is the winner %d : %d" % (left_result, right_result))
        return make_child(left_tab,right_tab)
    else:
        #print("Right map is the winner %d : %d" % (left_result, right_result))
        return make_child(right_tab,left_tab)

#generowanie mapy

tab1 = [[0,0,0,0,0,0,0,0,0,0,0],
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
tab = randomize_map(tab)
tab1 = randomize_map(tab1)
#cut_map(tab)
#cut_map(tab1)
#print(tab)
#print(tab1)
#mapa smeci
tabtrash =  [[0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]]

zapziel=0
zapzol=0
zapnieb=0
paliwo=1
czy_weekend=0

tabsim = [[0,0,0,0,0,0,0,0,0,0],
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
#tabroad = tabinit

#mapa kosztow drogi
tabcost =  tabinit


#rysowanie mapy drogi

#rysowanie mapy kosztow drogi
def generatecostroad(taba,tabb):
    for z1 in range(10):
     for z2 in range (10):
         if taba[z1][z2] == road:
             tabb[z1][z2] = 0
         else:
            tabb[z1][z2] = 1
    return tabb

#generowanie miejsca smieci
def sred():
    for i2 in range(0,10):
        for j2 in range(0,10):
           if tabtrash[i2][j2]<0:
               tabtrash[i2][j2]=tabtrash[i2][j2]+1


def generatesim():            
    for i12 in range(0,10):
        for j12 in range(0,10):
            if tab[i12][j12]==3:
                ran=random.randint(1,4)
                if ran==1:
                    tabsim[i12][j12]=1
                if ran==2:
                    tabsim[i12][j12]=2
                if ran==3:
                    tabsim[i12][j12]=4
                if ran==4:
                    tabsim[i12][j12]=20
                if ran>4:
                    print(ran)
def cr():
    for ci in range(0,10):
        for cj in range(0,10):
            if tab[ci][cj]==3:
                tabcost[ci][cj]=1
def ucr():
    for ci in range(0,10):
        for cj in range(0,10):
            if tab[ci][cj]==3 and tabtrash[ci][cj]>0:
                tabcost[ci][cj]=0
                
def collecttrash(gx,gy):
    tabcost[gx][gy]=1
    if tabsim[gx][gy]==1:
        tabtrash[gx][gy]=tabtrash[gx][gy]-tabtrash[gx][gy]-25
    if tabsim[gx][gy]==2:
        tabtrash[gx][gy]=tabtrash[gx][gy]-tabtrash[gx][gy]-20
    if tabsim[gx][gy]==4:
        tabtrash[gx][gy]=tabtrash[gx][gy]-tabtrash[gx][gy]-15
    if tabsim[gx][gy]==20:
        tabtrash[gx][gy]=tabtrash[gx][gy]-tabtrash[gx][gy]-5
    

#generowanie miejsca smieci##############################################
#1-szk,2-pl,3=pap
ldomek=0
mp=9
for i2 in range(0,10):
    for j2 in range(0,10):
        if tab[i2][j2]==3:
            ldomek=ldomek+1

#smieci dla rodziny
def gensm(r,a,b,gx,gy):
    tabcost[gx][gy]=0
    if r<=a:
        tabtrash[gx][gy]=1
    if r>a and r<=b:
        tabtrash[gx][gy]=2
    if r>b:
        tabtrash[gx][gy]=3
        
for u in range(0,10):
    print(tabsim[u])
#print(int(lsmieci))
def generatetrash():
    sred()
    for i2 in range(0,10):
        for j2 in range(0,10):
            if tab[i2][j2]==3 and tabtrash[i2][j2]==0:
                sm = random.randint(1,10)
                if tabsim[i2][j2]==1:
                    gensm(sm,1,2,i2,j2)
                if tabsim[i2][j2]==2:
                    gensm(sm,6,8,i2,j2)
                if tabsim[i2][j2]==4:
                    gensm(sm,2,8,i2,j2)
                if tabsim[i2][j2]==20:
                    gensm(sm,4,8,i2,j2)


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

def dec_smieciarka(point,zapziel,zapnieb,zapzol,paliwo,czy_weekend):
    clf=dec()    
    direction=point
    primpoint=point
    a=1
    b=-1
    mzpx=[-1,0,1]
    mzpy=[-1,0,1]
    czy_dom=0
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

'''
def genetic_alghorithm(some_maps):
    for i in some_maps:
        i = randomize_map(i)
    child = compare_maps(some_maps[0],some_maps[1])
    number_of_maps = len(maps)
    for j in range(2,number_of_maps,1):
        child = compare_maps(child,maps[j])
        #child = cut_map(child)
    return child'''

def sort_maps(some_maps):
    values = []
    for i in some_maps:
        values.append(rate_map(i))
    #print(values)
    bubble_sort_highest(values)
    #print(values)
    return some_maps

def genetic_alghorithm(some_maps):
    sort_maps(some_maps)
    for generation in range(0,10):
        #print("number of generation  %d" % (generation))
        some_maps[-1] = make_child(some_maps[0],some_maps[-10])
        #print(rate_map(some_maps[-1]))
        some_maps = sort_maps(some_maps)
    return some_maps[0]

maps = [ [[0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0]] for j in range(100)]

for i in maps:
    randomize_map(i)



#pozycja i szybkosc
tab = genetic_alghorithm(maps)
print(rate_map(tab))
start = startx, starty = set_start(tab)
point = pointx,pointy = set_point(tab)
speed = X
posX = startx*X
posY = starty*Y
screen = pygame.display.set_mode(size)
display = pygame.display.set_mode((size[0],int(size[1]+(size[1]/10)*3)),0,32) #rozmiar ekranu
tabcost = generatecostroad(tab,tabcost)
generatesim()
generatetrash()
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

for ti in range(0,10):
    for tj in range(0,10):
        if tab[ti][tj]==3:
            tabcost[ti][tj]=0

    
while True:
    for sin in range(0,100000):
        sin=1
        #if event.type == QUIT:
         #   pygame.quit()
          #  exit()
        pressedKeys = pygame.key.get_pressed()
        display.fill((255,255,255))##
        screen.blit(glass,(6*X,10*Y))
        screen.blit(paper,(6*X,11*Y))
        screen.blit(plastic,(6*X,12*Y))
        screen.blit(bg2,(0,0))
        screen.blit(glasfull,(zapziel*X,10*Y))
        screen.blit(paperfull,(zapnieb*X,11*Y))
        screen.blit(plasticfull,(zapzol*X,12*Y))
        #rysowanie mapy

        display.blit(cursorSrc, (posX, posY))

#########################ruch
        point = int(posX/X),int(posY/Y)
        path = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        path2 = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
       
        cr()
        end_road=dec_smieciarka(point,zapziel,zapnieb,zapzol,paliwo,czy_weekend)
        tabcost[end_road[0]][end_road[1]]=0
        path = astar(tabcost, point, end_road)
        tabcost[end_road[0]][end_road[1]]=1
        ucr()
        
        for mi in range(0,len(path)):
            
           # print(path[mi])
            
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
                    elif tab[z1][z2]  == 3 and tabtrash[z1][z2]<=0:
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
            time.sleep(0.5)
            if Ruch2(path,mi)=="Left":
                if tab[int(posX/X)-1][int(posY/Y)] == 2:
                    posX -= speed
                cursorSrc=cursorSrcLeft
                if tab[int(posX/X)-1][int(posY/Y)] == 3:
                    if tabtrash[int(posX/X)-1][int(posY/Y)] == 1 and zapziel!=5:
                        collecttrash(int(posX/X)-1,int(posY/Y))
                        zapziel=zapziel+1;
                    elif tabtrash[int(posX/X)-1][int(posY/Y)] == 2 and zapnieb!=5:
                        collecttrash(int(posX/X)-1,int(posY/Y))
                        zapnieb=zapnieb+1;
                    elif tabtrash[int(posX/X)-1][int(posY/Y)] == 3 and zapzol!=5:
                        collecttrash(int(posX/X)-1,int(posY/Y))
                        zapzol=zapzol+1;
                if tab[int(posX/X)-1][int(posY/Y)] == -1:
                    zapziel=0;
                elif tab[int(posX/X)+1][int(posY/Y)] == -2:
                    zapnieb=0;
                elif tab[int(posX/X)+1][int(posY/Y)] == -3:
                    zapzol=0;
                        
            elif Ruch2(path,mi)=="Right":
                if tab[int(posX/X)+1][int(posY/Y)] == 2:
                    posX += speed
                cursorSrc=cursorSrcRight
                if tab[int(posX/X)+1][int(posY/Y)] == 3:
                    if tabtrash[int(posX/X)+1][int(posY/Y)] == 1 and zapziel!=5:
                        collecttrash(int(posX/X)+1,int(posY/Y))
                        zapziel=zapziel+1;
                    elif tabtrash[int(posX/X)+1][int(posY/Y)] == 2 and zapnieb!=5:
                         collecttrash(int(posX/X)+1,int(posY/Y))
                         zapnieb=zapnieb+1;
                    elif tabtrash[int(posX/X)+1][int(posY/Y)] == 3 and zapzol!=5:
                        collecttrash(int(posX/X)+1,int(posY/Y))
                        zapzol=zapzol+1;
                if tab[int(posX/X)+1][int(posY/Y)] == -1:
                    zapziel=0;
                elif tab[int(posX/X)+1][int(posY/Y)] == -2:
                    zapnieb=0;
                elif tab[int(posX/X)+1][int(posY/Y)] == -3:
                    zapzol=0;
                        
            if Ruch2(path,mi)=="Up":
                if tab[int(posX/X)][int(posY/Y)-1] == 2:
                    posY -= speed
                cursorSrc=cursorSrcUp
                if tab[int(posX/X)][int(posY/Y)-1] == 3:
                    if tabtrash[int(posX/X)][int(posY/Y)-1] == 1 and zapziel!=5:
                        collecttrash(int(posX/X),int(posY/Y)-1)
                        zapziel=zapziel+1;
                    elif tabtrash[int(posX/X)][int(posY/Y)-1] == 2 and zapnieb!=5:
                        collecttrash(int(posX/X),int(posY/Y)-1)
                        zapnieb=zapnieb+1;
                    elif tabtrash[int(posX/X)][int(posY/Y)-1] == 3 and zapzol!=5:
                        collecttrash(int(posX/X),int(posY/Y)-1)
                        zapzol=zapzol+1;
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
                        collecttrash(int(posX/X),int(posY/Y)+1)
                        zapziel=zapziel+1;
                    elif tabtrash[int(posX/X)][int(posY/Y)+1] == 2 and zapnieb!=5:
                        collecttrash(int(posX/X),int(posY/Y)+1)
                        zapnieb=zapnieb+1;
                    elif tabtrash[int(posX/X)][int(posY/Y)+1] == 3 and zapzol!=5:
                        collecttrash(int(posX/X),int(posY/Y)+1)
                        zapzol=zapzol+1;
                if tab[int(posX/X)][int(posY/Y)+1] == -1:
                    zapziel=0;
                elif tab[int(posX/X)][int(posY/Y)+1] == -2:
                    zapnieb=0;
                elif tab[int(posX/X)][int(posY/Y)+1] == -3:
                    zapzol=0;

####################################################
        if posX >wight-X:
            posX=wight-X
        elif posX < 0:
            posX=0
        if posY >height-Y:
            posY=height-Y
        elif posY <0:
            posY=0
        
        #print(len(path)-1)
        generatetrash()
        pygame.display.update()
