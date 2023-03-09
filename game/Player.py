from GameObject import GameObject
from constants import *
from typing import List, Set, Dict, Tuple
import pygame

class Player(GameObject):
    # TODO: remove role attribute in favor of subclasses
    def __init__(self, pos, vel, team_num, role, name, state=PLAYER_WALKING, health=100):
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
        super().__init__((PLAYER_WIDTH, PLAYER_HEIGHT), pos, vel, team_num, img='assets/players/engineer.png', animation_steps=[3,3,3,3])
        self.m_role = role                                                         # Initialize player role
        self.m_state = state                                                       # Initialize player state
        self.m_backpack = {"potato":0, "carrot":0, "cabbage":0, "pumpkin":0}       # Initialize player backpack
        self.m_weight = role                                                       # Initialize player weight
        self.m_name = name                                                         # Initialize player name
        self.m_health = health                                                     # Initialize player health
        self.m_mounted = False

    @property
    def name(self) -> str:
        print("My name is: ", self.m_name)
        return self.m_name

    @name.setter
    def name(self, new_name: str) -> None:
        self.m_name = new_name

    @property
    def player_state(self) -> int:
        print("Current player state: ", self.m_state)
        return self.m_state

    @player_state.setter
    def player_state(self, new_player_state: int) -> None:
        self.m_state = new_player_state

    @property
    def health(self) -> int:
        print("Current base shield: ", self.m_health)
        return self.m_health

    @health.setter
    def health(self, new_health: int) -> None:
        self.m_health = new_health

    @property
    def player_role(self):
        print("Current player role: ", self.m_role)
        return self.m_role

    def is_alive(self):
        return self.health > 0

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
            self.display_backpack()
        else:
            print("sorry backpack full")

    def toggle_mount(self, slingshot):
        if self.m_mounted:
            self.m_mounted = False
            self.player_state = PLAYER_WALKING
        elif pygame.sprite.collide_rect(self, slingshot):
            self.m_mounted = True
            self.position = slingshot.position
            self.player_state = PLAYER_SHOOTING

    def update(self, js_action, screen):
        x_action, y_action = js_action

        if self.m_state == PLAYER_HARVESTING:
            super().update(screen)
            return
        
        elif self.m_state == PLAYER_WALKING:
            actions = []

            if y_action == -1:     # Up
                self.m_pos_y -= self.m_vel_y
                actions.append(3)
            if y_action == 1:      # Down
                self.m_pos_y += self.m_vel_y
                actions.append(0)
            if x_action == -1:     # Left
                self.m_pos_x -= self.m_vel_x
                actions.append(1)
            if x_action == 1:      # Right
                self.m_pos_x += self.m_vel_x
                actions.append(2)

            # Don't allow player to move off screen
            if self.rect.left < 0:
                self.m_pos_x = PLAYER_WIDTH/2
            if self.rect.right > SCREEN_WIDTH:
                self.m_pos_x = SCREEN_WIDTH-PLAYER_WIDTH
            if self.rect.top <= 0:
                self.m_pos_y = PLAYER_HEIGHT
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.m_pos_y = SCREEN_HEIGHT-PLAYER_HEIGHT

            action = actions[-1] if (len(actions) > 0) else None
            super().update(screen, action)
        
        elif self.m_state == PLAYER_SHOOTING:
            color = (255,0,0)
            aim_surf = pygame.Surface((10,60)) # dimensions for aiming rect
            aim_surf.fill(color)
            aimer = aim_surf.get_rect()
            aimer.center = (self.position[0] + 32, self.position[1] - 30)
            print(x_action)
            screen.blit(pygame.transform.rotate(aim_surf, x_action), aimer)
            super().update(screen)
            return

        
        

    def switch_state(self, pressed_key):
        if pressed_key[K_0]:
            self.player_state = PLAYER_WALKING
            print("Walking!")
        if pressed_key[K_1]:
            self.player_state = PLAYER_HARVESTING
            print("Harvesting!")
        if pressed_key[K_2]:
            self.player_state = PLAYER_SHOOTING
            print("Shooting!")

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
            self.display_backpack()
            return True
        else:
            # This should never be executed, since we won't display veggies that you don't have.
            print("sorry no ammo")
            return False

    def display_backpack(self):
        print(self.m_backpack)
        return self.m_backpack

class Engineer(Player):
    def __init__(self):
        pass


class Traveler(Player):
    def __init__(self):
        pass

class Soldier(Player):
    def __init__(self):
        pass

class Farmer(Player):
    def __init__(self):
        pass
