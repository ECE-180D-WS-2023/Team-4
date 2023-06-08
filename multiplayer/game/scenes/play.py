import pygame
from .scene import *
from ..constants import *
from ..ui.button import *
from ..ui.input import *

class PlayScene(Scene):
    def __init__(self):
        super().__init__()
        self.buttons = ButtonGroup()
        self.host_button = self.buttons.add_button(RectButton((700, 350), "HOST"))
        self.join_button = self.buttons.add_button(RectButton((700, 500), "JOIN"))
        self.back_button = self.buttons.add_button(RectButton((700, 650), "BACK"))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.buttons.check_for_presses(event.pos)
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
        super().draw(screen)
        self.buttons.draw(screen)

    def update(self):
        super().update()
        self.buttons.update()
