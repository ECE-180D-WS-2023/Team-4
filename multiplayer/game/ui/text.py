import pygame
from ..constants import *

class Text:
    def __init__(self, pos, text, font="assets/fonts/instruction.ttf", font_size=50, color=(255,255,255), shadow=False, shadow_offset=2):
        self.color = color
        self.font = pygame.font.Font(font, font_size)
        self.surf = self.font.render(text, True, color)
        self.rect = self.surf.get_rect(center=pos)
        if shadow:
            self.shadow = self.font.render(text, True, (150, 150, 150))
        else:
            self.shadow = False

    def draw(self, screen):
        if self.shadow:
            screen.blit(self.shadow, (self.rect.x, self.rect.y + 4))
        screen.blit(self.surf, self.rect)

class TypewriterText:
    def __init__(self, pos, text, font="assets/fonts/instruction.ttf", font_size=50, color=(255,255,255), slowness=2, line_padding=4, align="center"):
        self.pos = pos
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.message_list = text.split("\n")
        self.total_length = len(''.join(self.message_list[0:len(self.message_list)]))
        self.counter = 0
        self.slowness = slowness
        self.line_y_dist = font_size + line_padding
        self.align = align

    @property
    def done(self):
        return self.counter == self.slowness * self.total_length

    def update(self, screen):
        if self.counter < self.slowness * self.total_length:
            self.counter += 1
        for line_num, line in enumerate(self.message_list):
            # Note: self.counter//self.slowness is the number of displayed characters
            num_chars = max(0, self.counter//self.slowness - len(''.join(self.message_list[0:line_num])))
            snip = self.font.render(line[0:num_chars], True, self.color)
            if self.align == "center":
                screen.blit(snip, (self.pos[0] - snip.get_width()/2, self.pos[1] + line_num * self.line_y_dist))
            elif self.align == "left":
                screen.blit(snip, (self.pos[0], self.pos[1] + line_num * self.line_y_dist))
