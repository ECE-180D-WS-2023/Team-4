import pygame
import collections
from ...constants import *

class Inventory():
    def __init__(self):
        self.scale = 3
        self.item_queue = collections.deque()
        self.item_counts = {
            "Tomato": 0,
            "Peach": 0,
            "Carrot": 0,
            "Potato": 0,
            "Pumpkin": 0
        }

        # Use this instead of lambda to be able to pickle
        # def _():
        #     return 0
        # self.item_counts = collections.defaultdict(_)  # key: veggie classname (str), value: num in inventory (int)

    def draw(self, spritesheets, screen):
        screen.blit(pygame.transform.scale_by(spritesheets["Inventory"], self.scale), (0, SCREEN_HEIGHT - spritesheets["Inventory"].get_height() * self.scale))

        if len(self.item_queue) > 0:
            veggie_image = spritesheets["Inventory%s"%self.item_queue[0].__name__]
            veggie_image = pygame.transform.scale_by(veggie_image, self.scale)
            screen.blit(veggie_image, (90 * self.scale, SCREEN_HEIGHT - spritesheets["Inventory"].get_height() * self.scale + 5 * self.scale)) # 90 is the start of the placeholder of "next shooting type"

        screen.blit(pygame.transform.scale(spritesheets["Inventory%d"%self.item_counts["Tomato"]], (16*self.scale, 42*self.scale)), (5 * self.scale, SCREEN_HEIGHT - spritesheets["Inventory"].get_height() * self.scale))
        screen.blit(pygame.transform.scale(spritesheets["Inventory%d"%self.item_counts["Peach"]], (16*self.scale, 42*self.scale)), (5 * self.scale + 48, SCREEN_HEIGHT - spritesheets["Inventory"].get_height() * self.scale)) #48 comes from 16 * self.scale
        screen.blit(pygame.transform.scale(spritesheets["Inventory%d"%self.item_counts["Carrot"]], (16*self.scale, 42*self.scale)), (5 * self.scale + 48*2, SCREEN_HEIGHT - spritesheets["Inventory"].get_height() * self.scale))
        screen.blit(pygame.transform.scale(spritesheets["Inventory%d"%self.item_counts["Potato"]], (16*self.scale, 42*self.scale)), (5 * self.scale + 48*3, SCREEN_HEIGHT - spritesheets["Inventory"].get_height() * self.scale))
        screen.blit(pygame.transform.scale(spritesheets["Inventory%d"%self.item_counts["Pumpkin"]], (16*self.scale, 42*self.scale)), (5 * self.scale + 48*4, SCREEN_HEIGHT - spritesheets["Inventory"].get_height() * self.scale))
        screen.blit(pygame.transform.scale(spritesheets["Inventory%d"%len(self.item_queue)], (16*self.scale, 42*self.scale)), (90*self.scale, SCREEN_HEIGHT - spritesheets["Inventory"].get_height() * self.scale))

    def add(self, veggie):
        self.item_counts[veggie.__name__] += 1
        self.item_queue.append(veggie)

    def get(self):
        if len(self.item_queue) == 0:
            return False

        veggie = self.item_queue.popleft()
        self.item_counts[veggie.__name__] -= 1
        return veggie

    def __len__(self):
        return len(self.item_queue)
