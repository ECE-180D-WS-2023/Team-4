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
        normal_button = pygame.transform.scale_by(GFX["assets/graphics/buttons/individual_frames/silver/normal.png"], 7)
        hover_button = pygame.transform.scale_by(GFX["assets/graphics/buttons/individual_frames/silver/hover.png"], 7)
        self.ready_button = self.buttons.add_button(ImageButton((SCREEN_WIDTH/2, 500), normal_button, hover_button, text="READY"))
        self.back_button = self.buttons.add_button(ImageButton((SCREEN_WIDTH/2, 650), normal_button, hover_button, text="BACK"))

    def startup(self, globals):
        super().startup(globals)
        self.hosting_message = Text((SCREEN_WIDTH/2, 130), f"Server hosted on {self.globals['address']}", font="assets/fonts/fibberish.ttf", font_size=110, shadow=True)
        self.waiting_message = TypewriterText((SCREEN_WIDTH/2, 240), "Waiting for players", font="assets/fonts/fibberish.ttf", font_size=75, slowness=5)
        self.ellipsis = TypewriterText((SCREEN_WIDTH/2 + 305, 240), "....", font="assets/fonts/fibberish.ttf", font_size=75, slowness=30, align="left")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.buttons.check_for_presses(event.pos)
            if button == self.ready_button:
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
        self.waiting_message.draw(screen)
        if self.waiting_message.done:
            self.ellipsis.draw(screen)
        if self.ellipsis.done:
            self.ellipsis.counter = 0

    def update(self):
        self.buttons.update()
