from GameObject import GameObject
from constants import *

class Slingshot(GameObject):
    def __init__(self, pos, vel, team_num: int) -> None:
        super().__init__((SLINGSHOT_WIDTH, SLINGSHOT_HEIGHT), pos, vel, team_num, img='assets/trolly.png', scale=1.5)
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




    # # TODO: remove this test
    # def whoami(self):
    #     print("I am ", self.m_type, " and I have ", self.m_damage)
    #
    # @property
    # def veggie_type(self) -> str:
    #     print("Current veggie type: ", self.m_type)
    #     return self.m_type
    #
    # @veggie_type.setter
    # def veggie_type(self, new_veggie_type: str) -> None:
    #     self.m_type = new_veggie_type
    #
    # @property
    # def damage(self) -> int:
    #     print("Current veggie type: ", self.m_damage)
    #     return self.m_damage
    #
    # @damage.setter
    # def damage(self, new_damage: int) -> None:
    #     self.damage = new_damage
