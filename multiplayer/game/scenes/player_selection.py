import pygame
import server
import random
from .scene import *
from ..gameobjects.player import *
from  ..spritesheet import *
from ..constants import *
from ..ui.button import *
from ..ui.input import *

class PlayerSelectionScene(Scene):
    next = "map_selection"
    def __init__(self):
        super().__init__()
        self.buttons = ButtonGroup()
        self.right_button = self.buttons.add_button(ImageButton((1985, 675), GFX["assets/graphics/pause-phase/right-arrow.png"]))
        self.left_button = self.buttons.add_button(ImageButton((1592, 675), GFX["assets/graphics/pause-phase/left-arrow.png"], text=""))
        self.continue_button = self.buttons.add_button(ImageButton((1700, 1225), GFX["assets/graphics/pause-phase/pause-button.png"], text="CONTINUE"))
        self.player = random.choice(Player.__subclasses__())((1785, 677), scale=4, animate=True)
        player_list = Player.__subclasses__()
        self.player_dict = {}
        for i in range(len(player_list)):
            self.player_dict[player_list[i]] = {
                "next": player_list[(i + 1) % len(player_list)],
                "prev": player_list[(i - 1) % len(player_list)],
            }

    def startup(self, globals):
        super().startup(globals)
        self.book_animation = Animation((SCREEN_WIDTH/2,SCREEN_HEIGHT/2), self.globals["GFX"]["assets/graphics/pause-phase/choose-player-old.png"], 
                                animation_steps=[7], frame_size=(2560, 1600), pause_frames=[0], color=None)
        pygame.mixer.music.load('assets/music/the-voice-in-my-heart.mp3')
        pygame.mixer.music.play(-1)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.buttons.check_for_presses(event.pos)
            if button == self.right_button:
                self.player = self.player_dict[self.player.__class__]["next"](self.player.pos, scale=4, animate=True)
            elif button == self.left_button:
                self.player = self.player_dict[self.player.__class__]["prev"](self.player.pos, scale=4, animate=True)
            elif button == self.continue_button:
                self.globals["player_class"] = self.player.__class__
                self.done = True

    def draw(self, screen):
        self.book_animation.draw(screen)
        self.player.draw(self.globals["spritesheets"], screen)
        self.buttons.draw(screen)

    def update(self):
        self.player.update()
        self.buttons.update()
