import pygame
from constants import *

class Instructions:
    def __init__(self, text, slowness=2, font_size=50, line_padding=4):
        self.font = pygame.font.Font("assets/fonts/instruction.ttf", font_size)
        self.message = text.split("\n")
        self.total_length = len(text)        
        self.counter = 0
        self.slowness = slowness
        self.line_y_dist = font_size + line_padding

    def update(self, screen):
        if self.counter < self.slowness * self.total_length:
            self.counter += 1
        for idx, line in enumerate(self.message):
            # self.counter//self.slowness is the number of displayed characters
            num_chars = max(0, self.counter//self.slowness - len(''.join(self.message[0:idx])))
            snip = self.font.render(line[0:num_chars], True, 'white')
            screen.blit(snip, (500, 300 + idx * self.line_y_dist))
