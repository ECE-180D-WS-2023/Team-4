from GameObject import GameObject
from constants import *
import math
import collections
from typing import List, Set, Dict, Tuple
import pygame
from pygame import mixer

mixer.init()
walking_sound = pygame.mixer.Sound('assets/music/walking.mp3')
walking_sound.set_volume(1.5)
shooting_sound = pygame.mixer.Sound('assets/music/shotgun-firing.mp3')

class Player(GameObject):
    # TODO: remove role attribute in favor of subclasses
    def __init__(self, pos, vel, team_num, role, name, img, state=PLAYER_WALKING, health=100):
        super().__init__((PLAYER_WIDTH, PLAYER_HEIGHT), pos, vel, team_num, img, animation_steps=[3,3,3,3], scale=PLAYER_SCALE)
        self.role = role
        self.state = state
        self.backpack = collections.deque()
        self.weight = role
        self.name = name
        self.health = health
        self.mounted = False

    def attack(self, angle, sprite_groups):
        """
        Attack using an item in the player backpack (only when player is in SHOOTING mode)

        if the player's backpack is empty, then you cannot shoot.

        """
        if self.state != PLAYER_SHOOTING:
            return

        # if self.backpack.get(veggie_class.__name__, 0) == 0:
        #     return

        # self.backpack[veggie_class.__name__] -= 1

        if len(self.backpack) == 0:
            return

        veggie_class = self.backpack.popleft()

        x_vel = math.sin(math.radians(angle%360)) * VEGGIE_VELOCITY
        y_vel = math.cos(math.radians(angle%360)) * VEGGIE_VELOCITY
        veggie = veggie_class(self.pos, (x_vel, y_vel), self.team_num)
        veggie.add(*sprite_groups)

        shooting_sound.play()

    def harvest(self, veggies_group):
        if self.state == PLAYER_SHOOTING:
            return

        veggie = pygame.sprite.spritecollideany(self, veggies_group)
        if veggie:
            if pygame.sprite.spritecollideany(self, veggies_group, pygame.sprite.collide_mask):
                # self.backpack[veggie.__class__.__name__] = self.backpack.get(veggie.__class__.__name__, 0) + 1
                walking_sound.play()
                self.backpack.append(veggie.__class__)
                veggie.kill()

    def toggle_mount(self, slingshot):
        if self.mounted:
            self.mounted = False
            self.state = PLAYER_WALKING
            
        elif pygame.sprite.collide_rect(self, slingshot):
            if pygame.sprite.spritecollide(self, [slingshot], False, pygame.sprite.collide_mask):
                self.mounted = True
                self.pos = slingshot.pos
                self.state = PLAYER_SHOOTING

    def update(self, js_action, angle, screen):
        x_action, y_action = js_action
        if self.state == PLAYER_WALKING:
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
            player_rect_width = PLAYER_WIDTH*PLAYER_SCALE
            player_rect_height = PLAYER_HEIGHT*PLAYER_SCALE

            if self.pos_x < player_rect_width/2:
                self.pos_x = player_rect_width/2
            if self.pos_x > SCREEN_WIDTH - player_rect_width/2:
                self.pos_x = SCREEN_WIDTH - player_rect_width/2
            if self.pos_y < player_rect_height/2:
                self.pos_y = player_rect_height/2
            if self.pos_y > SCREEN_HEIGHT - player_rect_height/2:
                self.pos_y = SCREEN_HEIGHT - player_rect_height/2

            action = actions[-1] if (len(actions) > 0) else None
            super().update(screen, action)
            return

        elif self.state == PLAYER_SHOOTING:
            aiming_indicator = pygame.image.load("assets/players/cannon.png")
            self.blitRotate(screen,
                            aiming_indicator,
                            (self.pos[0], self.pos[1]),
                            (34,160),
                            angle)
            super().update(screen)
            return


    def blitRotate(self, surf, image, origin:Tuple[int, int], pivot:Tuple[int, int], angle):
        '''
        INPUT:
            - origin: position of the pivot point in the larger system
            - pivot: in the image sprite coordinates, where is the relative pivot

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
        image_rect = image.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))  # position the image in the correct location
        pivot_to_center = image_rect.center - pygame.math.Vector2(origin)
        rotated_pivot_to_center = pivot_to_center.rotate(-angle)
        rotated_image_center = (origin[0] + rotated_pivot_to_center.x, origin[1] + rotated_pivot_to_center.y)
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        surf.blit(rotated_image, rotated_image_rect)

    def switch_state(self, pressed_key):
        if pressed_key[K_0]:
            self.m_mounted = False
            self.player_state = PLAYER_WALKING
            print("Walking!")
        if pressed_key[K_1]:
            self.state = PLAYER_HARVESTING
            print("Harvesting!")
        if pressed_key[K_2]:
            self.state = PLAYER_SHOOTING
            print("Shooting!")

class Engineer(Player):
    def __init__(self, pos, vel, team_num, role, name, state=PLAYER_WALKING, health=100):
        super().__init__(pos, vel, team_num, role, name, img="assets/players/engineer.png", state=PLAYER_WALKING, health=100)

class DarthVader(Player):
    def __init__(self, pos, vel, team_num, role, name, state=PLAYER_WALKING, health=100):
        super().__init__(pos, vel, team_num, role, name, img="assets/players/darthvader.png", state=PLAYER_WALKING, health=100)

class Soldier(Player):
    def __init__(self, pos, vel, team_num, role, name, state=PLAYER_WALKING, health=100):
        super().__init__(pos, vel, team_num, role, name, img="assets/players/soldier.png", state=PLAYER_WALKING, health=100)

class Farmer(Player):
    def __init__(self, pos, vel, team_num, role, name, state=PLAYER_WALKING, health=100):
        super().__init__(pos, vel, team_num, role, name, state=PLAYER_WALKING, health=100)
