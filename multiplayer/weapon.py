import pygame
from gameobject import *

class Weapon(GameObject):
    def __init__(self, pos, vel=0, direction=(0, 0)):
        super().__init__(pos, vel, direction)
        self.angle = 0
