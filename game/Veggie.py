
import pygame
from GameObject import GameObject
from constants import *
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
        self.m_type = veggie_type               # Type of veggie
        self.m_harvest_time = veggie_dict[veggie_type] / 2   # Harvest_time = damage / 2
        


    def whoami(self):
        print("I am ", self.m_type, " and I have ", self.m_health)

    # Veggie type getter function
    @property
    def veggie_type(self):
        """
        Getter for PROPERTY veggie_type.

        INPUT:
        - NONE
        OUTPUT:
        - veggie_type
        """
        print("Current veggie type: ", self.m_type)
        return self.m_type

    # Veggie type setter function 
    @veggie_type.setter
    def veggie_type(self, new_veggie_type):
        """
        Setter for PROPERTY veggie type

        INPUT:
        - new_veggie_type: new veggie type
        OUTPUT:
        - NONE
        """
        self.m_type = new_veggie_type
