import pygame
# from GameObject import GameObject
from Veggie import Veggie
from Base import Base
from Constants import *

if __name__ == "__main__":
    """
    Object creation convention
    Veggie:
        - parent properties
                - position (tuple)
                - velocity (tuple)
                - health (scalar)
                - team_num (scalar)
        - child properties
                - veggie_type (scalar)
    Base:
        - parent properties
                - position (tuple)
                - velocity (tuple)
                - health (scalar)
                - team_num (scalar)
    """

    # Object creation
    veggie1 = Veggie(pos_x = 3, pos_y = 4, vel_x = 0, vel_y = 1, health = 3, team_num = 1, veggie_type="pumpkin")
    base1 = Base(pos_x = 50, pos_y = 0, vel_x = 0, vel_y = 0, health = 100, team_num = 1)

    # Veggie parent properties test
    assert veggie1.position == (3, 4)
    new_pos = (7,9)
    veggie1.position = new_pos
    assert veggie1.position == (7, 9)

    # Base parent properties test
    assert base1.position == (50, 0)
    damage = -5
    base1.health = base1.health + damage
    assert base1.health == 95
    new_team_number = 2
    assert base1.team_num == 1
    base1.team_num = new_team_number
    assert base1.team_num == 2

    # Veggie child properties test
    assert veggie1.veggie_type == "pumpkin"
    veggie1.veggie_type = "carrot"
    assert veggie1.veggie_type == "carrot"
    
    print("Everything passed")
