import pygame
from .scene import *
from ..constants import *
from ..ui.button import *
from ..ui.input import *

class PlayScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("assets/menu/static-background.png").convert_alpha()
        self.menu = ButtonMenu()
        self.host_button = self.menu.add_button(Button((700, 350), "HOST"))
        self.join_button = self.menu.add_button(Button((700, 500), "JOIN"))
        self.back_button = self.menu.add_button(Button((700, 650), "BACK"))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.menu.check_for_presses(event.pos)
            if button == self.host_button:
                self.next = "host"
                self.done = True
            if button == self.join_button:
                self.next = "join"
                self.done = True
            if button == self.back_button:
                self.next = "main_menu"
                self.done = True

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.menu.draw(screen)

    def update(self):
        self.menu.update()
