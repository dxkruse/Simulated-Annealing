# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 15:45:13 2020

@author: dxkru
"""
import utils
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def dijkstras(grid, obstacle_list):
    
    goal_x = grid.goal_x
    goal_y = grid.goal_y
    unvisited_nodes = dict()
    visited_nodes = dict()
    current_node = utils.node(grid.start_x,grid.start_y,0,0,-1)
    current_index = utils.index_calc(current_node.x, current_node.y, grid.spacing, grid.size_y)
    unvisited_nodes[current_index] = current_node
    
    for i in tqdm(range(10000)):
    
        while current_node.x != goal_x or current_node.y != goal_y:
            # Calculate index of node in unvisited nodes with lowest cost
            min_index = min(unvisited_nodes, key = lambda x: unvisited_nodes[x].cost)    
            # Travel to node at min_index
            current_index = min_index
            current_node = unvisited_nodes[current_index]   
            # Put current node in visited dict and delete from unvisited dict
            visited_nodes[current_index] = current_node
            del unvisited_nodes[current_index]
            # Check if goal is reached
            if current_node.x == goal_x and current_node.y == goal_y:
                break
            
            # Loop through neighboring nodes
            # MAKE FUNCTION
            for i in np.arange(-grid.spacing, grid.spacing + grid.spacing, grid.spacing):
                for j in np.arange(-grid.spacing, grid.spacing + grid.spacing, grid.spacing):
                    temp_x = current_node.x + i
                    temp_y = current_node.y + j
                    cost = utils.distance_calc(current_node.x, current_node.y, temp_x, temp_y) + current_node.cost
                    temp_node = utils.node(temp_x, temp_y, cost, 0, current_index)
                    temp_index = utils.index_calc(temp_node.x, temp_node.y, grid.spacing, grid.size_y)
                    
                    # Put all checks in one function?
                    same_check = bool(temp_node.x == current_node.x and temp_node.y == current_node.y)
                    coll_check = utils.collision_check(obstacle_list, temp_node, grid)
                    bound_check = bool(temp_node.x < grid.min_x or temp_node.x > grid.max_x or temp_node.y < grid.min_y or temp_node.y > grid.max_y)
                    main_check = bool(same_check == coll_check == bound_check == False)
                    
                    
                    if main_check == True:
                        if unvisited_nodes.get(temp_index, False) == True  and temp_node.cost < unvisited_nodes[temp_index].cost:
                            unvisited_nodes[temp_index].cost = temp_node.cost 
                            unvisited_nodes[temp_index].parent_index = temp_node.parent_index
                        elif unvisited_nodes.get(temp_index, False) == False and visited_nodes.get(temp_index, False) == False:
                            unvisited_nodes[temp_index] = temp_node        
                
    
    path_x = np.array([goal_x])
    path_y = np.array([goal_y])
    goal_index = utils.index_calc(goal_x, goal_y, grid.spacing, grid.size_y)
    parent = visited_nodes[goal_index].parent_index
    
    while parent != -1:
        path_x = np.append(path_x, visited_nodes[parent].x)
        path_y = np.append(path_y, visited_nodes[parent].y)
        parent = visited_nodes[parent].parent_index
    
    plt.plot(path_x, path_y, label="Dijkstras")
    plt.scatter(obstacle_list.x, obstacle_list.y)
    plt.grid(True)
    plt.legend()
    
    
    path_x = np.flip(path_x)
    path_y = np.flip(path_y)
    return path_x, path_y, visited_nodes[goal_index].cost