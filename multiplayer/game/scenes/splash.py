import pygame
from .scene import *
from ..constants import *

class SplashScene(Scene):
    next = "main_menu"
    def __init__(self):
        super().__init__()
        self.logo = pygame.image.load("assets/menu/puzzle.png").convert_alpha()
        self.label = pygame.font.Font("assets/fonts/introduction_font.ttf", 40).render("Veggie Wars Gaming", True, (255, 255, 255))
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((0, 0, 0))
        self.alpha_start = 0
        self.alpha_end = 255
        self.fade_in_duration = 2000  # in milliseconds
        self.fade_out_duration = 2000  # in milliseconds
        # self.next = "main_menu"

    def startup(self, globals):
        super().startup(globals)
        self.start_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, (SCREEN_WIDTH // 2 - self.logo.get_width() // 2, SCREEN_HEIGHT // 2 - self.logo.get_height() // 2))
        screen.blit(self.label, (SCREEN_WIDTH // 2 - self.label.get_width() // 2, SCREEN_HEIGHT // 2 + self.logo.get_height() // 2))

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        alpha = 0
        if elapsed_time < self.fade_in_duration:
            alpha = self.alpha_start + int((self.alpha_end - self.alpha_start) * elapsed_time / self.fade_in_duration)
        elif elapsed_time < (self.fade_in_duration + self.fade_out_duration):
            alpha = self.alpha_end - int((self.alpha_end - self.alpha_start) * (elapsed_time - self.fade_in_duration) / self.fade_in_duration)
        else:
            self.done = True

        self.logo.set_alpha(alpha)
        self.label.set_alpha(alpha)
