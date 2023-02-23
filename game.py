import pygame
from GameObject import GameObject
from Veggie import Veggie
from Constants import *

if __name__ == "__main__":

    game_object = Veggie(pos_x = 3, pos_y = 4, vel_x = 0, vel_y = 1, health = 3, team_num = 1, veggie_type="pumpkin")
    game_object.get_pos()
    print("Everything passed")
