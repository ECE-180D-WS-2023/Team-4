import pygame
from .scene import *
from ..constants import *
from ..ui.button import *
from ..ui.text import *

class LobbyScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = GFX["assets/graphics/misc/sky.png"]
        self.buttons = ButtonGroup()
        self.start_button = self.buttons.add_button(RectButton((SCREEN_WIDTH/2, 450), "START"))
        self.back_button = self.buttons.add_button(RectButton((SCREEN_WIDTH/2, 600), "BACK"))

    def startup(self, globals):
        super().startup(globals)
        self.hosting_message = Text((SCREEN_WIDTH/2, 110), f"Server hosted on {self.globals['address']}", font_size=95, shadow=True)
        self.waiting_message = TypewriterText((SCREEN_WIDTH/2, 225), "Waiting for players", font_size=75, slowness=5)
        self.ellipsis = TypewriterText((SCREEN_WIDTH/2 + 365, 225), "....", font_size=75, slowness=30, align="left")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.buttons.check_for_presses(event.pos)
            if button == self.start_button:
                self.next = "player_selection"
                self.done = True
            if button == self.back_button:
                self.next = "host"
                # stop server
                self.done = True

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.buttons.draw(screen)
        self.hosting_message.draw(screen)
        self.waiting_message.update(screen)
        if self.waiting_message.done:
            self.ellipsis.update(screen)
        if self.ellipsis.done:
            self.ellipsis.counter = 0

    def update(self):
        self.buttons.update()
