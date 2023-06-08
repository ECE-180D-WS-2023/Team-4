import pygame
from .gameobject import *
from ..constants import *

class Slingshot(GameObject):
    mount_offset: tuple
    def __init__(self, pos, vel=0, direction=(1, 0), scale=SLINGSHOT_SCALE):
        super().__init__(pos, vel, direction, scale)
        self.initial_pos_x = pos[0]

    def update(self):
        super().update()
        self.mount_pos = (self.pos[0] + self.mount_offset[0], self.pos[1] + self.mount_offset[1])
        # Hardcode the edges of rails
        if ((self.rect.right > self.initial_pos_x + 250) or
            (self.rect.left < self.initial_pos_x - 250)):
            self.direction.x *= -1

    def mount(self):
        self.vel = 3

    def unmount(self):
        self.vel = 0

class Trolley(Slingshot):
    frame_width, frame_height = 48, 32
    animation_steps = [1]
    mount_offset = (0, -20)
