import pygame

class GameObject:
    def __init__(self, pos, vel, direction=(0, 0), shape=(32, 32),  scale=1):
        width, height = shape[0]*scale, shape[1]*scale
        self.rect = pygame.Rect(pos[0] - width/2, pos[1] - height/2, width, height)
        self.vel = vel
        self.direction = pygame.math.Vector2(direction)
        self.frame = [0, 0]

    @property
    def pos(self):
        return self.rect.centerx, self.rect.centery

    @pos.setter
    def pos(self, pos):
        self.rect.center = pos

    def draw(self, spritesheets, screen):
        screen.blit(spritesheets[self.__class__.__name__][self.frame[0]][self.frame[1]], self.rect)

    def update(self):
        self.rect.center += self.direction * self.vel
