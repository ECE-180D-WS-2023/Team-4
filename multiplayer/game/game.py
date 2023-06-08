import pygame
import random
from .initialize import screen, GFX, spritesheets, SFX
from .constants import *
from .gameobjects.player import *

class Game:
    def __init__(self, scenes, first_scene):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.globals = {
            "GFX": GFX,
            "SFX": SFX,
            "spritesheets": spritesheets,
            "background": GFX["assets/graphics/misc/sky.png"],
            "middleground": GFX["assets/graphics/misc/tree_foreground.png"],
            "foreground": GFX["assets/graphics/misc/railway.png"],
            "middleground_x": 0,
            "foreground_x": 0,
            "middleground_speed": 1.5,
            "foreground_speed": 6,
            "player": random.choice(Player.__subclasses__())((525, 1175), vel=0, direction=(0, -1), scale=6, animate=True),
        }
        self.globals["player"].frame_row = 2
        self.scenes = scenes
        self.current_scene = scenes[first_scene]
        self.current_scene.startup(self.globals)

    def run(self):
        running = True
        while running:
            self.loop()
            self.update()
            self.draw()

    def next_scene(self):
        self.current_scene.cleanup()
        self.current_scene = self.scenes[self.current_scene.next]
        self.current_scene.startup(self.globals)

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            self.current_scene.handle_event(event)

    def draw(self):
        self.current_scene.draw(self.screen)
        pygame.display.update()

    def update(self):
        if self.current_scene.done:
            self.next_scene()
        self.current_scene.update()
        self.clock.tick(60)
