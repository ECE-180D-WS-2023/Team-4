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
        self.role = role
        self.state = state
        self.backpack = {}
        self.weight = role
        self.name = name
        self.health = health
        self.mounted = False

    def is_alive(self):
        return self.health > 0

    def harvest(self, item):
        """
        Add items to player backpack (only when player is in HARVESTING mode)

        if the player's backpack is full, then you cannot harvest that veggie and it rots.

        """
        if (self.state != PLAYER_HARVESTING):
            print("not in harvesting mode")

        elif self.backpack[item] < 5 and self.backpack[item] >= 0:
            print("You successfully added ", item)
            self.backpack[item] += 1
            # make veggie disapper in the arena and map
            self.display_backpack()
        else:
            print("sorry backpack full")

    def toggle_mount(self, slingshot):
        if self.mounted:
            self.mounted = False
            self.state = PLAYER_WALKING
        elif pygame.sprite.collide_rect(self, slingshot):
            self.mounted = True
            self.pos = slingshot.pos
            self.state = PLAYER_SHOOTING

    def update(self, js_action, screen):
        x_action, y_action = js_action

        if self.state == PLAYER_HARVESTING:
            super().update(screen)
            return

        elif self.state == PLAYER_WALKING:
            actions = []

            if y_action == -1:     # Up
                self.pos_y -= self.vel_y
                actions.append(3)
            if y_action == 1:      # Down
                self.pos_y += self.vel_y
                actions.append(0)
            if x_action == -1:     # Left
                self.pos_x -= self.vel_x
                actions.append(1)
            if x_action == 1:      # Right
                self.pos_x += self.vel_x
                actions.append(2)

            # Don't allow player to move off screen
            if self.rect.left < 0:
                self.pos_x = PLAYER_WIDTH/2
            if self.rect.right > SCREEN_WIDTH:
                self.pos_x = SCREEN_WIDTH-PLAYER_WIDTH
            if self.rect.top <= 0:
                self.pos_y = PLAYER_HEIGHT
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.pos_y = SCREEN_HEIGHT-PLAYER_HEIGHT

            action = actions[-1] if (len(actions) > 0) else None
            super().update(screen, action)
            return

        elif self.state == PLAYER_SHOOTING:
            aiming_indicator = pygame.image.load("assets/players/cannon.png")
            self.blitRotate(screen,
                            aiming_indicator,
                            (self.pos[0], self.pos[1]),
                            (34,160),
                            x_action)
            super().update(screen)
            return


    def blitRotate(self, surf, image, origin:Tuple[int, int], pivot:Tuple[int, int], angle):
        '''
        INPUT:
            - origin: where do you want to put it in the larger system
            - pivot: In the image sprite coordinates, where is the relative pivot

        For example:
        player: 32 x 32
        canon: 67 x 150

        We want to set the pivot at the center bottom of the canon, but we have
        to use the canon coordinate system, i.e. pivot=(32, 160)
        If you set the pivot to (0,0), for example, it will rotate wrt the top
        left corner of the canon.

        And then, we decide where to put that pivot in the larger coordinate system.
        In this case, we want to put that pivot on top of the player's position,
        hence origin=(self.pos[0], self.pos[1])

        '''
        image_rect = image.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        surf.blit(rotated_image, rotated_image_rect)

    def switch_state(self, pressed_key):
        if pressed_key[K_0]:
            self.state = PLAYER_WALKING
            print("Walking!")
        if pressed_key[K_1]:
            self.state = PLAYER_HARVESTING
            print("Harvesting!")
        if pressed_key[K_2]:
            self.state = PLAYER_SHOOTING
            print("Shooting!")

    def attack(self, item):
        """
        Attack using an item in the player backpack (only when player is in SHOOTING mode)

        if the player's backpack is empty, then you cannot shoot.

        """
        if (self.state != PLAYER_SHOOTING):
            print("Player not in shooting mode")
        elif self.backpack[item] >= 1:
            self.backpack[item] -= 1
            self.display_backpack()
            return True
        else:
            # This should never be executed, since we won't display veggies that you don't have.
            print("sorry no ammo")
            return True

    def display_backpack(self):
        print(self.backpack)
        return self.backpack

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
