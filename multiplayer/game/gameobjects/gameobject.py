import pygame

class GameObject:
    def __init__(self, pos, vel, direction=(0, 0), shape=(32, 32),  scale=1):
        self.width, self.height = shape[0]*scale, shape[1]*scale
        self.rect = pygame.Rect(pos[0] - self.width/2, pos[1] - self.height/2, self.width, self.height)
        self.vel = vel
        self.direction = pygame.math.Vector2(direction)
        self.frame = [0, 0]

    @property
    def pos(self):
        return self.rect.centerx, self.rect.centery

    @pos.setter
    def pos(self, pos):
        self.rect.center = pos

    def draw(self, spritesheets, screen, debug=False):
        screen.blit(spritesheets[self.__class__.__name__][self.frame[0]][self.frame[1]], self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def update(self):
        self.rect.center += self.direction * self.vel
