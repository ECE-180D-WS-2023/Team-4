import pygame
from .gameobject import *
from ..constants import *

class Veggie(GameObject):
    def __init__(self, pos, vel=10, direction=(0, 0), scale=VEGGIE_SCALE, damage=1, animate=False):
        super().__init__(pos, vel, direction, scale, animate=animate)
        self.damage = damage

    def check_collision(self, objects):
        for object in objects:
            if self.rect.colliderect(object.rect):
                self.hit(object)

    def hit(self, object):
        object.health -= self.damage
        self.kill = True
        print("hit:", object.health)

    def update(self):
        super().update()
        if (self.rect.left < 0 
            or self.rect.right > SCREEN_WIDTH 
            or self.rect.top <= 0
            or self.rect.bottom >= SCREEN_HEIGHT):
            self.kill = True

class Carrot(Veggie):
    frame_width, frame_height = 18, 20
    animation_steps = [4]
    damage = 5

class Peach(Veggie):
    frame_width, frame_height = 18, 20
    animation_steps = [4]
    damage = 5

class Potato(Veggie):
    frame_width, frame_height = 18, 20
    animation_steps = [4]
    damage = 5

class Tomato(Veggie):
    frame_width, frame_height = 18, 20
    animation_steps = [4]
    damage = 5
