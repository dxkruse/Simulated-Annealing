# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 17:34:17 2021

@author: Dietrich
"""

import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools 
from copy import deepcopy
          
# Initialize file path
filepath = os.path.dirname(__file__)
filename = os.path.join(filepath, 'roommates.txt')

# Load data
data = pd.read_csv(filename, sep=" ", header=None)
# Remove extra nan column, not sure why that existed.
data = data.dropna(axis=1)

T = 100

# Goal:
#   To find minimum compatibility score, sum of all rooms' compatibility scores 

# Define Classes

class Dorm:
    
    def __init__(self, data, num_rooms):
        self.scoreMatrix = data
        self.num_rooms = num_rooms
        self.totalScore = 0
        self.rooms = pd.DataFrame(index = np.arange(1,num_rooms+1), columns = ["students", "room_score"])
        self.rooms["students"] = self.rooms["students"].astype(object)
    
    def assignRooms(self):
        # Initialize Rooms assignments
        count = 0        
        for index, room in self.rooms.iterrows():
            room.students = pd.Series([count, count+1, count+2, count+3])
            count = count + 4
        
        self.rooms.fillna(0, inplace=True)         
        self.calculateAllRooms()
        self.calculateDormScore()
    
    def calculateRoomScore(self, room):
        
        # If statement handles different inputs allowing for calculation of 
        # score from numpy array if desired.
        
        if type(room) == int:
            # Get all combinations of student pairs in the room
            combos = list(itertools.combinations(self.rooms.loc[room, "students"], 2))
            
            # Loop through combinations, getting compatibility scores for each
            # and adding it to the room score            
            for combo in combos:
                student1 = combo[0]
                student2 = combo[1]            
                self.rooms.loc[room, "room_score"] += self.scoreMatrix.loc[student1, student2]
                
        elif type(room) == np.ndarray:            
            # Get all combinations of student pairs in the room
            combos = list(itertools.combinations(room, 2))
            #print(combos)
            # Loop through combinations, getting compatibility scores for each
            # and adding it to the room score
            room_score = 0
            for combo in combos:
                student1 = combo[0]
                student2 = combo[1]            
                room_score += self.scoreMatrix.loc[student1, student2]
            return room_score
        
    def calculateAllRooms(self):
        for index, room in self.rooms.iterrows():
            room.room_score = self.calculateRoomScore(index)
    
    def calculateDormScore(self):
        self.totalScore = sum(self.rooms.room_score)
    
    def getRandomRooms(self):
        randomRooms = np.random.randint(1, self.num_rooms, size=2)
        if randomRooms[0] == randomRooms[1]:
            randomRooms = np.random.randint(1, self.num_rooms, size=2)
        return randomRooms
    
    def getRandomStudents(self):
        randomStudents = np.random.randint(0,3, size=2)
        if randomStudents[0] == randomStudents[1]:
            randomStudents = np.random.randint(0,3, size=2)
        return randomStudents
    
    def swapOne(self):
        ""
        
        # Generate random rooms and students
        randomRooms = self.getRandomRooms()
        randomStudents = self.getRandomStudents()
        
        # Get room 1 students and score
        room1 = np.asarray(self.rooms.loc[randomRooms[0], "students"].values)
        room1_score = self.rooms.loc[randomRooms[0], "room_score"]
        # Store copy of room 1
        temp_room1 = deepcopy(room1)
        
        # Get room 2 students and score
        room2 = self.rooms.loc[randomRooms[1], "students"].values
        room2_score = self.rooms.loc[randomRooms[1], "room_score"]
        # Store copy of room 2
        temp_room2 = deepcopy(room2)

        # Get IDs of random students
        student1 = self.rooms.loc[randomRooms[0], "students"].values[randomStudents[0]]
        student2 = self.rooms.loc[randomRooms[1], "students"].values[randomStudents[1]]
        
        
        # Create temporary rooms with swapped students
        temp_room1[randomStudents[0]] = student2
        temp_room2[randomStudents[1]] = student1
        # print(room1, temp_room1)
        # print(room2, temp_room2)  
        
        # Calculate temporary room scores
        temp1_score = self.calculateRoomScore(temp_room1)
        temp2_score = self.calculateRoomScore(temp_room2)
        
        # Calculate net score change from room swap
        net_score = (room1_score - temp1_score) + (room2_score - temp2_score)
        print(net_score)
        
        if (net_score < 0):
            print("Swapping student", student1, "from room", randomRooms[0], "with", student2, "from room", randomRooms[1])
            self.rooms.loc[randomRooms[0], "students"][randomStudents[0]] = student2
            self.rooms.loc[randomRooms[1], "students"][randomStudents[1]] = student1
        else:
            probability = np.exp(-(net_score/T))
            print(probability)
        return room1_score
    
def swapTwo(self):
    ""

#%%
dorm = Dorm(data, 50)
dorm.assignRooms()
#%%
score = dorm.swapOne()
#%%
#print(dorm.rooms)


#%%

# Initialize T

# Loop

# Make Random change to current state x; call resulting state y and find score
# of state E(y)

# If E(y) < E(x), make the change. Otherwise, make the change anyway with
# probability np.exp^(-(dE/T))

# Assuming some parameter N characterizing the size of the problem (people to
# assign to rooms) reduce T according to some schedule, every 10N successful
# changes or 100N attempted changes.

# Continue until a cycle with no successful changes, or other stopping
# criterion is reached.

# Does NOT guarantee global optimum. Improvements:
#   Slower cooling, to allow more thorogh exploration
#   Multiple runs with random restarts, take best found of various attempts
