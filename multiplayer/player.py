import pygame
import collections
from gameobject import *

class Player(GameObject):
    def __init__(self, pos=(0, 0), vel=5):
        super().__init__(pos, vel)
        self.backpack = collections.deque()
        self.mounted = False
