import pygame
import math
import collections
from gameobject import *
from constants import *
from weapon import *
from veggie import *

class Player(GameObject):
    def __init__(self, pos, team_num, vel):
        super().__init__(pos, vel, scale=PLAYER_SCALE)
        self.team_num = team_num
        self.state = PLAYER_WALKING
        self.backpack = collections.deque()
        self.mounted = False
        self.weapon = None

    def shoot(self, shots):
        if self.state != PLAYER_SHOOTING:
            return
        if len(self.backpack) == 0:
            return

        veggie_class = self.backpack.popleft()
        shots.append(veggie_class(self.pos, self.strength + self.weapon_class.strength, (math.cos(math.radians(self.weapon.angle-90)), math.sin(math.radians(self.weapon.angle-90)))))

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
            self.weapon = self.weapon_class(self.pos)
        else:
            self.weapon = None

    def update(self):
        if self.state == PLAYER_WALKING:
            self.rect.center += self.direction * self.vel

class Engineer(Player):
    power = 5
    strength = 5
    weapon_class = Cannon
    def __init__(self, pos, team_num=0, vel=7):
        super().__init__(pos, team_num, vel)

class Soldier(Player):
    power = 10
    strength = 10
    weapon_class = Cannon
    def __init__(self, pos, team_num=0, vel=3):
        super().__init__(pos, team_num, vel)
