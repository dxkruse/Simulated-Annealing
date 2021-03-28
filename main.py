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
import time


          
# Initialize file path
filepath = os.path.dirname(__file__)
filename = os.path.join(filepath, 'roommates.txt')

# Load data
data = pd.read_csv(filename, sep=" ", header=None)
# Remove extra nan column, not sure why that existed.
data = data.dropna(axis=1)
T = 1000

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
        self.successfulSwaps = 0
        self.attemptedSwaps = 0
        self.consecutiveAttempts = 0
    
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
        room_score = 0
        if type(room) == int:
            print("int")
            # Get all combinations of student pairs in the room
            combos = list(itertools.combinations(self.rooms.loc[room, "students"], 2))
            print(combos)
            # Loop through combinations, getting compatibility scores for each
            # and adding it to the room score            
            for combo in combos:
                student1 = combo[0]
                print(student1)
                student2 = combo[1]
                print(student2)
                print(self.scoreMatrix.loc[student1, student2])
                room_score += self.scoreMatrix.loc[student1, student2]
                #self.rooms.loc[room, "room_score"] += self.scoreMatrix.loc[student1, student2]            
                print(room_score)
            self.rooms.loc[room, "room_score"] = room_score
            print(self.rooms.loc[room, "room_score"])
                
        elif type(room) == np.ndarray:            
            # Get all combinations of student pairs in the room
            combos = list(itertools.combinations(room, 2))
            #print(combos)
            # Loop through combinations, getting compatibility scores for each
            # and adding it to the room score
            
            for combo in combos:
                student1 = combo[0]
                student2 = combo[1]            
                room_score += self.scoreMatrix.loc[student1, student2]
            return room_score
        
    def calculateAllRooms(self):
        for index, room in self.rooms.iterrows():
            room.room_score = self.calculateRoomScore(index)
    
    def calculateDormScore(self):
        #self.calculateAllRooms()
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
        rm1_net = (temp1_score - room1_score)
        rm2_net = (temp2_score - room2_score)
        net_score = rm1_net + rm2_net
        # print(net_score)
        
        
        if (net_score < 0):
            
            print("Swapping Student", [student1], "from Room", randomRooms[0],
                  "with Student", [student2], "from Room", randomRooms[1])
            self.rooms.loc[randomRooms[0], "students"][randomStudents[0]] = student2
            self.rooms.loc[randomRooms[1], "students"][randomStudents[1]] = student1

            self.rooms.loc[randomRooms[0], "room_score"] = self.calculateRoomScore(randomRooms[0])
            self.rooms.loc[randomRooms[1], "room_score"] = self.calculateRoomScore(randomRooms[1])
            # self.rooms.loc[randomRooms[0], "room_score"] += rm1_net
            # self.rooms.loc[randomRooms[1], "room_score"] += rm2_net
            
            # print("Old RM1 score:", room1_score)
            # print("New RM1 score:", temp1_score)
            # print("Old RM2 score:", room2_score)
            # print("New RM2 score:", temp2_score)
            # print("Net Score:", net_score)
            
            self.successfulSwaps += 1
            self.consecutiveAttempts = 0
            self.totalScore += net_score
            
        else:
            
            probability = np.exp(-(net_score/T))
            # print(probability)
            if (np.random.random() <= probability):
                print("Net score higher, swapping Student", [student1], 
                      "from Room", randomRooms[0], "with Student", [student2], 
                      "from Room", randomRooms[1], "anyway")
                self.rooms.loc[randomRooms[0], "students"][randomStudents[0]] = student2
                self.rooms.loc[randomRooms[1], "students"][randomStudents[1]] = student1
                
                self.rooms.loc[randomRooms[0], "room_score"] = self.calculateRoomScore(randomRooms[0])
                self.rooms.loc[randomRooms[1], "room_score"] = self.calculateRoomScore(randomRooms[1])
                
                # self.rooms.loc[randomRooms[0], "room_score"] += rm1_net
                # self.rooms.loc[randomRooms[1], "room_score"] += rm2_net
                

                # print("Old RM1 score:", room1_score)
                # print("New RM1 score:", temp1_score)
                # print("Old RM2 score:", room2_score)
                # print("New RM2 score:", temp2_score)
                # print("Net Score:", net_score)
                
                
                self.successfulSwaps += 1
                self.consecutiveAttempts = 0
                self.totalScore += net_score
            else:
                print("No successful changes were made.")
                self.attemptedSwaps += 1
                self.consecutiveAttempts += 1

        return net_score
    
    def swapTwo(self):

        randomRooms = self.getRandomRooms()
        student1 = self.rooms.loc[randomRooms[0], "students"].values[0]
        student2 = self.rooms.loc[randomRooms[0], "students"].values[1]
        student3 = self.rooms.loc[randomRooms[1], "students"].values[2]
        student4 = self.rooms.loc[randomRooms[1], "students"].values[3]
        
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

        
        # Create temporary rooms with swapped students
        temp_room1[0] = student3
        temp_room1[1] = student4
        temp_room2[2] = student1
        temp_room2[3] = student2
        
        # print(room1, temp_room1)
        # print(room2, temp_room2)  
        
        # # Calculate temporary room scores
        temp1_score = self.calculateRoomScore(temp_room1)
        temp2_score = self.calculateRoomScore(temp_room2)
        
        
        rm1_net = (temp1_score - room1_score)
        rm2_net = (temp2_score - room2_score)
        net_score = rm1_net + rm2_net
        # # Calculate net score change from room swap
        #print(net_score)        
        
        if (net_score < 0):
            
            print("Swapping Students", [student1, student2], "from Room", randomRooms[0], "with Students", 
                      [student3, student4], "from Room", randomRooms[1])
            self.rooms.loc[randomRooms[0], "students"][0] = student3
            self.rooms.loc[randomRooms[0], "students"][1] = student4
            self.rooms.loc[randomRooms[1], "students"][2] = student1
            self.rooms.loc[randomRooms[1], "students"][3] = student2
            
            self.rooms.loc[randomRooms[0], "room_score"] = self.calculateRoomScore(randomRooms[0])
            self.rooms.loc[randomRooms[1], "room_score"] = self.calculateRoomScore(randomRooms[1])
            
            # self.rooms.loc[randomRooms[0], "room_score"] += rm1_net
            # self.rooms.loc[randomRooms[1], "room_score"] += rm2_net
            
            # print("Old RM1 score:", room1_score)
            # print("New RM1 score:", temp1_score)
            # print("Old RM2 score:", room2_score)
            # print("New RM2 score:", temp2_score)
            # print("Net Score:", net_score)
            
            
            self.successfulSwaps += 1
            self.consecutiveAttempts = 0
            self.totalScore += net_score
            
        else:
            
            probability = np.exp(-(net_score/T))
            #print(probability)
            if (np.random.random() <= probability):
                print("Net score higher, swapping Students", [student1, 
                      student2], "from Room", randomRooms[0], "with Students", 
                      [student3, student4], "from Room", randomRooms[1], "anyway.")
                self.rooms.loc[randomRooms[0], "students"][0] = student3
                self.rooms.loc[randomRooms[0], "students"][1] = student4
                self.rooms.loc[randomRooms[1], "students"][2] = student1
                self.rooms.loc[randomRooms[1], "students"][3] = student2
                
                self.rooms.loc[randomRooms[0], "room_score"] = self.calculateRoomScore(randomRooms[0])
                self.rooms.loc[randomRooms[1], "room_score"] = self.calculateRoomScore(randomRooms[1])
                
                # self.rooms.loc[randomRooms[0], "room_score"] += rm1_net
                # self.rooms.loc[randomRooms[1], "room_score"] += rm2_net
               
                # print("Old RM1 score:", room1_score)
                # print("New RM1 score:", temp1_score)
                # print("Old RM2 score:", room2_score)
                # print("New RM2 score:", temp2_score)
                # print("Net Score:", net_score)
                
                
                self.successfulSwaps += 1
                self.consecutiveAttempts = 0
                self.totalScore += net_score
                
            else:
                
                print("No successful changes were made.")
                self.attemptedSwaps += 1
                self.consecutiveAttempts += 1

        # return net_score

