import pygame
import collections
import Spritesheet
from constants import *

scale = 3
class Inventory():
    def __init__(self):
        self.queue = collections.deque()
        self.item_counts = collections.defaultdict(lambda: 0)
        self.inventory_display = pygame.image.load("assets/inventory/inventory-display.png").convert_alpha()
        self.inventory_display = pygame.transform.scale(self.inventory_display, (self.inventory_display.get_width() * scale, self.inventory_display.get_height() * scale))
        self.veggie_images = {
            "Carrot": pygame.image.load("assets/inventory/carrot-inventory.png").convert_alpha(),
            "Potato": pygame.image.load("assets/inventory/potato-inventory.png").convert_alpha(),
            "Pumpkin": pygame.image.load("assets/inventory/pumpkin-inventory.png").convert_alpha(),
            "Strawberry": pygame.image.load("assets/inventory/strawberry-inventory.png").convert_alpha(),
            "Peach": pygame.image.load("assets/inventory/peach-inventory.png").convert_alpha(),
        }
        self.digit_images = { #numbers are 16x42 pixels
            0: pygame.transform.scale(pygame.image.load("assets/inventory/zero.png").convert_alpha(), (16 * scale, 42 * scale)),
            1: pygame.transform.scale(pygame.image.load("assets/inventory/one.png").convert_alpha(), (16 * scale, 42 * scale)),
            2: pygame.transform.scale(pygame.image.load("assets/inventory/two.png").convert_alpha(), (16 * scale, 42 * scale)),
            scale: pygame.transform.scale(pygame.image.load("assets/inventory/three.png").convert_alpha(), (16 * scale, 42 * scale)),
            4: pygame.transform.scale(pygame.image.load("assets/inventory/four.png").convert_alpha(), (16 * scale, 42 * scale)),
            5: pygame.transform.scale(pygame.image.load("assets/inventory/five.png").convert_alpha(), (16 * scale, 42 * scale)),
        }

    def draw(self, screen):
        screen.blit(self.inventory_display, (0, SCREEN_HEIGHT - self.inventory_display.get_height()))
        if len(self.queue) > 0:
            veggie_image = self.veggie_images[self.queue[0].__name__]
            veggie_image = pygame.transform.scale(veggie_image, (veggie_image.get_width() * scale, veggie_image.get_height() * scale))
            screen.blit(veggie_image, (90 * scale, SCREEN_HEIGHT - self.inventory_display.get_height() + 5 * scale)) # 90 is the start of the placeholder of "next shooting type"

        screen.blit(self.digit_images[self.item_counts["Carrot"]], (5 * scale, SCREEN_HEIGHT - self.inventory_display.get_height()))
        screen.blit(self.digit_images[self.item_counts["Potato"]], (5 * scale + 48, SCREEN_HEIGHT - self.inventory_display.get_height())) #48 comes from 16 * scale
        screen.blit(self.digit_images[self.item_counts["Pumpkin"]], (5 * scale + 48*2, SCREEN_HEIGHT - self.inventory_display.get_height()))
        screen.blit(self.digit_images[self.item_counts["Strawberry"]], (5 * scale + 48*3, SCREEN_HEIGHT - self.inventory_display.get_height()))
        screen.blit(self.digit_images[self.item_counts["Peach"]], (5 * scale + 48*4, SCREEN_HEIGHT - self.inventory_display.get_height()))
        screen.blit(self.digit_images[len(self.queue)], (90*scale, SCREEN_HEIGHT - self.inventory_display.get_height()))

    def add(self, veggie):
        self.item_counts[veggie.__name__] += 1
        self.queue.append(veggie)

    def get(self):
        if len(self.queue) == 0:
            return False

        veggie = self.queue.popleft()
        self.item_counts[veggie.__name__] -= 1
        return veggie

    def __len__(self):
        return len(self.queue)