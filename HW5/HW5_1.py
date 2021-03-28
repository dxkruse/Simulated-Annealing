# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 20:06:43 2020

@author: dxkru
"""
import utils
import numpy as np

###### PUT ALL INTO UTILS FILE #######
from rrt import rrt
from dijkstras import dijkstras
from astar import astar

import matplotlib.pyplot as plt

## 5.1
#obstacle_list_x = np.array([], dtype = float)
#obstacle_list_y = np.array([], dtype = float)

#5.2
#obstacle_list_x = [4, 3, 5, 5, 0, 1, 2, 3, 4]
#obstacle_list_y = [4, 4, 0, 1, 7, 7, 7, 7, 7]

## 5.3
obstacle_list_x = [2, 2, 2, 2, 0, 1, 2, 3, 4, 5, 5, 5, 5,5, 8, 9, 10, 11, 12, 13, 8, 8, 8, 8, 8, 8, 8, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5, 6, 7, 8, 9, 10, 11, 12, 12, 12, 12, 12]
obstacle_list_y = [2, 3, 4, 5, 5, 5, 5, 5, 5, 5, 2, 3, 4, 5, 2, 2, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8, 9, 7,7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 8, 9, 10, 11, 12, 13, 9, 10, 11, 12, 13, 14, 15, 12, 12, 12, 12, 12, 12, 8, 9, 10, 11, 12]

min_x = 0
min_y = 0
max_x = 15
max_y = 15
spacing = 1
robot_rad = 0.6

start = [1,1]
goal = [7,13]


    
# Initialize Variables    
grid = utils.grid_info(min_x, min_y, max_x, max_y, spacing, robot_rad, start, goal)
obstacle_list = utils.obstacle_list(obstacle_list_x, obstacle_list_y)

rrt_x, rrt_y, rrt_cost, counter = rrt(grid, obstacle_list)
dij_x, dij_y, dij_cost = dijkstras(grid, obstacle_list)
astar_x, astar_y, astar_cost = astar(grid, obstacle_list)

