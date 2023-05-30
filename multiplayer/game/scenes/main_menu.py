import pygame
from .scene import *
from ..constants import *
from ..ui.button import *

class MainMenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("assets/menu/static-background.png").convert_alpha()
        self.middleground = pygame.image.load("assets/menu/5.png").convert_alpha()
        self.foreground = pygame.image.load("assets/menu/6.png").convert_alpha()
        self.middleground_x, self.foreground_x = 0, 0
        self.middleground_speed, self.foreground_speed = 1.5, 6
        self.menu = ButtonMenu()
        self.play_button = self.menu.add_button(Button((700, 350), "PLAY"))
        self.tutorials_button = self.menu.add_button(Button((700, 500), "TUTORIALS"))
        self.quit_button = self.menu.add_button(Button((700, 650), "QUIT"))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.menu.check_for_presses(event.pos)
            if button == self.play_button:
                self.next = "play"
                self.done = True
            if button == self.tutorials_button:
                self.next = "tutorial"
                self.done = True
            if button == self.quit_button:
                self.done = True

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.middleground, (self.middleground_x, 0))
        screen.blit(self.foreground, (self.foreground_x, 0))
        self.menu.draw(screen)

    def update(self):
        self.middleground_x -= self.middleground_speed
        self.foreground_x -= self.foreground_speed
        if self.middleground_x < (-self.middleground.get_width() + SCREEN_WIDTH):
            self.middleground_x = 0
        if self.foreground_x < (-self.foreground.get_width() + SCREEN_WIDTH):
            self.foreground_x = 0
        self.menu.update()
