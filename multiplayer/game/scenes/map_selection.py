import pygame
from .scene import *
from ..spritesheet import Animation
from ..ui.button import *
from ..constants import *
from ..gameobjects.weapon import *

class MapSelectionScene(Scene):
    next = "game"
    def __init__(self):
        super().__init__()
        self.buttons = ButtonGroup()
        self.weapon_outline = pygame.image.load("assets/graphics/pause-phase/weapon-selection-outline.png").convert_alpha()
        self.map_outline = pygame.image.load("assets/graphics/pause-phase/map-selection-outline.png").convert_alpha()
        self.skull_crossbow_button = self.buttons.add_button(TransparentButton((549, 931), width=100, height=100))
        self.demonic_crossbow_button = self.buttons.add_button(TransparentButton((693, 931), width=100, height=100))
        self.fire_crossbow_button = self.buttons.add_button(TransparentButton((835, 931), width=100, height=100))
        self.venom_crossbow_button = self.buttons.add_button(TransparentButton((972, 933), width=100, height=100))
        self.divine_crossbow_button = self.buttons.add_button(TransparentButton((1111, 933), width=100, height=100))
        self.summer_map_button = self.buttons.add_button(TransparentButton((1760, 631), width=580, height=190))
        self.fall_map_button = self.buttons.add_button(TransparentButton((1760, 855), width=580, height=190))
        self.winter_map_button = self.buttons.add_button(TransparentButton((1760, 1080), width=580, height=190))
        self.ready_button = self.buttons.add_button(ImageButton((1750, 1250), pygame.transform.scale_by(GFX["assets/graphics/pause-phase/pause-button.png"], 1.5), text="READY", font_size=20, text_color=(150,150,150), text_color_hover=(200,200,200)))
        self.page_flip_sound = pygame.mixer.Sound('assets/sounds/book_flip.mp3')

    def startup(self, globals):
        super().startup(globals)
        self.player = self.globals["player_class"]((603, 624), scale=3, animate=True)
        self.book_animation = Animation((SCREEN_WIDTH/2,SCREEN_HEIGHT/2), self.globals["GFX"]["assets/graphics/pause-phase/choose-player-old.png"], 
                                animation_steps=[7], frame_size=(2560, 1600), pause_frames=[6], color=None)
        self.ink_animation = Animation((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), self.globals["GFX"]["assets/graphics/pause-phase/phase2-text-appear.png"],
                                  [13], (SCREEN_WIDTH, SCREEN_HEIGHT), 1, animation_cooldown=90)
        self.selected_weapon_class = SkullCrossbow
        self.selected_map = GFX["assets/graphics/maps/summer_rails.png"]
        self.page_flip_sound.play()
        self.weapon_outline_pos = (549, 931)
        self.map_outline_pos = (1760, 631)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            button = self.buttons.check_for_presses(event.pos)
            if button == self.ready_button:
                self.globals["weapon_class"] = self.selected_weapon_class
                self.globals["map"] = self.selected_map
                self.done = True
            elif button == self.skull_crossbow_button:
                self.selected_weapon_class = SkullCrossbow
                self.weapon_outline_pos = (549, 931) 
            elif button == self.demonic_crossbow_button:
                self.selected_weapon_class = DemonicCrossbow
                self.weapon_outline_pos = (693, 931) 
            elif button == self.fire_crossbow_button:
                self.selected_weapon_class = FireCrossbow
                self.weapon_outline_pos = (835, 931) 
            elif button == self.venom_crossbow_button:
                self.selected_weapon_class = VenomCrossbow
                self.weapon_outline_pos = (972, 931) 
            elif button == self.divine_crossbow_button:
                self.selected_weapon_class = DivineCrossbow
                self.weapon_outline_pos = (1111, 931) 
            elif button == self.summer_map_button:
                self.selected_map = GFX["assets/graphics/maps/summer_rails.png"]
                self.map_outline_pos = (1760, 631) 
            elif button == self.fall_map_button:
                self.selected_map = GFX["assets/graphics/maps/fall_rails.png"]
                self.map_outline_pos = (1760, 855) 
            elif button == self.winter_map_button:
                self.selected_map = GFX["assets/graphics/maps/winter_rails.png"]
                self.map_outline_pos = (1760, 1080) 

    def draw(self, screen):
        self.book_animation.draw(screen)

        if self.book_animation.stopped:
            self.buttons.draw(screen)
            self.player.draw(self.globals["spritesheets"], screen)
            self.ink_animation.draw(screen)

        if self.ink_animation.stopped:
            screen.blit(self.weapon_outline, (self.weapon_outline_pos[0]-self.weapon_outline.get_width()/2, self.weapon_outline_pos[1]-self.weapon_outline.get_height()/2))
            screen.blit(self.map_outline, (self.map_outline_pos[0]-self.map_outline.get_width()/2, self.map_outline_pos[1]-self.map_outline.get_height()/2))


    def update(self):
        self.book_animation.update(loop=False)
        if self.book_animation.stopped:
            self.ink_animation.update()
        if self.ink_animation.stopped:
            self.buttons.update()
        self.player.update()
