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
        self.input = InputField((SCREEN_WIDTH/2, 300), default_text=get_private_ip(), label_text="Enter IP:", font_size=40)
        self.buttons = ButtonGroup()
        self.start_button = self.buttons.add_button(RectButton((SCREEN_WIDTH/2, 450), "START"))
        self.back_button = self.buttons.add_button(RectButton((SCREEN_WIDTH/2, 600), "BACK"))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.buttons.check_for_presses(event.pos)
            if button == self.start_button:
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
        super().draw(screen)
        self.buttons.draw(screen)
        self.input.draw(screen)

    def update(self):
        super().update()
        self.buttons.update()
        self.input.update()
