from GameObject import GameObject
from constants import *
import pygame

class Veggie(GameObject):
    def __init__(self, pos, vel, team_num: int, veggie_type: str, damage: int, ) -> None:
        super().__init__((VEGGIE_WIDTH, VEGGIE_HEIGHT), pos, vel, team_num, img='assets/veggies/veggies.png')
        self.type = veggie_type
        self.damage = damage
        self.harvest_time = veggie_dict[veggie_type] / 2
        
    def update(self, screen, action=None):
        self.pos_x -= self.vel_x
        self.pos_y -= self.vel_y
        self.rect.center = (self.pos_x, self.pos_y)
        self.draw(screen, action)

        if (self.rect.left < 0 
            or self.rect.right > SCREEN_WIDTH 
            or self.rect.top <= 0
            or self.rect.bottom >= SCREEN_HEIGHT):
            self.kill()
            print("this object is killed")

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
