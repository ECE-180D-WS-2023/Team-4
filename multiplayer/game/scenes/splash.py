import pygame
from .scene import *
from ..constants import *

class SplashScene(Scene):
    next = "loading"
    def __init__(self):
        super().__init__()
        self.logo = pygame.transform.scale_by(GFX["assets/graphics/misc/tomato.png"], 10)
        self.label = pygame.font.Font("assets/fonts/bongo.ttf", 25).render("Happy Tomato Productions", True, (255, 255, 255))
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((0, 0, 0))
        self.alpha_start = 0
        self.alpha_end = 255
        self.fade_in_duration = 2000  # in milliseconds
        self.fade_out_duration = 2000  # in milliseconds
        self.sound = pygame.mixer.Sound("assets/sounds/logo_sound.mp3")
        # self.next = "main_menu"

    def startup(self, globals):
        super().startup(globals)
        self.start_time = pygame.time.get_ticks()
        self.sound.play()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, (SCREEN_WIDTH//2 - self.logo.get_width()//2, SCREEN_HEIGHT//2 - self.logo.get_height()//2))
        screen.blit(self.label, (SCREEN_WIDTH//2 - self.label.get_width()//2, SCREEN_HEIGHT//2 + self.logo.get_height()//2 + 40))

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
