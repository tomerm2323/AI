import pandas as pd
import numpy as np

class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def empty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, node):
        self.queue.append(node)

    # for popping an element based on Priority
    def delete(self):
        if self.empty():
            return
        try:
            min_val = float("inf")
            min_node_pos = None
            for i in range(len(self.queue)):
                node = self.queue[i]
                f_val = node[0]
                if f_val < min_val:
                    min_val = f_val
                    min_node_pos = i
            item = self.queue[min_node_pos]
            del self.queue[min_node_pos]
            return item
        except IndexError:
            print()
            exit()

    def remove_from_queue(self, index):
        del self.queue[index]


# The function initializes and returns open
def init_open():
    prq = PriorityQueue()
    return prq

# The function inserts s into open
def insert_to_open(open_list, s):  # Should be implemented according to the open list data structure
    open_list.insert(s)

# The function returns the best node in open (according to the search algorithm)
def get_best(open_list):
    return open_list.delete()

# The function returns neighboring locations of s_location
def get_neighbors(grid, s_location):
    neighbors = []
    cur_x, cur_y = s_location
    grid_size = grid.shape - np.array((1, 1))
    opt_pos = [(cur_x + 1, cur_y),
                   (cur_x + 1 , cur_y + 1),
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

# The function returns whether or not s_location is the goal location
def is_goal(s_location, goal_location):
    return s_location == goal_location

# The function estimates the cost to get from s_location to goal_location
def calculate_heuristic(s_location, goal_location):
    distance = 0
    for s_i, g_i in zip(s_location, goal_location):
        distance += abs(s_i - g_i)
    return distance

# The function returns whether n_location should be generated (checks in open_list)
# removes a node from open_list if needed 
def check_for_duplicates_open(n_location, s, open_list):
    if n_location in open_list.queue:
        n_loc_index = open_list.queue.index(n_location)
        if s[2] + 1 < open_list.queue[n_loc_index][2]:
            open_list.remove_from_queue(n_loc_index)
            open_list.insert(n_location)
            return False
        return True
    return False
  
# The function returns whether n_location should be generated (checks in closed_list)
# removes a node from closed_list if needed  
def check_for_duplicates_close(n_location, s, closed_list):
    if n_location in closed_list:
        return True
    return False

# Locations are tuples of (x, y)
def astar_search(grid, start_location, goal_location):
    # State = (f, h, g, x, y, s_prev) # f = g + h (For Priority Queue)
    # Start_state = (0, 0, 0, x_0, y_0, False)
    start = (0, 0, 0, start_location[0], start_location[1], False)
    open_list = init_open()
    closed_list = {}
    # Mark the source node as
    # visited and enqueue it
    insert_to_open(open_list, start)
    while not open_list.empty():
        # Dequeue a vertex from
        # queue and print it
        s = get_best(open_list)
        s_location = (s[3], s[4])
        if s_location in closed_list:
            continue
        if is_goal(s_location, goal_location):
            print("The number of states visited by AStar Search:", len(closed_list))
            return s
        neighbors_locations = get_neighbors(grid, s_location)
        for n_location in neighbors_locations:
            if check_for_duplicates_open(n_location, s, open_list) or check_for_duplicates_close(n_location, s, closed_list):
                continue
            h = calculate_heuristic(n_location, goal_location)
            g = s[2] + 1
            f = g + h
            n = (f, h, g, n_location[0], n_location[1], s)
            insert_to_open(open_list, n)
        closed_list[s_location] = s

def print_route(s):
    for r in s:
        print(r)

def get_route(s):
    route = []
    while s:
        s_location = (s[3], s[4])
        route.append(s_location)
        s = s[5]
    route.reverse()
    return route

def print_grid_route(route, grid):
    for location in route:
        grid[location] = 'x'
    print(pd.DataFrame(grid))
