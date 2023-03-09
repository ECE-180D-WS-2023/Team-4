from GameObject import GameObject
from constants import *
import pygame

class Veggie(GameObject):
    def __init__(self, pos, vel, team_num: int, veggie_type: str, damage: int, ) -> None:
        super().__init__((VEGGIE_WIDTH, VEGGIE_HEIGHT), pos, vel, team_num, img='assets/veggies/veggies.png')
        self.m_type = veggie_type
        self.m_damage = damage
        self.m_harvest_time = veggie_dict[veggie_type] / 2
        
    def update(self, screen, action=None):
        self.m_pos_x -= self.m_vel_x
        self.m_pos_y -= self.m_vel_y
        self.rect.center = (self.m_pos_x, self.m_pos_y)
        self.draw(screen, action)

        if (self.rect.left < 0 
            or self.rect.right > SCREEN_WIDTH 
            or self.rect.top <= 0
            or self.rect.bottom >= SCREEN_HEIGHT):
            self.kill()
            print("this object is killed")

    # TODO: remove this test
    def whoami(self):
        print("I am ", self.m_type, " and I have ", self.m_damage)

    @property
    def veggie_type(self) -> str:
        print("Current veggie type: ", self.m_type)
        return self.m_type

    @veggie_type.setter
    def veggie_type(self, new_veggie_type: str) -> None:
        self.m_type = new_veggie_type

    @property
    def damage(self) -> int:
        print("Current veggie type: ", self.m_damage)
        return self.m_damage

    @damage.setter
    def damage(self, new_damage: int) -> None:
        self.damage = new_damage

class Carrot(Veggie):
    # def __init__(self, pos, vel, team_num: int, veggie_type: str, damage: int) -> None:
    #     super().__init__(pos, vel, team_num, veggie_type, damage)
    ...

class Mushroom(Veggie):
    def __init__(self):
        pass

class Cabbage(Veggie):
    def __init__(self):
        pass

class Potato(Veggie):
    def __init__(self):
        pass
