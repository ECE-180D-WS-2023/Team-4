import pygame
from Constants import *
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
)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, **profile):
        """
        INPUT: 
            - **profile: kwargs containing attribute values
                - pos_x: position in x axis
                - pos_y: position in y axis
                - vel_x: velocity in x direction
                - vel_y: velocity in y direction
                - health: object health/damage
                - team_num: object team number
        """
        super().__init__()            # Initialize Sprite class
        # Create game object graphics  
        self.surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = (profile["pos_x"], profile["pos_y"])
        # Attribute Initialization
        self.m_pos_x = profile["pos_x"]                 # Initialize x position
        self.m_pos_y = profile["pos_y"]                 # Initialize y position
        self.m_vel_x = profile["vel_x"]                 # Initialize x velocity
        self.m_vel_y = profile["vel_y"]                 # Initialize y velocity
        self.m_health = profile["health"]               # Initialize object health
        self.m_team_num = profile["team_num"]           # Initialize team number


    def get_pos(self):
        print(self.m_pos_x, " and ", self.m_pos_y)