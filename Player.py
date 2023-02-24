import pygame
from GameObject import GameObject
from Constants import *


class Player(GameObject):
    def __init__(self, role, name, state=PLAYER_WALKING, **profile):
        """
        INPUT:
        - role: player_role
            - ENGINEER(const.): 3
            - TRAVELER(const.): 4
            - SOLDIER(const.): 5
            - FARMER(const.): 6
        - state: player_state
            - PLAYER_WALKING(const.): 0
            - PLAYER_HARVESTING(const.): 1
            - PLAYER_SHOOTING(const.): 2
        - name: name
        - **profile: kwargs containing attribute values
            - pos_x: position in x axis
            - pos_y: position in y axis
            - vel_x: velocity in x direction
            - vel_y: velocity in y direction
            - health: object health/damage
            - team_num: object team number
        """
        super().__init__(**profile)
        self.m_role = role                                                         # Initialize player role
        self.m_state = state                                                       # Initialize player state
        self.m_backpack = {'potato':0, 'carrot':0, 'cabbage':0, 'pumpkin':0}       # Initialize player backpack
        self.m_weight = role                                                       # Initialize player weight
        self.m_name = name                                                         # Initialize player name

    # player name getter function
    @property
    def name(self):
        """
        Getter for PROPERTY name

        INPUT:
        - NONE
        OUTPUT:
        a string of player name
        """
        
        print("My name is: ", self.m_name)
        return self.m_name
    
    # player name setter function
    @name.setter
    def name(self, new_name):
        """
        Setter for PROPERTY name

        INPUT:
        - new_name: a new player name
        OUTPUT:
        - NONE
        """
        self.m_name = new_name
    
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
        
        print("My velocity is: ", self.m_vel_x , " and ", self.m_vel_y)
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
    
    # Getter method for player state
    @property
    def player_state(self):
        """
        Getter for PROPERTY player_state

        INPUT:
        - NONE
        OUTPUT:
        - player state
        """
        print("Current player state: ", self.m_state)
        return self.m_state
    
    # Setter method for player state
    @player_state.setter
    def player_state(self, new_player_state):
        """
        Setter for PROPERTY player_state

        INPUT:
        - new_player_state: new player state
        OUTPUT:
        - NONE
        """
        self.m_state = new_player_state

    # Getter method for player state
    @property
    def player_role(self):
        """
        Getter function for PROPERTY player_role

        INPUT:
        - NONE
        OUTPUT:
        - player role
        """
        print("Current player role: ", self.m_role)
        return self.m_role
    
    # Setter method for player role
    # @player_role.setter
    # def player_role(self, new_player_role):
    #     """
    #     Setter for PROPERTY player_role

    #     INPUT:
    #     - new_player_role: new player role
    #     OUTPUT:
    #     - NONE
    #     """
    #     self.m_role = new_player_role


    def harvest(self, item):
        """
        Add items to player backpack (only when player is in HARVESTING mode)

        if the player's backpack is full, then you cannot harvest that veggie and it rots.

        """
        if (self.m_state != PLAYER_HARVESTING):
            print("not in harvesting mode")

        elif self.m_backpack.get(item) < 5 and self.m_backpack.get(item) >= 0:
            print("You successfully added ", item)
            self.m_backpack[item] += 1
            # make veggie disapper in the arena and map
        else:
            print("sorry backpack full")
    
    def attack(self, item):
        """
        ##########################################
        UNDER CONSTRUCTION!!!
        ##########################################

        Attack using an item in the player backpack (only when player is in SHOOTING mode)

        if the player's backpack is empty, then you cannot shoot.
        
        """
        if (self.m_state != PLAYER_SHOOTING):
            print("Player not in shooting mode")
        elif self.m_backpack.get(item) >= 1:
            self.m_backpack[item] -= 1
        else:
            # This should never be executed, since we won't display veggies that you don't have.
            print("sorry no ammo")
    
    def display_backpack(self):
        """
        Display player backpack
        """
        print(self.m_backpack)
        return self.m_backpack


        