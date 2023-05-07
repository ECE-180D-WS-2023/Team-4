import pygame

def blitRotate(surf, image, origin, pivot, angle):
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
    image_rect = image.get_rect(topleft = (origin[0] - pivot[0], origin[1] - pivot[1]))  # position the pivot point on origin
    pivot_to_center = image_rect.center - pygame.math.Vector2(origin)
    rotated_pivot_to_center = pivot_to_center.rotate(angle)  # note: pygame.Vector.rotate() is clockwise
    rotated_image_center = (origin[0] + rotated_pivot_to_center.x, origin[1] + rotated_pivot_to_center.y)
    rotated_image = pygame.transform.rotate(image, -angle)  # note: pygame.image.rotate() is counter-clockwise
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)
