import pygame
import server
import multiprocessing
from .scene import *
from ..constants import *
from ..network import get_private_ip
from ..ui.button import *
from ..ui.input import *

class HostScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = GFX["assets/graphics/misc/sky.png"]
        self.input = InputField((SCREEN_WIDTH/2, 300), default_text=get_private_ip(), label_text="Enter IP:", font_size=40)
        self.buttons = ButtonGroup()
        normal_button = pygame.transform.scale_by(GFX["assets/graphics/buttons/individual_frames/silver/normal.png"], 7)
        hover_button = pygame.transform.scale_by(GFX["assets/graphics/buttons/individual_frames/silver/hover.png"], 7)
        self.host_button = self.buttons.add_button(ImageButton((SCREEN_WIDTH/2, 500), normal_button, hover_button, text="HOST"))
        self.back_button = self.buttons.add_button(ImageButton((SCREEN_WIDTH/2, 650), normal_button, hover_button, text="BACK"))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.buttons.check_for_presses(event.pos)
            if button == self.host_button:
                self.globals["address"] = self.input.text
                self.globals["server"] = multiprocessing.Process(target=server.run, args=(self.globals["address"],))
                self.globals["server"].start()
                self.next = "lobby"
                self.done = True
            if button == self.back_button:
                self.next = "play"
                self.done = True
        elif event.type == KEYDOWN:
            self.input.process_keydown(event)

    def draw(self, screen):
        # super().draw(screen)
        screen.blit(self.background, (0, 0))
        self.buttons.draw(screen)
        self.input.draw(screen)

    def update(self):
        # super().update()
        self.buttons.update()
        self.input.update()
