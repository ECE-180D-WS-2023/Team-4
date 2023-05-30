import pygame
from .gameobject import *

def blitRotate(surf, image, origin, pivot, angle):
    """ Blit a rotated version of a given surface

    Args:
        surf (pygame.Surface): surface to blit onto
        image (pygame.Surface): surface to blit
        origin (Tuple): position of pivot in the larger system
        pivot (Tuple): position of pivot in terms of the image sprite's coordinates
        angle (int): number of degrees to rotate image
    """
    image_rect = image.get_rect(topleft = (origin[0] - pivot[0], origin[1] - pivot[1]))  # position the pivot point on origin
    pivot_to_center = image_rect.center - pygame.math.Vector2(origin)
    rotated_pivot_to_center = pivot_to_center.rotate(angle)  # note: pygame.Vector.rotate() is clockwise
    rotated_image_center = (origin[0] + rotated_pivot_to_center.x, origin[1] + rotated_pivot_to_center.y)
    rotated_image = pygame.transform.rotate(image, -angle)  # note: pygame.image.rotate() is counter-clockwise
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)

class Weapon(GameObject):
    def __init__(self, pos, vel, direction):
        super().__init__(pos, vel, direction)
        self.angle = 0

    def draw(self, spritesheets, screen):
        blitRotate(screen, spritesheets[self.__class__.__name__][self.frame[0]][self.frame[1]], self.pos, self.pivot, self.angle)

class Cannon(Weapon):
    pivot = (34, 170)
    power = 10
    strength = 20
    def __init__(self, pos, vel=0, direction=(0, 0)):
        super().__init__(pos, vel, direction)
