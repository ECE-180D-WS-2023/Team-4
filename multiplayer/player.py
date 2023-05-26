import pygame
import math
import collections
from gameobject import *
from constants import *
from weapon import *
from veggie import *

class Player(GameObject):
    def __init__(self, pos, team_num, vel, weapon_class):
        super().__init__(pos, vel, scale=PLAYER_SCALE)
        self.team_num = team_num
        self.state = PLAYER_WALKING
        self.backpack = collections.deque()
        self.mounted = False
        self.weapon = weapon_class(pos)

    def shoot(self, shots):
        if self.state != PLAYER_SHOOTING:
            return
        if len(self.backpack) == 0:
            return

        veggie_class = self.backpack.popleft()
        shots.append(veggie_class(self.pos, self.strength + self.weapon.strength, (math.cos(math.radians(self.weapon.angle-90)), math.sin(math.radians(self.weapon.angle-90)))))

    def harvest(self, veggies):
        veggie = self.rect.collideobjects(veggies, key=lambda o: o.rect)
        if veggie:
            self.backpack.append(veggie.__class__)
            veggies.remove(veggie)

    def toggle_mount(self, slingshot):
        if self.mounted:
            print("unmount")
            self.mounted = False
            self.state = PLAYER_WALKING
            # self._toggle_weapon()
        elif self.rect.colliderect(slingshot.rect):
            print("mount")
            self.mounted = True
            self.pos = slingshot.pos
            self.weapon.pos = self.pos
            self.state = PLAYER_SHOOTING
            # self._toggle_weapon()

    def draw(self, spritesheets, screen):
        super().draw(spritesheets, screen)
        if self.state == PLAYER_SHOOTING:
            self.weapon.draw(spritesheets, screen)

    def update(self):
        if self.state == PLAYER_WALKING:
            self.rect.center += self.direction * self.vel

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Engineer(Player):
    power = 5
    strength = 5
    def __init__(self, pos, weapon_class, team_num=0, vel=7):
        super().__init__(pos, team_num, vel, weapon_class)

class Soldier(Player):
    power = 10
    strength = 10
    def __init__(self, pos, weapon_class, team_num=0, vel=3):
        super().__init__(pos, team_num, vel, weapon_class)
