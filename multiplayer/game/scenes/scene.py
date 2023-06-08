import pygame
from ..constants import *
from ..spritesheet import *
from ..initialize import GFX

class Scene:
    next = None
    def __init__(self):
        self.done = False

    def startup(self, globals):
        self.globals = globals

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                self.globals["player"].vel = 15

    def cleanup(self):
        self.done = False

    def draw(self, screen):
        screen.blit(self.globals["background"], (0, 0))
        screen.blit(self.globals["middleground"], (self.globals["middleground_x"], 0))
        screen.blit(self.globals["foreground"], (self.globals["foreground_x"], 0))
        self.globals["player"].draw(self.globals["spritesheets"], screen)

    def update(self):
        self.globals["middleground_x"] -= self.globals["middleground_speed"]
        self.globals["foreground_x"] -= self.globals["foreground_speed"]
        if self.globals["middleground_x"] < (-self.globals["middleground"].get_width() + SCREEN_WIDTH):
            self.globals["middleground_x"] = 0
        if self.globals["foreground_x"] < (-self.globals["foreground"].get_width() + SCREEN_WIDTH):
            self.globals["foreground_x"] = 0
        # if self.globals["player"].pos[1] != 1125:
        #     self.globals["player"].vel -= 0.4
        # if self.globals["player"].pos[1] > 1125:
        #     self.globals["player"].pos = (200, 1125)
        #     self.globals["player"].vel = 0
        self.globals["player"].update()
