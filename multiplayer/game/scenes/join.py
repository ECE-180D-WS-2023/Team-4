import pygame
from .scene import *
from ..constants import *
from ..ui.button import *
from ..ui.input import *

class JoinScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("assets/menu/static-background.png").convert_alpha()
        self.input = InputField((SCREEN_WIDTH/2, 300), label_text="Enter Server IP:", font_size=40)
        self.menu = ButtonMenu()
        self.start_button = self.menu.add_button(Button((SCREEN_WIDTH/2, 450), "START"))
        self.back_button = self.menu.add_button(Button((SCREEN_WIDTH/2, 600), "BACK"))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.menu.check_for_presses(event.pos)
            if button == self.start_button:
                self.next = "game"
                self.done = True
            if button == self.back_button:
                self.next = "play"
                self.done = True
        elif event.type == KEYDOWN:
            self.input.process_keydown(event)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.menu.draw(screen)
        self.input.draw(screen)

    def update(self):
        self.menu.update()
        self.input.update()
