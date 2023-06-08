import pygame
from .scene import *
from ..spritesheet import Animation
from ..constants import *

class LoadingScene(Scene):
    next = "main_menu"
    def __init__(self):
        super().__init__()
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((0, 0, 0))

    def startup(self, globals):
        super().startup(globals)
        self.loading_bar_animation = Animation((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), self.globals["GFX"]["assets/graphics/misc/progress_bar.png"], animation_steps=[8], frame_size=(480, 320), animation_cooldown=500)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.loading_bar_animation.draw(screen)
        self.done = self.loading_bar_animation.stopped

    def update(self):
        self.loading_bar_animation.update()
