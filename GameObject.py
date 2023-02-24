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

    # Position getter function
    @property
    def position(self):
        """
        Getter for PROPERTY position.

        INPUT:
        - NONE
        OUTPUT:
        a tuple of position x and y
        """
        print("I am at: ", self.m_pos_x, " and ", self.m_pos_y)
        return self.m_pos_x, self.m_pos_y

    # Position setter function 
    @position.setter
    def position(self, pos):
        """
        Setter for PROPERTY position

        INPUT:
        - pos: A tuple containing updated x and y position
        OUTPUT:
        - NONE
        """
        self.m_pos_x, self.m_pos_y = pos

    # Velocity getter function
    @property
    def velocity(self):
        """
        Getter for PROPERTY velocity

        INPUT:
        - NONE
        OUTPUT:
        a tuple of velocity x and y
        """
        print("My velocity is: ", self.m_vel_x, " and ", self.m_vel_y)
        return self.m_vel_x, self.m_vel_y
    
    # Velocity setter function
    @velocity.setter
    def velocity(self, vel):
        """
        Setter for PROPERTY velocity

        INPUT:
        - vel: A tuple containing updated x and y velocity
        OUTPUT:
        - NONE
        """
        self.m_vel_x, self.m_vel_y = vel


    # Health getter function
    @property
    def health(self):
        """
        Getter for PROPERTY health.

        INPUT:
        - NONE
        OUTPUT:
        - health value
        """
        print("Game Object current health: ", self.m_health)
        return self.m_health

    # Health setter function 
    @health.setter
    def health(self, new_health):
        """
        Setter for PROPERTY health

        INPUT:
        - new_health: new health value
        OUTPUT:
        - NONE
        """
        self.m_health = new_health


    # Team number getter function
    @property
    def team_num(self):
        """
        Getter for PROPERTY team number.

        INPUT:
        - NONE
        OUTPUT:
        - team number value
        """
        print("Current team number: ", self.m_team_num)
        return self.m_team_num

    # Team number setter function 
    @team_num.setter
    def team_num(self, new_team_num):
        """
        Setter for PROPERTY team number

        INPUT:
        - new team number: new team number
        OUTPUT:
        - NONE
        """
        self.m_team_num = new_team_num