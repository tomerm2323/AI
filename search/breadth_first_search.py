import pandas as pd
import numpy as np
import queue

class Queue():

    def __init__(self):
        self.items = []

    def empty(self):
        return self.items == []

    def size(self):
        # size of the list
        return len(self.items)

    def enqueue(self, item):
        # insert the item in the front of the list
        self.items.insert(0, item)

    def dequeue(self):
        # removes and returns the last item in the list
        return self.items.pop()


# The function initializes and returns open
def init_open():
    q = Queue()
    return q

# The function inserts s into open
def insert_to_open(open_list, s):  # Should be implemented according to the open list data structure
    open_list.enqueue(s)

# The function returns the best node in open (according to the search algorithm)
def get_best(open_list):
    a_node = open_list.dequeue()
    return a_node

# The function returns neighboring locations of s_location
def get_neighbors(grid, s_location):
    neighbors = []
    cur_x, cur_y = s_location
    grid_size = grid.shape - np.array((1, 1))
    opt_pos = [(cur_x + 1, cur_y),
                   (cur_x + 1, cur_y + 1),
                   (cur_x + 1, cur_y -1 ),
                   (cur_x, cur_y),
                   (cur_x , cur_y + 1),
                   (cur_x, cur_y -1),
                   (cur_x - 1, cur_y),
                   (cur_x - 1, cur_y + 1),
                   (cur_x - 1, cur_y - 1)
               ]
    for pos in opt_pos:
        x, y = pos
        if x >= 0 and x <= grid_size[0] and y >= 0 and y <= grid_size[-1] and str(grid[x, y]) != '@':
            neighbors.append(pos)
    return neighbors

# The function returns whether n_location should be generated (checks in open_list)
# removes a node from open_list if needed 
def check_for_duplicates_open(n_location, s, open_list):
    return n_location in open_list.items

  
# The function returns whether n_location should be generated (checks in closed_list)
# removes a node from closed_list if needed  
def check_for_duplicates_close(n_location, s, closed_list):
    return n_location in closed_list

# The function returns whether or not s_location is the goal location
def is_goal(s_location, goal_location):
    return s_location == goal_location

# Locations are tuples of (x, y)
def bfs(grid, start_location, goal_location):
    # State = (x, y, s_prev)
    # Start_state = (x_0, y_0, False)
    open_list = init_open()
    closed_list = {}

    # Mark the source node as
    # visited and enqueue it
    start = (start_location[0], start_location[1], False)
    insert_to_open(open_list, start)

    while not open_list.empty():
        # Dequeue a vertex from
        # queue and print it
        s = get_best(open_list)
        # print(s, end=" ")
        s_location = (s[0], s[1])
        if s_location in closed_list:
            continue
        if is_goal(s_location, goal_location):
            print("The number of states visited by BFS:", len(closed_list))
            return s
        neighbors = get_neighbors(grid, s_location)
        for n_location in neighbors:
            if check_for_duplicates_open(n_location, s, open_list) or check_for_duplicates_close(n_location, s, closed_list):
                continue
            n = (n_location[0], n_location[1], s)
            insert_to_open(open_list, n)
        closed_list[s_location] = s

def print_route(s):
    while s:
        print(s[0], s[1])
        s = s[3]

def get_route(s):
    route = []
    while s:
        s_location = (s[0], s[1])
        route.append(s_location)
        s = s[2]
    route.reverse()
    return route

def print_grid_route(route, grid):
    for location in route:
        grid[location] = 'x'
    print(pd.DataFrame(grid))
