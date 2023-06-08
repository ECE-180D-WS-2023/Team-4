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
    "Student": SpriteSheet(GFX["assets/graphics/players/student.png"]).get_animation_list((Student.frame_width, Student.frame_height), Student.animation_steps),
    "Soldier": SpriteSheet(GFX["assets/graphics/players/soldier.png"]).get_animation_list((Soldier.frame_width, Soldier.frame_height), Soldier.animation_steps),
    "Enchantress": SpriteSheet(GFX["assets/graphics/players/enchantress.png"]).get_animation_list((Enchantress.frame_width, Enchantress.frame_height), Enchantress.animation_steps),

    "Cannon": SpriteSheet(GFX["assets/graphics/weapons/cannon.png"]).get_animation_list((Cannon.frame_width, Cannon.frame_height), Cannon.animation_steps),
    "VenomCrossbow": SpriteSheet(GFX["assets/graphics/weapons/venom_crossbow.png"]).get_animation_list((VenomCrossbow.frame_width, VenomCrossbow.frame_height), VenomCrossbow.animation_steps),
    "DemonicCrossbow": SpriteSheet(GFX["assets/graphics/weapons/demonic_crossbow.png"]).get_animation_list((DemonicCrossbow.frame_width, DemonicCrossbow.frame_height), DemonicCrossbow.animation_steps),
    "DivineCrossbow": SpriteSheet(GFX["assets/graphics/weapons/divine_crossbow.png"]).get_animation_list((DivineCrossbow.frame_width, DivineCrossbow.frame_height), DivineCrossbow.animation_steps),
    "FireCrossbow": SpriteSheet(GFX["assets/graphics/weapons/fire_crossbow.png"]).get_animation_list((FireCrossbow.frame_width, FireCrossbow.frame_height), FireCrossbow.animation_steps),
    "SkullCrossbow": SpriteSheet(GFX["assets/graphics/weapons/skull_crossbow.png"]).get_animation_list((SkullCrossbow.frame_width, SkullCrossbow.frame_height), SkullCrossbow.animation_steps),

    "Carrot": SpriteSheet(GFX["assets/graphics/veggies/carrot-sheet.png"]).get_animation_list((Carrot.frame_width, Carrot.frame_height), Carrot.animation_steps),
    "Potato": SpriteSheet(GFX["assets/graphics/veggies/potato-sheet.png"]).get_animation_list((Potato.frame_width, Potato.frame_height), Potato.animation_steps),
    "Tomato": SpriteSheet(GFX["assets/graphics/veggies/tomato-sheet.png"]).get_animation_list((Tomato.frame_width, Tomato.frame_height), Tomato.animation_steps),
    "Peach": SpriteSheet(GFX["assets/graphics/veggies/peach-sheet.png"]).get_animation_list((Peach.frame_width, Peach.frame_height), Peach.animation_steps),
    "Pumpkin": SpriteSheet(GFX["assets/graphics/veggies/pumpkin-sheet.png"]).get_animation_list((Pumpkin.frame_width, Pumpkin.frame_height), Pumpkin.animation_steps),

    "Trolley": SpriteSheet(GFX["assets/graphics/slingshots/trolley_static.png"]).get_animation_list((Trolley.frame_width, Trolley.frame_height), Trolley.animation_steps),
    "Base": SpriteSheet(GFX["assets/graphics/bases/base2.png"]).get_animation_list((Base.frame_width, Base.frame_height), Base.animation_steps),

    "Inventory": pygame.image.load("assets/graphics/inventory/inventory-display.png"),
    "InventoryCarrot": pygame.image.load("assets/graphics/inventory/carrot-inventory.png").convert_alpha(),
    "InventoryPotato": pygame.image.load("assets/graphics/inventory/potato-inventory.png").convert_alpha(),
    "InventoryPumpkin": pygame.image.load("assets/graphics/inventory/pumpkin-inventory.png").convert_alpha(),
    "InventoryTomato": pygame.image.load("assets/graphics/inventory/tomato-inventory.png").convert_alpha(),
    "InventoryPeach": pygame.image.load("assets/graphics/inventory/peach-inventory.png").convert_alpha(),
    "Inventory0": pygame.image.load("assets/graphics/inventory/zero.png").convert_alpha(),
    "Inventory1": pygame.image.load("assets/graphics/inventory/one.png").convert_alpha(),
    "Inventory2": pygame.image.load("assets/graphics/inventory/two.png").convert_alpha(),
    "Inventory3": pygame.image.load("assets/graphics/inventory/three.png").convert_alpha(),
    "Inventory4": pygame.image.load("assets/graphics/inventory/four.png").convert_alpha(),
    "Inventory5": pygame.image.load("assets/graphics/inventory/five.png").convert_alpha(),
}

SFX = {
    "harvest": pygame.mixer.Sound('assets/sounds/harvest.mp3'),
    "shoot": pygame.mixer.Sound('assets/sounds/shotgun-firing.mp3'),
    "hit": pygame.mixer.Sound('assets/sounds/collision.mp3'),
}
