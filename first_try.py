import random
import numpy as np
from matplotlib import pyplot as plt

class District():
    def __init__(self, i, j, crimes0):
        self.i = i              # row
        self.j = j              # column
        self.neighbours = []
        self.crimes = [crimes0]
    
    def find_neigbours(self, map):
        for i in [self.i-1, self.i+1]:
            if i < (map.i_len) and i >= 0:
                self.neighbours.append(map.districts[f"{i},{self.j}"])
        
        for j in [self.j-1, self.j+1]:
            if j < (map.j_len) and j >= 0:
                self.neighbours.append(map.districts[f"{self.i},{j}"])
        
        return self.neighbours
    
    def next_timestep(self, k):
        crime = self.crimes[-1]
        for neighbour in self.neighbours:
            crime += k * (neighbour.crimes[-1] - self.crimes[-1]) / len(self.neighbours)
        self.crimes.append(crime)

class Map():
    def __init__(self, i_len, j_len):
        self.i_len = i_len
        self.j_len = j_len
        self.districts = {}

        for i in range(i_len):
            for j in range(j_len):
                self.districts[f"{i},{j}"] = District(i, j, random.random())

def timesteps(map, n):
    for time in range(n):
        for item in map.districts:
            map.districts[item].next_timestep(0.4)
        

        # plots
        i_list, j_list, colours = [], [], []

        for item in map.districts:
            i, j = item.split(",")
            i_list.append(i)
            j_list.append(j)
            colours.append(map.districts[item].crimes[-1])

        plt.scatter(j_list, i_list, s=100, c=colours, marker="s",)
        plt.title(time)
        plt.axis("square")
        plt.draw()           # update grafiek
        plt.pause(0.5)
        plt.clf()            # clear grafiek
    plt.show()

map = Map(20, 20)
for item in map.districts:
    map.districts[item].find_neigbours(map)

timesteps(map, 100)