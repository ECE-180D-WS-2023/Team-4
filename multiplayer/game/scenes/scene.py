import pygame

class Scene:
    def __init__(self):
        self.next = None
        self.done = False

    def startup(self, globals):
        self.globals = globals

    def handle_event(self, event):
        ...

    def cleanup(self):
        self.done = False

    def draw(self, screen):
        ...

    def update(self):
        ...
