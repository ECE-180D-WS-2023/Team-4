from GameObject import GameObject
from constants import *

class Base(GameObject):
    def __init__(self, pos, vel, team_num, health=100, shield=0):
        super().__init__((BASE_WIDTH, BASE_HEIGHT), pos, vel, team_num, img="assets/base.png")
        self.shield = shield
        self.health = health
        self.immune_time = 0
