import pygame
import math
import collections
from .gameobject import *
from .weapon import *
from .veggie import *
from ..constants import *

class Player(GameObject):
    strength: int
    power: int
    def __init__(self, pos, vel, direction, scale, weapon_class, team_num, animate):
        super().__init__(pos, vel, direction, scale=scale, animate=animate)
        self.team_num = team_num
        self.state = PLAYER_WALKING
        self.backpack = collections.deque()
        self.weapon = weapon_class(pos)

    def shoot(self, shots):
        if self.state != PLAYER_SHOOTING:
            return
        if len(self.backpack) == 0:
            return

        veggie_class = self.backpack.popleft()
        shots.append(veggie_class(self.pos, vel=self.power+self.weapon.power, direction=(math.cos(math.radians(self.weapon.angle-90)), math.sin(math.radians(self.weapon.angle-90))), scale=1.5, damage=self.strength+self.weapon.strength))

    def harvest(self, veggies):
        veggie = self.rect.collideobjects(veggies, key=lambda o: o.rect)
        if veggie:
            self.backpack.append(veggie.__class__)
            veggies.remove(veggie)

    def toggle_mount(self, slingshot):
        if self.state == PLAYER_SHOOTING:
            print("unmount")
            slingshot.unmount()
            self.state = PLAYER_WALKING
        elif self.rect.colliderect(slingshot.rect):
            print("mount")
            slingshot.mount()
            self.slingshot = slingshot
            self.pos = slingshot.mount_pos
            self.weapon.pos = self.pos
            self.state = PLAYER_SHOOTING

    def draw(self, spritesheets, screen):
        super().draw(spritesheets, screen)
        if self.state == PLAYER_SHOOTING:
            self.weapon.draw(spritesheets, screen)

    def update(self):
        if self.state == PLAYER_WALKING:
            super().update()
        elif self.state == PLAYER_SHOOTING:
            self.pos = self.slingshot.mount_pos
            self.weapon.pos = self.pos

        # Negative team number for player objects not in game (e.g. in main menu)
        if self.team_num >= 0:
            # Animation update
            if self.direction.x == -1:
                self.frame_row = 1
                self.animate = True
            elif self.direction.x == 1:
                self.frame_row = 2
                self.animate = True
            elif self.direction.y == 1:
                self.frame_row = 0
                self.animate = True
            elif self.direction.y == -1:
                self.frame_row = 3
                self.animate = True
            else:
                self.animate = False

            # Borders
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top < TEAM_BOUNDARIES[self.team_num]["top"]:
                self.rect.top = TEAM_BOUNDARIES[self.team_num]["top"]
            if self.rect.bottom > TEAM_BOUNDARIES[self.team_num]["bottom"]:
                self.rect.bottom = TEAM_BOUNDARIES[self.team_num]["bottom"]

class Engineer(Player):
    frame_width, frame_height = 32, 32
    animation_steps = [3, 3, 3, 3]
    strength = 5
    power = 5
    def __init__(self, pos, vel=7, direction=(0, 0), scale=PLAYER_SCALE, weapon_class=Cannon, team_num=-1, animate=False):
        super().__init__(pos, vel, direction, scale, weapon_class, team_num, animate)

class Soldier(Player):
    frame_width, frame_height = 32, 32
    animation_steps = [3, 3, 3, 3]
    strength = 10
    power = 10
    def __init__(self, pos, vel=3, direction=(0, 0), scale=PLAYER_SCALE, weapon_class=Cannon, team_num=-1, animate=False):
        super().__init__(pos, vel, direction, scale, weapon_class, team_num, animate)
