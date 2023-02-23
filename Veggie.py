
import pygame
from GameObject import GameObject
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


class Veggie(GameObject):
    def __init__(self, veggie_type, **profile):
        super().__init__(**profile)
        self.m_type = veggie_type


    def whoami(self):
        print("I am ", self.m_type, " and I have ", self.m_health)




