"""GameObject class

The GameObject class contains attributes that are common to *all* game objects
"""

import pygame
from typing import List, Set, Dict, Tuple
from constants import *

class GameObject(pygame.sprite.Sprite):
    def __init__(self, shape: Tuple[int, int], pos: Tuple[int, int], vel: Tuple[int, int], team_num: int) -> None:
        super().__init__() # initialize sprite class

        # Attribute Initialization
        self.m_pos_x = pos[0]                 # Initialize x position
        self.m_pos_y = pos[1]                 # Initialize y position
        self.m_vel_x = vel[0]                 # Initialize x velocity
        self.m_vel_y = vel[1]                 # Initialize y velocity
        self.m_team_num = team_num            # Initialize team number

        # Pygame sprite initialization
        self.surf = pygame.Surface(shape)
        self.surf.fill((255, 255, 255)) # TODO: maybe generalize this?
        self.rect = self.surf.get_rect()
        self.rect.center = pos

    @property
    def position(self):
        print("I am at: ", self.m_pos_x, " and ", self.m_pos_y)
        return self.m_pos_x, self.m_pos_y

    @position.setter
    def position(self, pos: Tuple[int, int]):
        self.m_pos_x, self.m_pos_y = pos

    @property
    def velocity(self) -> Tuple[int, int]:
        print("My velocity is: ", self.m_vel_x, " and ", self.m_vel_y)
        return self.m_vel_x, self.m_vel_y
    
    @velocity.setter
    def velocity(self, vel: Tuple[int, int]) -> None:
        self.m_vel_x, self.m_vel_y = vel

    @property
    def team_num(self) -> int:
        print("Current team number: ", self.m_team_num)
        return self.m_team_num

    @team_num.setter
    def team_num(self, team_num) -> None:
        self.m_team_num = team_num
