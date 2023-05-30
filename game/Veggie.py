from GameObject import GameObject
from constants import *
import pygame

class Veggie(GameObject):
    def __init__(self, pos, vel, team_num: int, img) -> None:
        super().__init__((VEGGIE_WIDTH, VEGGIE_HEIGHT), pos, vel, team_num, img, animation_steps = [4], scale=3)
        
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

# class Carrot(Veggie):
#     def __init__(self, pos, vel, team_num: int) -> None:
#         super().__init__(pos, vel, team_num, img='assets/veggies/carrot_16pi1.png')
#         self.damage = CARROT_DAMAGE

# class Mushroom(Veggie):
#     def __init__(self, pos, vel, team_num: int) -> None:
#         super().__init__(pos, vel, team_num, img='assets/veggies/mushroom.png')
#         self.damage = CARROT_DAMAGE

# class Cabbage(Veggie):
#     def __init__(self, pos, vel, team_num: int) -> None:
#         super().__init__(pos, vel, team_num, img='assets/veggies/cabbage.png')
#         self.damage = CARROT_DAMAGE

# class Potato(Veggie):
#     def __init__(self, pos, vel, team_num: int) -> None:
#         super().__init__(pos, vel, team_num, img='assets/veggies/potato.png')
        self.damage = CARROT_DAMAGE

# class YellowBellPepper(Veggie):
#     def __init__(self, pos, vel, team_num: int) -> None:
#         super().__init__(pos, vel, team_num, img='assets/veggies/yellow-bell-pepper.png')
#         self.damage = CARROT_DAMAGE

class TestPumpkin(Veggie):
    def __init__(self, pos, vel, team_num: int) -> None:
        super().__init__(pos, vel, team_num, img='assets/veggies/pumpkin-animation.png')
        self.damage = CARROT_DAMAGE

    def update(self, screen, action=0):
        self.pos_x -= self.vel_x
        self.pos_y -= self.vel_y
        self.rect.center = (self.pos_x, self.pos_y)
        # self.frame_col = (self.frame_col + 1) % 4
        self.draw(screen, action)

        if (self.rect.left < 0 
            or self.rect.right > SCREEN_WIDTH 
            or self.rect.top <= 0
            or self.rect.bottom >= SCREEN_HEIGHT):
            self.kill()

class TestPotato(Veggie):
    def __init__(self, pos, vel, team_num: int) -> None:
        super().__init__(pos, vel, team_num, img='assets/veggies/potato-sheet.png')
        self.damage = CARROT_DAMAGE

    def update(self, screen, action=0):
        self.pos_x -= self.vel_x
        self.pos_y -= self.vel_y
        self.rect.center = (self.pos_x, self.pos_y)
        # self.frame_col = (self.frame_col + 1) % 4
        self.draw(screen, action)

        if (self.rect.left < 0 
            or self.rect.right > SCREEN_WIDTH 
            or self.rect.top <= 0
            or self.rect.bottom >= SCREEN_HEIGHT):
            self.kill()

class TestCarrot(Veggie):
    def __init__(self, pos, vel, team_num: int) -> None:
        super().__init__(pos, vel, team_num, img='assets/veggies/carrot-sheet.png')
        self.damage = CARROT_DAMAGE

    def update(self, screen, action=0):
        self.pos_x -= self.vel_x
        self.pos_y -= self.vel_y
        self.rect.center = (self.pos_x, self.pos_y)
        # self.frame_col = (self.frame_col + 1) % 4
        self.draw(screen, action)

        if (self.rect.left < 0 
            or self.rect.right > SCREEN_WIDTH 
            or self.rect.top <= 0
            or self.rect.bottom >= SCREEN_HEIGHT):
            self.kill()

class TestStrawberry(Veggie):
    def __init__(self, pos, vel, team_num: int) -> None:
        super().__init__(pos, vel, team_num, img='assets/veggies/strawberry-sheet.png')
        self.damage = CARROT_DAMAGE

    def update(self, screen, action=0):
        self.pos_x -= self.vel_x
        self.pos_y -= self.vel_y
        self.rect.center = (self.pos_x, self.pos_y)
        # self.frame_col = (self.frame_col + 1) % 4
        self.draw(screen, action)

        if (self.rect.left < 0 
            or self.rect.right > SCREEN_WIDTH 
            or self.rect.top <= 0
            or self.rect.bottom >= SCREEN_HEIGHT):
            self.kill()

class TestPeach(Veggie):
    def __init__(self, pos, vel, team_num: int) -> None:
        super().__init__(pos, vel, team_num, img='assets/veggies/peach-sheet.png')
        self.damage = CARROT_DAMAGE

    def update(self, screen, action=0):
        self.pos_x -= self.vel_x
        self.pos_y -= self.vel_y
        self.rect.center = (self.pos_x, self.pos_y)
        # self.frame_col = (self.frame_col + 1) % 4
        self.draw(screen, action)

        if (self.rect.left < 0 
            or self.rect.right > SCREEN_WIDTH 
            or self.rect.top <= 0
            or self.rect.bottom >= SCREEN_HEIGHT):
            self.kill()