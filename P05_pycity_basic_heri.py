# Standard modules from Python
import argparse
import time
import os
import collections
import pandas as pd
import json

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
p.add_argument("-t", dest="t", type=int, default=5, help="Update interval (s) (default 5s)")
args = p.parse_args()

class Field:
    def __init__(self, char):
        self.char = char
        self.value = 0

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

class Surface:
    def __init__(self, m, n):
        self.surface = np.full((m, n), Land())
        self.m = m
        self.n = n

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
        for index, row in self.df.iterrows():
            for column in row:
                print(column.char, end="")
            print()

    def evolve(self):
        pass

class Game:
    def __init__(self):
        self.surface = Surface(args.m, args.n)
        self.logs = collections.deque(maxlen=5)

    def play(self):
        loopstop = []
        if "keyboard" in globals():
            keyboard.add_hotkey("q", lambda: loopstop.append(1))

        f = open("pycity.log", "a")

        while not loopstop:
            time.sleep(args.t)
            os.system("cls") # Bei Windows sollte hier "cls" stehen
            self.surface.draw()  

g = Game()
g.play()
