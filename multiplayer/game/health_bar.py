import pygame

class HealthBar:
    def __init__(self, owner, width, height=12, padding=10):
        self.owner = owner
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), (self.owner.rect.x, self.owner.rect.y - 10, self.width, self.height))  # Red
        pygame.draw.rect(screen, (0,128,0), (self.owner.rect.x, self.owner.rect.y - 10, (self.owner.health/self.owner.max_health)*(self.width), self.height))  # Green
