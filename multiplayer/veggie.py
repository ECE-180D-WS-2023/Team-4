import pygame
from gameobject import *
from constants import *

class Veggie(GameObject):
    def __init__(self, pos=(0, 0), vel=10, direction=(0, 0), damage=1):
        super().__init__(pos, vel, direction)
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
    ...

class Mushroom(Veggie):
    ...

class Cabbage(Veggie):
    ...

class Potato(Veggie):
    ...

class YellowBellPepper(Veggie):
    ...
