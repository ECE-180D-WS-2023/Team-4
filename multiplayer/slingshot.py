import pygame
from gameobject import *

class Slingshot(GameObject):
    def __init__(self, pos=(0, 0), vel=0):
        super().__init__(pos, vel)
