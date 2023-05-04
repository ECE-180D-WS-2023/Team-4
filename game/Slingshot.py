from GameObject import GameObject
from constants import *

class Slingshot(GameObject):
    def __init__(self, pos, vel, team_num: int) -> None:
        super().__init__((SLINGSHOT_WIDTH, SLINGSHOT_HEIGHT), pos, vel, team_num, img='assets/slingshot_station.png', scale=2)

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
