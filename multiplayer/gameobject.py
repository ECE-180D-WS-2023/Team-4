import pygame

class GameObject:
    def __init__(self, pos, vel, direction=(0, 0)):
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.vel = vel
        self.direction = pygame.math.Vector2(direction)

    @property
    def pos(self):
        return self.rect.centerx, self.rect.centery

    @pos.setter
    def pos(self, pos):
        self.rect.center = pos

    def update(self):
        self.rect.center += self.direction * self.vel
