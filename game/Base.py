from GameObject import GameObject
from constants import *

class Base(GameObject):
    def __init__(self, pos, vel, team_num, health=100, shield=0):
        super().__init__((BASE_WIDTH, BASE_HEIGHT), pos, vel, team_num, img="assets/base.png", frame_size=(93, 100))
        self.m_shield = shield
        self.m_health = health
        self.m_immune_time = 0
    
    @property
    def base_shield(self) -> int:
        print("Current base shield: ", self.m_shield)
        return self.m_shield

    @base_shield.setter
    def base_shield(self, new_base_shield: int) -> None:
        self.m_shield = new_base_shield

    @property
    def immune_time(self) -> int:
        print("Current base shield: ", self.m_immune_time)
        return self.m_immune_time

    @immune_time.setter
    def immune_time(self, new_time: int) -> None:
        self.m_shield = new_time

    @property
    def health(self) -> int:
        print("Current base shield: ", self.m_health)
        return self.m_health

    @health.setter
    def health(self, new_health: int) -> None:
        self.m_health = new_health
