from users import Users
from hand import Hand
class Player : 
    def __init__(self,user_id,chips) : 
        self.active = True
        self.hand = Hand()
        self.user_id = user_id
        self.has_bet = False
        self.chips = chips
        self.all_in = False
        self.bet = 0

    def reset(self) : 
        self.active = True
        self.hand = Hand()
        self.has_bet = False
        self.all_in = False        
        self.bet = 0