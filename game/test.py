import pygame
# from GameObject import GameObject
from Veggie import Veggie
from Base import Base
from Player import Player
from constants import *

if __name__ == "__main__":
    """
    Object creation/properties convention
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

    Player:
        - parent properties
                - position (tuple)
                - velocity (tuple)
                - health (scalar)
                - team_num (scalar)
        - child properties
                - player_state (scalar)
                - player_role (scalar)
    """

    # Object creation
    # player1_dict = {(30, 0), (0, 0), team_num = 1, name = "Bruce", role =  PLAYER_ENGINEER, state = PLAYER_WALKING,  health = 10}
    veggie1 = Veggie((3, 4), (0, 1), damage = 3, team_num = 1, veggie_type = "pumpkin")
    base1 = Base((50, 0), (0, 0), health = 100, team_num = 1)
    #player1 = Player(pos_x = 30, pos_y = 0, vel_x = 0, vel_y = 0, health = 10, team_num = 1, name="Bruce" ,role = PLAYER_ENGINEER, state = PLAYER_WALKING)
    player1 = Player((30, 0), (0, 0), team_num = 1, name = "Bruce", role =  PLAYER_ENGINEER, state = PLAYER_WALKING,  health = 10)

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

    # Base child properties test
    gain_shield = 5
    base1.base_shield = base1.base_shield + gain_shield
    assert base1.base_shield == 5

    # Veggie child properties test
    assert veggie1.veggie_type == "pumpkin"
    veggie1.veggie_type = "carrot"
    assert veggie1.veggie_type == "carrot"

    # Player parent properties test
    assert player1.name == "Bruce"              # Initialize player name
    player1.name = "Hector"                     # Modify name
    assert player1.name == "Hector"             # Check name

    # Player child properties test
    player1.harvest("carrot")
    player1.display_backpack()
    curr_backpack = player1.display_backpack()  # current backpack information
    assert curr_backpack["carrot"] == 0         # the player cannot pick up carrot because the player is not in harvesting mode
    player1.player_state = PLAYER_HARVESTING    # switch player state
    player1.harvest("carrot")                   # pick up carrot successfully
    assert curr_backpack["carrot"] == 1
    assert curr_backpack["cabbage"] == 0
    player1.harvest("carrot")
    player1.harvest("carrot")
    player1.harvest("carrot")
    player1.harvest("cabbage")
    player1.harvest("carrot")
    assert curr_backpack["carrot"] == 5
    assert curr_backpack["cabbage"] == 1
    player1.harvest("carrot")
    assert curr_backpack["carrot"] == 5
    player1.display_backpack()

    # Player alive test
    assert player1.is_alive() == True
    print("meow", str(player1.health))
    damage = -11
    player1.health = player1.health + damage
    print("meow", str(player1.health))
    assert player1.is_alive() == False
    del player1
    
    print("Everything passed")
