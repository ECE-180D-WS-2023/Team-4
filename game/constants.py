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
    K_2
)

# Arena Parameters
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
SLINGSHOT_WIDTH = 50
SLINGSHOT_HEIGHT = 50
SHOT_WIDTH = 5
SHOT_HEIGHT = 10
VEGGIE_WIDTH = 16
VEGGIE_HEIGHT = 16
BASE_WIDTH = 64
BASE_HEIGHT = 64

# Veggie damage
VEGGIE_POTATO = 5
VEGGIE_CARROT = 7
VEGGIE_CABBAGE = 10
VEGGIE_PUMPKIN = 15
veggie_dict = {"carrot": VEGGIE_CARROT, "cabbage": VEGGIE_CABBAGE,
               "potato": VEGGIE_POTATO, "pumpkin": VEGGIE_PUMPKIN}

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
