import pygame
from GameObject import *

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
    def __init__(self, pos, vel, team_num, img):
        super().__init__((WEAPON_WIDTH, WEAPON_HEIGHT), pos, vel, team_num, img, animation_steps=[1], scale=WEAPON_SCALE)

    def blitRotate(self, surf, image, origin:Tuple[int, int], pivot:Tuple[int, int], angle):
        '''
        INPUT:
            - origin: position of the pivot point in the larger system
            - pivot: in the image sprite coordinates, where is the relative pivot

        For example:
        player: 32 x 32
        canon: 67 x 150

        We want to set the pivot at the center bottom of the canon, but we have
        to use the canon coordinate system, i.e. pivot=(32, 160)
        If you set the pivot to (0,0), for example, it will rotate wrt the top
        left corner of the canon.

        And then, we decide where to put that pivot in the larger coordinate system.
        In this case, we want to put that pivot on top of the player's position,
        hence origin=(self.pos[0], self.pos[1])

        '''
        image_rect = image.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))  # position the image in the correct location
        pivot_to_center = image_rect.center - pygame.math.Vector2(origin)
        rotated_pivot_to_center = pivot_to_center.rotate(-angle)
        rotated_image_center = (origin[0] + rotated_pivot_to_center.x, origin[1] + rotated_pivot_to_center.y)
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        surf.blit(rotated_image, rotated_image_rect)

class Cannon(Weapon):
    def __init__(self, pos, team_num, vel=(0,0)):
        super().__init__(pos=pos, vel=vel, team_num=team_num, img="assets/weapons/cannon.png")
        self.pivot = (34, 160)
        self.power = 10
        self.strength = 20

class Newb_Crossbow(Weapon):
    def __init__(self, pos, team_num, vel=(0,0)):
        super().__init__(pos=pos, vel=vel, team_num=team_num, img="assets/weapons/newb_crossbow.png")
        self.pivot = (32, 69)
        self.power = 10
        self.strength = 20

        
