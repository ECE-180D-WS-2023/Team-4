import pygame
from constants import *

class Instructions:
    def __init__(self, instruction):
        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.message = instruction
        self.counter = 0
        self.speed = 3
        done = False



    def update(self, screen):
        if self.counter < self.speed * len(self.message):
            self.counter += 1
        elif self.counter >= self.speed * len(self.message):
            done = True
        snip = self.font.render(self.message[0:self.counter//self.speed], True, 'white')
        screen.blit(snip, (0, 0))