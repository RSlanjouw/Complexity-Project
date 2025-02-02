import random
import numpy as np
from matplotlib import pyplot as plt

class District():
    def __init__(self, i, j, crimes0):
        self.i = i              # row
        self.j = j              # column
        self.neighbours = []
        self.crimes_over_time = [crimes0]

    def find_neigbours(self, map):
        for i in [self.i-1, self.i+1]:
            if i < (map.i_len) and i >= 0:
                self.neighbours.append(map.districts[f"{i},{self.j}"])

        for j in [self.j-1, self.j+1]:
            if j < (map.j_len) and j >= 0:
                self.neighbours.append(map.districts[f"{self.i},{j}"])

        return self.neighbours

    def manning_transition(self, k):
        """
        This transition rule is based on the transition rule proposed by Manning.
        """
        crime = self.crimes_over_time[-1]
        for neighbour in self.neighbours:
            # needs to take neighbours previous timestep but some neighbours are not on next timestep yet and others are
            if len(self.crimes_over_time) == len(neighbour.crimes_over_time):
                crime += k * (self.crimes_over_time[-1] - neighbour.crimes_over_time[-1]) / len(self.neighbours)
            else:
                crime += k * (self.crimes_over_time[-1] - neighbour.crimes_over_time[-2]) / len(self.neighbours)
        self.crimes_over_time.append(crime)
        return crime
    
    def manning_transition2(self, k):
        """
        This transition rule is based on the transition rule proposed by Manning. There is an
        adaptation that the difference is taken as (neighbour.crimes_over_time[-1] - self.crimes_over_time[-1])
        instead of (self.crimes_over_time[-1] - neighbour.crimes_over_time[-1]) as proposed by Manning.
        """
        crime = self.crimes_over_time[-1]
        for neighbour in self.neighbours:
            # needs to take neighbours previous timestep but some neighbours are not on next timestep yet and others are
            if len(self.crimes_over_time) == len(neighbour.crimes_over_time):
                crime += k * (neighbour.crimes_over_time[-1] - self.crimes_over_time[-1]) / len(self.neighbours)
            else:
                crime += k * (neighbour.crimes_over_time[-2] - self.crimes_over_time[-1]) / len(self.neighbours)
        self.crimes_over_time.append(crime)
        return crime
    
    def transition2(self, n, p):
        """
        This transition rule has separate parameters for neighbours exerting positive and negative influence.

        n: negative influence parameter
        p: positive influence parameter
        """
        crime = self.crimes_over_time[-1]
        for neighbour in self.neighbours:
            if len(self.crimes_over_time) == len(neighbour.crimes_over_time):
                if neighbour.crimes_over_time[-1] - self.crimes_over_time[-1] > 0:
                    crime += n * (neighbour.crimes_over_time[-1]- self.crimes_over_time[-1]) / len(self.neighbours)
                if neighbour.crimes_over_time[-1] - self.crimes_over_time[-1] < 0:
                    crime += p * (neighbour.crimes_over_time[-1] - self.crimes_over_time[-1]) / len(self.neighbours)

            else:
                if neighbour.crimes_over_time[-2] - self.crimes_over_time[-1] > 0:
                    crime += n * (neighbour.crimes_over_time[-2] - self.crimes_over_time[-1]) / len(self.neighbours)
                if neighbour.crimes_over_time[-2] - self.crimes_over_time[-1] < 0:
                    crime += p * (neighbour.crimes_over_time[-2] - self.crimes_over_time[-1]) / len(self.neighbours)
        self.crimes_over_time.append(crime)
        return crime
    
    def transition3(self, k):
        crime = (1-k) * self.crimes_over_time[-1]
        for neighbour in self.neighbours:
            if len(self.crimes_over_time) == len(neighbour.crimes_over_time):
                crime += k/2 * neighbour.crimes_over_time[-1]

            else:
                crime += k/2 * neighbour.crimes_over_time[-2]
        self.crimes_over_time.append(crime)
        return crime

class Map():
    def __init__(self, i_len, j_len):
        self.i_len = i_len
        self.j_len = j_len
        self.districts = {}

        for i in range(i_len):
            for j in range(j_len):
                # if i == 50 and j == 50:
                #     self.districts[f"{i},{j}"] = District(i, j, 0.5)
                # else:
                #     self.districts[f"{i},{j}"] = District(i, j, 0)
                self.districts[f"{i},{j}"] = District(i, j, random.random())

    def reset(self):
        for key in self.districts:
            self.districts[key].crimes_over_time = [self.districts[key].crimes_over_time[0]]
            self.districts[key].neighbours = []
        return self

    def set_4neighbours(self):
        for key in self.districts:
            district = self.districts[key]
            for i in [district.i-1, district.i+1]:
                if i < (map.i_len) and i >= 0:
                    district.neighbours.append(map.districts[f"{i},{district.j}"])

            for j in [district.j-1, district.j+1]:
                if j < (map.j_len) and j >= 0:
                    district.neighbours.append(map.districts[f"{district.i},{j}"])

        return map

    def set_8neighbours(self):
        for key in self.districts:
            district = self.districts[key]
            for i in [district.i-1, district.i, district.i+1]:
                for j in [district.j-1, district.j, district.j+1]:
                    if i < (map.i_len) and i >= 0 and j < (map.j_len) and j >= 0:
                        if i != district.i or j != district.j:
                            district.neighbours.append(map.districts[f"{i},{j}"])

        return map

def police_intervention(district):
    if district.crimes_over_time[-1] >= 0.8:
        district.crimes_over_time[-1] = 0
        # for neighbour in district.neighbours:
        #     neighbour.crimes_over_time[-1] += 0.05

def timesteps(map, num_timesteps, n, p):
    for timestep in range(num_timesteps):        
        # for item in map.districts:
        #     police_intervention(map.districts[item])

        # plots
        i_list, j_list, colours = [], [], []

        for item in map.districts:
            i, j = item.split(",")
            i_list.append(i)
            j_list.append(j)
            colours.append(map.districts[item].manning_transition2(1))

        plt.scatter(j_list, i_list, s=5, c=colours, marker="s", cmap="binary", vmin=0, vmax=1)
        plt.title(timestep)
        plt.axis("square")
        plt.axis('off')
        plt.colorbar()
        plt.draw()     
        plt.pause(0.1)
        plt.clf()            
    plt.show()

map = Map(100, 100)
map.set_8neighbours()
timesteps(map, 10, 0.3, 0.3)