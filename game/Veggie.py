from GameObject import GameObject
from constants import *

class Veggie(GameObject):
    def __init__(self, pos, vel, team_num: int, veggie_type: str, damage: int, ) -> None:
        super().__init__((VEGGIE_WIDTH, VEGGIE_HEIGHT), pos, vel, team_num, img='assets/veggies/veggies.png')
        self.m_type = veggie_type
        self.m_damage = damage
        self.m_harvest_time = veggie_dict[veggie_type] / 2

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
