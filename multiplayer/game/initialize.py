import pygame
import os
import multiprocessing
from .constants import *
from .spritesheet import *
from .gameobjects.player import *
from .gameobjects.veggie import *
from .gameobjects.base import *
from .gameobjects.slingshot import *
from .gameobjects.weapon import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Veggie Wars")
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
multiprocessing.set_start_method("fork")

# Load all images (key: path/to/image, value: pygame surface)
GFX = {}
for dir, _, filenames in os.walk('assets/graphics'):
    for filename in filenames:
        _, ext = os.path.splitext(filename)
        if ext.lower() in (".png", ".jpg", ".jpeg"):
            filepath = os.path.join(dir, filename)
            GFX[filepath] = pygame.image.load(filepath).convert_alpha()

# spritesheets = {}
# gameobjects = []
# for gameobject in gameobjects:
#     spritesheets[gameobject.__name__] = Spritesheet(gameobject.image_path).get_animation_list((gamobject.frame_width, gameobject.frame_height))
spritesheets = {
    "Engineer": SpriteSheet(GFX["assets/graphics/players/engineer.png"]).get_animation_list((Engineer.frame_width, Engineer.frame_height), Engineer.animation_steps),
    "Soldier": SpriteSheet(GFX["assets/graphics/players/soldier.png"]).get_animation_list((Soldier.frame_width, Soldier.frame_height), Soldier.animation_steps),

    "Cannon": SpriteSheet(GFX["assets/graphics/weapons/cannon.png"]).get_animation_list((Cannon.frame_width, Cannon.frame_height), Cannon.animation_steps),

    "Carrot": SpriteSheet(GFX["assets/graphics/veggies/carrot-sheet.png"]).get_animation_list((Carrot.frame_width, Carrot.frame_height), Carrot.animation_steps),
    "Potato": SpriteSheet(GFX["assets/graphics/veggies/potato-sheet.png"]).get_animation_list((Potato.frame_width, Potato.frame_height), Potato.animation_steps),
    "Tomato": SpriteSheet(GFX["assets/graphics/veggies/tomato-sheet.png"]).get_animation_list((Tomato.frame_width, Tomato.frame_height), Tomato.animation_steps),
    "Peach": SpriteSheet(GFX["assets/graphics/veggies/peach-sheet.png"]).get_animation_list((Peach.frame_width, Peach.frame_height), Peach.animation_steps),

    "Trolley": SpriteSheet(GFX["assets/graphics/slingshots/trolley_static.png"]).get_animation_list((Trolley.frame_width, Trolley.frame_height), Trolley.animation_steps),
    "Base": SpriteSheet(GFX["assets/graphics/bases/base2.png"]).get_animation_list((Base.frame_width, Base.frame_height), Base.animation_steps),
}
