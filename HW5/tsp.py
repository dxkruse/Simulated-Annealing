# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 22:06:05 2020

@author: Dietrich
"""

import utils
from itertools import permutations
import numpy as np
from math import factorial
import matplotlib.pyplot as plt
from astar import astar

min_x = 0
min_y = 0
max_x = 15
max_y = 15
spacing = 1
robot_rad = 0.6
obstacle_list = utils.obstacle_list([], [])
wayX = [0,2,5,3,6]
wayY = [0,2,3,4,4]

# Initialize paths dictionary
paths = dict()

# Get permutations
perms = list(permutations([0,1,2,3,4]))
# Get only permutations that begin at 0
perms = perms[0:factorial(4)]

# Initialize cost table
cost_table = np.zeros((len(wayX),len(wayY)))
# Initialize waypoints dictionary
waypoints = dict()

# Loop through waypoints, create nodes for each, add to waypoints dictionary
for i in range(len(wayX)):
      way_node = utils.node(wayX[i], wayY[i], 0, 0, 0)
      waypoints[i] = way_node
      
# Create table of costs between each waypoint
for i in range(len(wayX)):
    for j in range(len(wayY)):
        start = [waypoints[i].x, waypoints[i].y]
        goal = [waypoints[j].x, waypoints[j].y]
        grid = utils.grid_info(min_x, min_y, max_x, max_y, spacing, robot_rad, start, goal)
        
        if i == j:
            cost_table[i,j] = 0
        else:
            path_x, path_y, cost = astar(grid, obstacle_list)
            cost_table[i,j] = cost
            
for i in range(len(perms)):
    perm_index = i
    perm = np.asarray(perms[i])
    cost = 0
    for j in range(len(perm) - 1):
        cost = cost + cost_table[j,j+1]
        
        
    
    
    
    
            
            
            

