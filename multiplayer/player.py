import pygame
import math
import collections
from gameobject import *
from constants import *
from weapon import *
from veggie import *

class Player(GameObject):
    def __init__(self, pos=(0, 0), vel=5, team_num=1):
        super().__init__(pos, vel, scale=PLAYER_SCALE)
        self.state = PLAYER_WALKING
        self.team_num = team_num
        self.backpack = collections.deque()
        self.mounted = False
        self.weapon = None

    def shoot(self):
        return Veggie(self.pos, 10, (math.cos(math.radians(self.weapon.angle-90)), math.sin(math.radians(self.weapon.angle-90))))

    def harvest(self, veggies):
        for veggie in veggies:
            if self.rect.colliderect(veggie.rect):
                self.backpack.append(veggie.__class__)
                veggies.remove(veggie)
                break

    def toggle_mount(self, slingshot):
        if self.mounted:
            print("unmount")
            self.mounted = False
            self.state = PLAYER_WALKING
            self._toggle_weapon()
        elif self.rect.colliderect(slingshot.rect):
            print("mount")
            self.mounted = True
            self.pos = slingshot.pos
            self.state = PLAYER_SHOOTING
            self._toggle_weapon()

    def _toggle_weapon(self):
        if not self.weapon:
            self.weapon = Weapon(self.pos)
        else:
            self.weapon = None

    def update(self):
        if self.state == PLAYER_WALKING:
            self.rect.center += self.direction * self.vel
