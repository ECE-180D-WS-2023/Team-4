import pygame
from .gameobject import *
from .attachments.health_bar import *
from ..constants import *

class Base(GameObject):
    frame_width, frame_height = 80, 80
    animation_steps = [1]
    max_health = 500
    def __init__(self, pos, vel=0, direction=(0, 0), scale=BASE_SCALE):
        super().__init__(pos, vel, direction, scale)
        self.health = self.max_health
        self.health_bar = HealthBar(self, self.frame_width*scale)

    def draw(self, spritesheets, screen):
        super().draw(spritesheets, screen)
        self.health_bar.draw(screen)

    def update(self):
        super().update()
        if self.health < 0:
            self.kill = True
