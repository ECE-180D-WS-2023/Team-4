import pygame
from .scene import *
from ..constants import *
from ..ui.button import *
from ..ui.input import *
from ..ui.text import *

class PlayScene(Scene):
    def __init__(self):
        super().__init__()
        self.buttons = ButtonGroup()
        normal_button = pygame.transform.scale_by(GFX["assets/graphics/buttons/individual_frames/silver/normal.png"], 7)
        hover_button = pygame.transform.scale_by(GFX["assets/graphics/buttons/individual_frames/silver/hover.png"], 7)
        self.host_button = self.buttons.add_button(ImageButton((SCREEN_WIDTH/2, 500), normal_button, hover_button, text="HOST"))
        self.join_button = self.buttons.add_button(ImageButton((SCREEN_WIDTH/2, 650), normal_button, hover_button, text="JOIN"))
        self.back_button = self.buttons.add_button(ImageButton((SCREEN_WIDTH/2, 800), normal_button, hover_button, text="BACK"))
        self.title = Text((SCREEN_WIDTH/2, 250), "Play", font="assets/fonts/fibberish.ttf", font_size=200, shadow=True, shadow_offset=5)

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
        self.title.draw(screen)

    def update(self):
        super().update()
        self.buttons.update()
