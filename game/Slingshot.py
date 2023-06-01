from GameObject import GameObject
from constants import *

class Slingshot(GameObject):
    def __init__(self, pos, vel, team_num: int) -> None:
        super().__init__((TROLLY_WIDTH, TROLLY_HEIGHT), pos, vel, team_num, img='assets/trolly.png', scale=1.5)
        self.mounted = False

    def update(self, screen, action=None):
        if self.mounted:
            if self.team_num == 0:
                if self.vel_x == 0:
                    self.rect.center = (self.pos_x, self.pos_y)
                elif self.vel_x > 0:
                    if self.pos_x <= 1820:
                        self.pos_x += self.vel_x
                        self.rect.center = (self.pos_x, self.pos_y)
                    else:
                        self.vel_x = -self.vel_x
                elif self.vel_x < 0:
                    if self.pos_x >= 1370:
                        self.pos_x += self.vel_x
                        self.rect.center = (self.pos_x, self.pos_y)
                    else:
                        self.vel_x = -self.vel_x
            elif self.team_num == 1:
                if self.vel_x == 0:
                    self.rect.center = (self.pos_x, self.pos_y)
                elif self.vel_x > 0:
                    if self.pos_x <= 1180:
                        self.pos_x += self.vel_x
                        self.rect.center = (self.pos_x, self.pos_y)
                    else:
                        self.vel_x = -self.vel_x
                elif self.vel_x < 0:
                    if self.pos_x >= 750:
                        self.pos_x += self.vel_x
                        self.rect.center = (self.pos_x, self.pos_y)
                    else:
                        self.vel_x = -self.vel_x
        
        self.draw(screen, action)
        self.mask = pygame.mask.from_surface(self.animation_list[self.frame_row][self.frame_col])


