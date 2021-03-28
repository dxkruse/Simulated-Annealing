# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:52:51 2020

@author: dxkru
"""
import numpy as np

class grid_info:
    def __init__(self, min_x, min_y, max_x, max_y, spacing, robot_radius, start, goal):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.spacing = spacing
        self.size_x = (max_x - min_x)/spacing + 1
        self.size_y = (max_y - min_y)/spacing + 1
        self.robot_radius = robot_radius
        self.start_x = start[0]
        self.start_y = start[1]
        self.goal_x = goal[0]
        self.goal_y = goal[1]

class node:
    def __init__(self, x, y, cost, heuristic, parent_index):
        self.x = x
        self.y = y
        self.cost = cost
        self.heuristic = heuristic
        self.total_cost = cost + heuristic
        self.parent_index = parent_index

class obstacle_list:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def index_calc(x, y, grid_spacing, grid_size_y):
    index = (x/grid_spacing) + (grid_size_y/grid_spacing)*y
    return index

def distance_calc(x1, y1, x2, y2):
    distance = np.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))
    return distance

def collision_check(obstacle_list, node, grid_info):
    #   Initialize collision check to False
    collision = bool(0)
    #   Loop through obstacle list, checking distance from obstacle
    for i in range(0, len(obstacle_list.x)):
        obs_dist = distance_calc(node.x, node.y, obstacle_list.x[i], obstacle_list.y[i])
        #   If too close to obstacle, set collision to True
        if obs_dist < grid_info.robot_radius:
            collision = bool(1)
    #   Reset variables for easier syntax
    min_x = grid_info.min_x
    min_y = grid_info.min_y
    max_x = grid_info.max_x
    max_y = grid_info.max_y
    radius = grid_info.robot_radius
    
    #   If robot is too close to boundary, set collision to True
    if node.x == min_x + radius or node.x == max_x - radius or node.y == min_y + radius or node.y == max_y - radius:
        collision = bool(1)
    return collision

