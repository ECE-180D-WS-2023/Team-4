import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    K_SPACE,
    K_ESCAPE,
    K_q,
    KEYDOWN,
    QUIT,
    K_TAB,
    K_0,
    K_1,
    K_2,
    K_p
)

# Arena Parameters
SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1600

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_SCALE = 2

SLINGSHOT_WIDTH = 32
SLINGSHOT_HEIGHT = 32
SLINGSHOT_SCALE = 1

SHOT_WIDTH = 32
SHOT_HEIGHT = 32
SHOT_SCALE = 1

VEGGIE_WIDTH = 32
VEGGIE_HEIGHT = 32
VEGGIE_SCALE = 1

BASE_WIDTH = 93
BASE_HEIGHT = 100
BASE_SCALE = 1

MAX_VEGGIES = 10

# Veggie damage
POTATO_DAMAGE = 5
CARROT_DAMAGE = 7
CABBAGE_DAMAGE = 10
PUMPKIN_DAMAGE = 15
VEGGIE_VELOCITY = 10

# Veggie weights

# Player State
PLAYER_WALKING = 0
PLAYER_HARVESTING = 1
PLAYER_SHOOTING = 2

# Player Weight
WEIGHT_FACTOR = 0.2

# Player Role
PLAYER_ENGINEER = 3
PLAYER_FARMER = 4
PLAYER_SOLDIER = 5
PLAYER_TRAVELER = 6

# Game object team assignment
TEAM1 = 1
TEAM2 = 2

# Game Flow
GAME_ON = 1
