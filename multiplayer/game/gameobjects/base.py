import pygame
from .gameobject import *
from ..constants import *
from ..health_bar import *

class Base(GameObject):
    max_health = 100
    def __init__(self, pos=(0, 0), vel=0):
        super().__init__(pos, vel, shape=(BASE_WIDTH, BASE_HEIGHT))
        self.health = self.max_health
        self.health_bar = HealthBar(self, BASE_WIDTH)

    def draw(self, spritesheets, screen):
        super().draw(spritesheets, screen)
        self.health_bar.draw(screen)

    def update(self):
        ...
