import pygame
import random
from .scene import *
from ..constants import *
from ..ui.button import *
from ..ui.text import *
from ..gameobjects.player import *
from ..spritesheet import *

class MainMenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.buttons = ButtonGroup()
        # self.play_button = self.buttons.add_button(RectButton((700, 450), "PLAY"))
        # self.tutorials_button = self.buttons.add_button(RectButton((700, 600), "TUTORIALS"))
        # self.quit_button = self.buttons.add_button(RectButton((700, 750), "QUIT"))
        normal = pygame.transform.scale_by(GFX["assets/graphics/buttons/individual_frames/silver/normal.png"], 7)
        hover = pygame.transform.scale_by(GFX["assets/graphics/buttons/individual_frames/silver/hover.png"], 7)
        self.play_button = self.buttons.add_button(ImageButton((SCREEN_WIDTH/2, 500), normal, hover, text="PLAY"))
        self.tutorials_button = self.buttons.add_button(ImageButton((SCREEN_WIDTH/2, 650), normal, hover, text="TUTORIALS"))
        self.quit_button = self.buttons.add_button(ImageButton((SCREEN_WIDTH/2, 800), normal, hover, text="QUIT"))

    def startup(self, globals):
        super().startup(globals)
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('assets/music/another-sunny-day.mp3')
            pygame.mixer.music.play(-1)
        self.title = Text((SCREEN_WIDTH/2, 200), "Veggie Wars", font="assets/fonts/fibberish.ttf", font_size=200, shadow=True, shadow_offset=5)
        # self.title = TypewriterText((SCREEN_WIDTH/2, 75), "Veggie Wars", font="assets/fonts/bongo.ttf", font_size=150, slowness=7)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.buttons.check_for_presses(event.pos)
            if button == self.play_button:
                self.next = "play"
                self.done = True
            if button == self.tutorials_button:
                self.next = "tutorial"
                self.done = True
            if button == self.quit_button:
                # Quit scene?
                pygame.quit()

    def draw(self, screen):
        super().draw(screen)
        self.buttons.draw(screen)
        self.title.draw(screen)

    def update(self):
        super().update()
        self.buttons.update()
