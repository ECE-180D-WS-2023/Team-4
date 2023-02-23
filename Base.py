from GameObject import GameObject



class Base(GameObject):
    def __init__(self, **profile):
        super().__init__(**profile)

    def take_damage(self, damage):
        """
        Base health will be deducted if taken damage
        
        INPUT:
        - damage: health of incoming veggie
        OUTPUT:
        - NONE
        """
        self.m_health = self.m_health - damage
