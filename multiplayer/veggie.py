import pygame
from gameobject import *

class Veggie(GameObject):
    def __init__(self, pos=(0, 0), vel=10, direction=(0, 0)):
        super().__init__(pos, vel, direction)
