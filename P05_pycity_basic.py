# Standard modules from Python
import argparse
import time
import os
import sys
import random
import collections

# External modules from Anaconda distribution
import numpy as np

# External modules from PyPi
try:
    import keyboard
except:
    print("Warning: no real-time keyboard/hotkey support.")

p = argparse.ArgumentParser(description="City simulation in Python.")
p.add_argument("-m", dest="m", type=int, default=20, help="Width of surface (default 20)")
p.add_argument("-n", dest="n", type=int, default=20, help="Height of surface (default 20)")
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

class Surface:
    def __init__(self, m, n):
        self.surface = np.full((m, n), Land())
        self.m = m
        self.n = n

        for i in range(random.randrange(m + n)):
            self.surface[random.randrange(m), random.randrange(n)] = random.choice((Water(), Resident(), Business()))

    def draw(self):
        for row in range(self.n):
            for col in range(self.m):
                print(self.surface[col, row].char, end="")
            print()

    def evolve(self):
        changes = []

        for row in range(self.n):
            for col in range(self.m):
                field = self.surface[col, row]
                if isinstance(field, Resident):
                    field.value += 1
                    if field.value >= random.randint(5, 10):
                        field = Water()
                        changes.append(f"Residents at {row},{col} drowned.")
                self.surface[col, row] = field

        return changes

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
            print(f"Sim round #{int(time.time())} - Symbols: ・land 〜water 〠res.house 〓business")

            changes = self.surface.evolve()
            self.surface.draw()

            for change in changes:
                stampedchange = f"#{int(time.time())} {change}"
                self.logs.append(stampedchange)
                print(stampedchange, file=f)
            for log in self.logs:
                print(f"» {log}")

g = Game()
g.play()
