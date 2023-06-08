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

# Players
PLAYER_SCALE = 2

PLAYER_WALKING = 0
PLAYER_TRANSFORMING = 1
PLAYER_SHOOTING = 2

# Veggies
VEGGIE_SCALE = 2.5

# Slingshots
SLINGSHOT_SCALE = 1.5

# Shots
SHOT_SCALE = 1

# Bases
BASE_SCALE = 2

# Game Parameters
TEAM0_SPAWN = (SCREEN_WIDTH/2, SCREEN_HEIGHT*(1/5))
TEAM1_SPAWN = (SCREEN_WIDTH/2, SCREEN_HEIGHT*(4/5))

TEAM_BOUNDARIES = [
    # Team 0
    {
        "top": 0,
        "bottom": (SCREEN_HEIGHT / 2) - 75
    },
    # Team 1
    {
        "top": (SCREEN_HEIGHT / 2) + 75,
        "bottom": SCREEN_HEIGHT
    }
]

MAX_VEGGIES = 5
