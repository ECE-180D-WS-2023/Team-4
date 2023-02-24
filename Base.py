from GameObject import GameObject



class Base(GameObject):
    def __init__(self, shield=0, **profile):
        super().__init__(**profile)
        self.m_shield = shield
    
    # Base shield getter function
    @property
    def base_shield(self):
        """
        Getter for PROPERTY base_shield.

        INPUT:
        - NONE
        OUTPUT:
        - base shield value
        """
        print("Current base shield: ", self.m_shield)
        return self.m_shield

    # Team number setter function 
    @base_shield.setter
    def base_shield(self, new_base_shield):
        """
        Setter for PROPERTY team number

        INPUT:
        - new team number: new team number
        OUTPUT:
        - NONE
        """
        self.m_shield = new_base_shield



    
