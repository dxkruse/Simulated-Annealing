# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 15:45:13 2020

@author: dxkru
"""
import utils
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def rrt(grid, obstacle_list):
    
    goal_x = grid.goal_x
    goal_y = grid.goal_y
    nodes = dict()
    
    current_node = utils.node(grid.start_x, grid.start_y, 1000, 0, -1)    
    current_index = utils.index_calc(current_node.x, current_node.y, grid.spacing, grid.size_y)
    nodes[current_index] = current_node
    
    step = 0.5
    distanceThreshold = 1
    
    counter = 0
    lim = 10000  
    
    # Initialize distance to goal
    distanceToGoal = utils.distance_calc(current_node.x, current_node.y, goal_x, goal_y)
    
    for i in tqdm(range(10000)):
    
    # Loop while distance to goal is above threshold
        while distanceToGoal >= distanceThreshold:
            
            #print(counter)
            # Get random coordinate
            rand_x = np.random.rand() * grid.max_x
            rand_y = np.random.rand() * grid.max_y
            
            # Loop through tree and calculate cost from random coordinate to all nodes in tree
            for key in nodes:
                cost = utils.distance_calc(nodes[key].x, nodes[key].y, rand_x, rand_y)
                nodes[key].cost = cost
            
            # Set current node to index of node with min cost
            min_index = min(nodes, key = lambda x: nodes[x].cost)
            current_node = nodes[min_index]
                    
            # Calculate angle from current node to random node
            dist_x = rand_x - current_node.x
            dist_y = rand_y - current_node.y        
            theta = np.arctan2(dist_y, dist_x)
            
            # Set temp node one step from current node in direction of random coordinate
            temp_x = current_node.x + step*np.cos(theta)
            temp_y = current_node.y + step*np.sin(theta)
            temp_index = utils.index_calc(temp_x, temp_y, grid.spacing, grid.size_y)
            temp_node = utils.node(temp_x, temp_y, 0, 0, min_index)
            
            # Same Node/ Collision/ Out of Boundary Check
            same_check = bool(temp_node.x == current_node.x and temp_node.y == current_node.y)
            coll_check = utils.collision_check(obstacle_list, temp_node, grid)
            bound_check = bool(temp_node.x < grid.min_x or temp_node.x > grid.max_x or temp_node.y < grid.min_y or temp_node.y > grid.max_y)
            main_check = bool(same_check == coll_check == bound_check == False)
            
            # If check is passed, add temp node to node tree
            if main_check == True:
                nodes[temp_index] = temp_node
            
            distanceToGoal = utils.distance_calc(temp_node.x, temp_node.y, goal_x, goal_y)
            counter = counter + 1
            
            if counter > lim:
                print("Error: Maximum iterations reached")
                return
                
    
    path_x = np.array([goal_x])
    path_y = np.array([goal_y])
    goal_index = utils.index_calc(goal_x, goal_y, grid.spacing, grid.size_y)
    goal_pindex = nodes[temp_index].parent_index
    goal_cost = utils.distance_calc(temp_x,temp_y,goal_x,goal_y)
    goal = utils.node(goal_x, goal_y, goal_cost, 0, goal_pindex)
    nodes[goal_index] = goal
    
    parent = nodes[goal_index].parent_index
    
    while parent != -1:
        path_x = np.append(path_x, nodes[parent].x)
        path_y = np.append(path_y, nodes[parent].y)
        parent = nodes[parent].parent_index

    plt.plot(path_x, path_y, label="RRT")
    plt.scatter(obstacle_list.x, obstacle_list.y)
    plt.grid(True)
        
    goal_cost = len(path_x) * step
    path_x = np.flip(path_x)
    path_y = np.flip(path_y)
    
    return path_x, path_y, goal_cost, counter