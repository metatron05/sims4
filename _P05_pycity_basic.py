
# Standard modules from Python
import argparse
import time
import os
import collections
import pandas as pd
import random

# External modules from Anaconda distribution
import numpy as np

# External modules from PyPi
try:
    import keyboard
except:
    print("Warning: no real-time keyboard/hotkey support.")

p = argparse.ArgumentParser(description="City simulation in Python.")
p.add_argument("-m", dest="m", type=int, default=30, help="Width of surface (default 30)")
p.add_argument("-n", dest="n", type=int, default=30, help="Height of surface (default 30)")
p.add_argument("-t", dest="t", type=int, default=1, help="Update interval (s) (default 1s)")
args = p.parse_args()

#Parent class
class Field:
    def __init__(self, char):
        self.char = char
        self.value = 0

#Subclasses
class Land(Field):
    def __init__(self):
        Field.__init__(self, "..")

class Water(Field):
    def __init__(self):
        Field.__init__(self, "🌊")

class Resident(Field):
    def __init__(self):
        Field.__init__(self, "🏠")

class Business(Field):
    def __init__(self):
        Field.__init__(self, "🏭")

class Street(Field):
    def __init__(self):
        Field.__init__(self, "██")

class Car(Field):
    def __init__(self):
        Field.__init__(self, "🚘")

#Map
class Surface:
    def __init__(self, m, n):
        self.surface = np.full((m, n), Land())
        self.m = m
        self.n = n
        self.oldcardirection = ()

        #load and replace Map (Dataframe) with classes
        self.df = pd.read_csv("map.csv", sep=";")
        self.df = self.repair_map(self.df)

    def repair_map(self, map):
        map = map.replace(["w"], Water())
        map = map.replace(["s"], Street())
        map = map.replace(["h"], Resident())
        map = map.replace(["f"], Business())
        map = map.replace([np.nan], Land())
        return map

    def draw(self):
        #draw Map
        if(self.carexists() == False):
            self.insertcar()                

        for index, row in self.df.iterrows():
            for column in row:
                #Print Class Characters (Variable char)
                try:
                    print(column.char, end="")
                except:
                    print("..")
            print()

    def insertcar(self):
        for col in self.df.columns:
            for idx, value in self.df[col].items():
                if isinstance(value, Street):
                    self.df.at[idx, col] = Car()
                    return self.df
                
    def carexists(self):
        for col in self.df.columns:
            for idx, value in self.df[col].items():
                if isinstance(value, Car):
                    return idx, col
                
        return False
    
    def drivecar(self):
        currentcarposition = self.carexists()
        direction = self.getnewdirection(currentcarposition)
        self.df.at[currentcarposition[0], currentcarposition[1]] = Street()
        self.df.at[direction[0], direction[1]] = Car()
        self.oldcardirection = currentcarposition

    def getnewdirection(self, currentcarposition):
        direct = currentcarposition
        for i in range(100):
            number = random.randint(1,4)
            #Right
            if(number == 1):
                if(isinstance(self.df.at[direct[0], str(int(direct[1])+1)], Street)):
                    if((direct[0], str(int(direct[1])+1)) != self.oldcardirection):
                        return (direct[0], str(int(direct[1])+1))
            #Left
            if(number == 2):
                if(isinstance(self.df.at[direct[0], str(int(direct[1])-1)], Street)):
                    if((direct[0], str(int(direct[1])-1)) != self.oldcardirection):
                        return (direct[0], str(int(direct[1])-1))
            #Down
            if(number == 3):
                if(isinstance(self.df.at[direct[0]+1, direct[1]], Street)):
                    if((direct[0]+1, direct[1]) != self.oldcardirection):
                        return (direct[0]+1, direct[1])
            #Up
            if(number == 4):
                if(isinstance(self.df.at[direct[0]-1, direct[1]], Street)):
                    if((direct[0]-1, direct[1]) != self.oldcardirection):
                        return (direct[0]-1, direct[1])
            
        return self.oldcardirection

#Gameloop
class Game:
    def __init__(self):
        self.surface = Surface(args.m, args.n)
        self.logs = collections.deque(maxlen=5)

    def play(self):
        loopstop = []
        if "keyboard" in globals():
            keyboard.add_hotkey("q", lambda: loopstop.append(1))

        while not loopstop:
            time.sleep(args.t)
            os.system("cls") # Bei Windows sollte hier "cls" stehen
            self.surface.draw()
            self.surface.drivecar()

g = Game()
g.play()
