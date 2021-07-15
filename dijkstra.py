import numpy as np
import random
import re
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)


pygame.init()

#Initialise pygame
pygame.init()

#Constants
HEIGHT = 800
WIDTH = 800
BLOCKSIZE = 50
START_COLOUR = (0,255,100)
END_COLOUR = (255,100,0)
WALL_COLOUR = (200,200,200)
PATH_COLOUR = (0,255,200)

#Create window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra")

def dijkstra(graph, start, end):
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph
    infinity = 999999999999
    path = []

    #Set shortest distance to all nodes to "infinity"
    for node in unseenNodes:
        shortest_distance[node] = infinity
    #Set shortest distance to start node to 0 as it is the starting point
    shortest_distance[start] = 0

    #While unseenNodes isn't None
    #Loops until all nodes have been visited
    while unseenNodes:
        minNode = None
        #Finds node with the shortest distance
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node
        
        #For every connected node and weight at minNode
        #If this is a closer path to get there then change the shortest distance for the child node
        #Set the predecessor to the child node to be minNode, used to create path
        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode
        #Removes node from unseen nodes
        unseenNodes.pop(minNode)
    
    #Work back from the end to the start forming the shortest path
    currentNode = end
    while currentNode != start:
        try:
            path.insert(0, currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print("ERROR NO PATHS AVAILABLE")
            break
    path.insert(0, start)
    #Print shortest distance and the path of nodes
    if shortest_distance[end] != infinity:
        print("Shortest distance is: ", shortest_distance[end])
        print("Path: ", path)

    return path

def create_graph():
    global grid

    #Get neighbours from grid or point x, y
    #Return dictionary of neighbours
    def neighbours(x, y):
        #All distances are 1 as graph is a gridwith nodes on all integer x, y
        neighbours = {}
        #Up
        if (y - 1 >= 0) and (grid[x][y - 1] == 0):
            tup = (x, y - 1)
            neighbours[str(tup)] = 1
        #Down
        if (y + 1 < int(HEIGHT//BLOCKSIZE)) and (grid[x][y + 1] == 0):
            tup = (x, y + 1)
            neighbours[str(tup)] = 1
        #Left
        if (x - 1 >= 0) and (grid[x - 1][y] == 0):
            tup = (x - 1, y)
            neighbours[str(tup)] = 1
        #Right
        if (x + 1 < int(WIDTH//BLOCKSIZE)) and (grid[x + 1][y] == 0):
            tup = (x + 1, y)
            neighbours[str(tup)] = 1

        #print(neighbours)

        return neighbours

    #All nodes on grid (all points not walls)
    nodes = []
    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            if grid[x][y] != 1:
                nodes.append(str((x, y)))

    #Dictionary of neighbouring nodes and distances to them
    distances = {}
    for node in nodes:
        #Node is a string so use regex to get x, y values
        nums = re.findall(r'\d+', node)
        #Find neighbours of node
        node_dict = neighbours(int(nums[0]), int(nums[1]))
        #Add neighbours and distanced to distances dictionary at key node
        distances[node] = node_dict
    #print(distances)
    #Return distances which is the graph form of grid
    return distances

def draw_grid(start_point, end_point, path):
    sx = int(start_point[0])
    sy = int(start_point[1])
    ex = int(end_point[0])
    ey = int(end_point[1])
    if grid[sx][sy] == 1:
        grid[sx][sy] = 0
    if grid[ex][ey] == 1:
        grid[ex][ey] = 0
    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            if grid[x][y] == 1:
                pygame.draw.rect(WINDOW, WALL_COLOUR, (x * BLOCKSIZE, y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
            else:
                pygame.draw.rect(WINDOW, (255,255,255), (x * BLOCKSIZE, y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))


    if path != None:
        for p in path:
            nums = re.findall(r'\d+', p)
            #print(nums)
            pygame.draw.rect(WINDOW, PATH_COLOUR, (int(nums[0]) * BLOCKSIZE, int(nums[1]) * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))

    pygame.draw.rect(WINDOW, START_COLOUR, (sx * BLOCKSIZE, sy * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    pygame.draw.rect(WINDOW, END_COLOUR, (ex * BLOCKSIZE, ey * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))

def draw_squares():
    for x in range(0, WIDTH, BLOCKSIZE):
        pygame.draw.line(WINDOW, (0,0,0), (x, 0), (x, HEIGHT), 1)
    
    for y in range(0, HEIGHT, BLOCKSIZE):
        pygame.draw.line(WINDOW, (0,0,0), (0, y), (WIDTH, y), 1)

def draw_window(grid, start_point, end_point, path):
    #Clear window
    WINDOW.fill((255, 255, 255))

    draw_grid(start_point, end_point, path)

    draw_squares()

    #Update display
    pygame.display.update()

def event_loop():
    global place_objects
    #Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            #If space bar is pressed, stop allowing objects to be placed and reset border
            if event.key == K_SPACE:
                place_objects = False
        #If mouse button is down then place object in grid
        if event.type == pygame.MOUSEBUTTONDOWN:
            if place_objects:
                mouse_pos = pygame.mouse.get_pos()
                #Add or remove walls
                if grid[mouse_pos[0]//BLOCKSIZE][mouse_pos[1]//BLOCKSIZE] == 1:
                    grid[mouse_pos[0]//BLOCKSIZE][mouse_pos[1]//BLOCKSIZE] = 0
                    
                elif grid[mouse_pos[0]//BLOCKSIZE][mouse_pos[1]//BLOCKSIZE] == 0:
                    grid[mouse_pos[0]//BLOCKSIZE][mouse_pos[1]//BLOCKSIZE] = 1


def main():
    global grid, place_objects
    clock = pygame.time.Clock()

    #GRID:
    #0:Empty space
    #1:Wall
    #Create grid and get random  start and end points
    grid = np.zeros((int(WIDTH//BLOCKSIZE), int(HEIGHT//BLOCKSIZE)), dtype=int)
    sx = random.randint(0, int(WIDTH//BLOCKSIZE) - 1)
    sy = random.randint(0, int(HEIGHT//BLOCKSIZE) - 1)
    start_point = (sx, sy)
    ex = random.randint(0, int(WIDTH//BLOCKSIZE) - 1)
    ey = random.randint(0, int(HEIGHT//BLOCKSIZE) - 1)
    while sx == ex and sy == ey:
        ex = random.randint(0, int(WIDTH//BLOCKSIZE) - 1)
        ey = random.randint(0, int(HEIGHT//BLOCKSIZE) - 1)
    end_point = (ex, ey)

    print(start_point, end_point)

    #Main loop
    path = None
    place_objects = True
    make_graph = False
    running = True
    while running:
        event_loop()
        

        if not place_objects:
            if not make_graph:
                #Convert grid array to graph with Empty space being nodes
                graph = create_graph()
                make_graph = True
                #Gets shortest path using dijkstra's algorithm
                path = dijkstra(graph, str(start_point), str(end_point))

        clock.tick(30)
        draw_window(grid, start_point, end_point, path)

main()