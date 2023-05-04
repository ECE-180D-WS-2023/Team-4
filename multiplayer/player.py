import pygame
import collections
from gameobject import *
from constants import *

class Player(GameObject):
    def __init__(self, pos=(0, 0), vel=5):
        super().__init__(pos, vel)
        self.backpack = collections.deque()
        self.mounted = False

    def toggle_mount(self, slingshot):
        if self.mounted:
            print("unmount")
            self.mounted = False
            self.state = PLAYER_WALKING
        elif self.rect.colliderect(slingshot.rect):
            print("mount")
            self.mounted = True
            self.pos = slingshot.pos
            self.state = PLAYER_SHOOTING
        else:
            print("toggle")
