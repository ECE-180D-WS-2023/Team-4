import pygame
import multiprocessing
from .constants import *

pygame.init()
print("HFKDLSJFSKDL")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Veggie Wars")
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
multiprocessing.set_start_method("fork")

class Game:
    def __init__(self, scenes, first_scene):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.globals = {}
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
            self.current_scene.handle_event(event)

    def draw(self):
        self.current_scene.draw(self.screen)
        pygame.display.update()

    def update(self):
        if self.current_scene.done:
            self.next_scene()
        self.current_scene.update()
        self.clock.tick(60)
