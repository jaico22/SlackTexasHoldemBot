import numpy as np

class Hand:

    def __init__(self):
        self.card_nums = []
        self.card_suits = []
        self.rank = 0.0
        self.secondar_tb = 0.0
        self.high_card = 0.0

    def clear(self):
        '''
        Resets players hand back to original state
        '''
        self.card_nums = []
        self.card_suits = []
        self.rank = 0.0
        self.secondar_tb = 0.0
        self.high_card = 0

    def print_hand(self,n=-1):
        '''
        Returns a string representation of the players hands
        '''
        print_hand_out = ""
        if n == -1 :
            cards_to_print = range(len(self.card_nums))
        else :
            cards_to_print = range(0,n)
        for i in cards_to_print:
            print_hand_out += "["
            # Print Number
            if self.card_nums[i] <= 10 :
                print_hand_out += str(self.card_nums[i]) 
            elif self.card_nums[i] == 11 : 
                print_hand_out += ":jack_o_lantern:"
            elif self.card_nums[i] == 12 : 
                print_hand_out += ":princess:"
            elif self.card_nums[i] == 13 : 
                print_hand_out += ":prince:"
            else :
                print_hand_out += ":a:"
            print_hand_out += ""
            # Print Suit
            if self.card_suits[i] == 0 :
                print_hand_out += ":spades:"
            elif self.card_suits[i] == 1 :
                print_hand_out += ":diamonds:"
            elif self.card_suits[i] == 2 :
                print_hand_out += ":clubs:"
            elif self.card_suits[i] == 3 :
                print_hand_out += ":hearts:"
            print_hand_out += "] "
        return print_hand_out

    def add_card(self,num,suits):
        '''
        Adds a card to the players hand
        '''
        self.card_nums.append(num)
        self.card_suits.append(suits)


    def rank_hand(self):
        '''
         Determines a numberical value corresponding with the strenght of a hand; Lower is better!
        '''
        self.rank = 0.0
        # Sort card numbers for easier processing
        card_nums_copy = self.card_nums
        self.card_nums.sort()
        # Determine if flush
        flush = False
        for suit in range(4):
            flush = flush or (np.count_nonzero(np.array(self.card_suits)==suit)==5)
        # Detmine if srtaight
        if (self.card_nums[5] - self.card_nums[0] == 4 ):
            self.rank = 6.0 + 1 - self.card_nums[len(self.card_nums)-1]/15.0
            if self.card_nums[0] == 10 and flush:
                self.rank = 1.0
            elif flush :
                self.rank = 2.0 + 1 - self.card_nums[len(self.card_nums)-1]/15.0
        # How many of each number
        card_num_counts = []
        print(self.card_nums)
        for card_num in range(2,15):
            card_num_counts.append(np.count_nonzero(np.array(self.card_nums)==card_num))
        # Check if 4 of a kind
        max_count_num = np.argmax(card_num_counts)
        max_count = card_num_counts[max_count_num]
        if max_count >= 4 :
            self.rank = 3 + (max_count_num+2)/15.0
        # Check if 3 of a kind exists
        elif max_count == 3 : 
            # Check if full house
            if np.count_nonzero(np.array(card_num_counts)==2) >= 1 :
                self.rank = 4 + (1 - (max_count_num+2)/15.0)
            else :
                self.rank = 7 + (1 - (max_count_num+2)/15.0)      
        elif max_count == 2 :
            # Check if two pair
            if np.count_nonzero(np.array(card_num_counts)==2) >= 2 :
                self.secondar_tb = (max_count_num+2)/ 15.0
                # Create special case, secondary tie breaker
                for i in range(len(card_num_counts)) :
                    if card_num_counts[i] == 2 and i!=max_count_num :
                        self.rank = 8 + 1-(i+2)/15.0     
                    elif card_num_counts[i] == 1 :
                        self.rank = 8 + 1-(i+2)/15.0     
            else :
                self.rank = 9 + 1 - (max_count_num+2)/15.0
        else :
            self.rank = 10 + 1 - self.card_nums[len(self.card_nums)-1]/15.0
        self.high_card = self.card_nums[len(self.card_nums)-1]
        print('Hand Ranked: ' + str(self.rank) + ' TB: ' + str(self.secondar_tb) + ' HC: ' + str(self.high_card))