dorm = Dorm(data, 50)
dorm.assignRooms()


#%%
dorm.swapOne()


#%%
dorm.swapTwo()


#%%

startTime = time.time()
# Initialize T
iterations = 1000000
T = 1000
N = 0.95
# Loop

for i in range(iterations):
    
    # Assuming some parameter N characterizing the size of the problem (people to
    # assign to rooms) reduce T according to some schedule, every 10N successful
    # changes or 100N attempted changes.
    if (dorm.successfulSwaps % 2000 == 0 or dorm.attemptedSwaps % 20000 == 0):
        T = N*T
    
    # Repeat until 20,000 attempts without successful change
    if (dorm.consecutiveAttempts >= 20000):
        print("Reached 20,000 attempts without a successful change")
        break
        
    # Make Random change to current state x; call resulting state y and find
    # score of state E(y).
    # If E(y) < E(x), make the change. Otherwise, make the change anyway with
    # probability np.exp^(-(dE/T))
    change = np.random.randint(0,2)
    if (change == 0):
        dorm.swapOne()
    else:
        dorm.swapTwo()
        

executionTime = (time.time() - startTime)
print("Execution time:", str(np.round(executionTime, 3)), "seconds \n",
      "Iterations:", i)
# Assuming some parameter N characterizing the size of the problem (people to
# assign to rooms) reduce T according to some schedule, every 10N successful
# changes or 100N attempted changes.

# Continue until a cycle with no successful changes, or other stopping
# criterion is reached.

# Does NOT guarantee global optimum. Improvements:
#   Slower cooling, to allow more thorogh exploration
#   Multiple runs with random restarts, take best found of various attempts
