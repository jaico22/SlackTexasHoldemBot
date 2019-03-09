from deck import Deck
from hand import Hand
import sys

class TexasHoldemGame:

    def __init__(self) : 
        # Player related variables
        self.players = []
        self.players_active = [] 
        self.hands = []
        self.bets = []
        self.has_bet = [] 
        self.big_blind_player = 0
        self.small_blind_player = 1
        self.big_blind = 15
        self.small_blind = 5

        # Game State Related Variables
        self.game_state = 0
        self.GS_INIT = 0
        self.GS_BETTING = 1

        # Deck related variables
        self.deck = Deck()
        self.community_cards = Hand()

    def determine_winner(self):
        '''
        Determines what hand has the highest strength and also breaks ties
        '''
        winning_player = '' 
        lowest_rank = 10
        best_tb = 0
        for i in range(len(self.players)) :
            if self.hands[i].rank < lowest_rank and self.players_active[i]==True :
                lowest_rank = self.hands[i].rank
                winning_player = self.players[i]
                best_tb = self.hands[i].secondar_tb
            elif self.hands[i].rank == lowest_rank and self.hands[i].secondar_tb > best_tb\
             and self.players_active[i]==True : 
                lowest_rank = self.hands[i].rank
                winning_player = self.players[i]
                best_tb = self.hands[i].secondar_tb
        string_out = str(winning_player) + " wins the round and earns " + str(sum(self.bets))
        return string_out

    def fold(self,user_id):
        ''' 
        Removes player from the round
        '''
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :
            self.players_active[player_idx] = False

    def print_community_cards(self):
        '''
        Returns string displaying the community hand
        '''
        return self.community_cards.print_hand()

    def add_community_card(self):
        ''' 
        Adds Card to Community Hand
        '''
        # Reset "has bet"
        self.has_bet = [False] * len(self.players)
        if len(self.community_cards.card_nums) < 5 :
            num, suit = self.deck.draw()
            # Add to community pile
            self.community_cards.add_card(num,suit)
            # Add to each hand
            for i in range(len(self.players)):
                self.hands[i].add_card(num,suit)
        else : 
            self.determine_winner()
        
    def get_player_idx(self,user_id):
        '''
        Returns index in players list where user is found
        '''
        for i in range(len(self.players)):
            if self.players[i] == user_id :
                return i
        return -1

    def call(self,user_id):
        '''
        Modified bet to equal maximum bet
        '''
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :
            self.bets[player_idx] = max(self.bets)
            self.has_bet[player_idx] = True
            print(self.bets)
            return 1
        else :
            return 0

    def raise_bet(self,user_id,amnt):
        '''
        Raises current bet by amnt
        '''
        # Find user id in player list
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :
            self.bets[player_idx] = max(self.bets) + amnt
            self.has_bet[player_idx] = True
            print(self.bets)
            return 1
        else:
            return 0
            

    def print_hand(self,user_id):
        ''' 
        Returns a string containing description of hand
        '''
        # Find user id in player list
        for i in range(len(self.players)) :
            if self.players[i] == user_id : 
                hand = self.hands[i].print_hand()
                return hand
                break
        return "Player is not in the game"

    def check_betting_complete(self):
        '''
        Checks if betting has been completed
        '''
        # Find minimum and maximum bet
        min_bet = sys.maxint
        max_bet = 0
        for i in range(len(self.bets)) :
            if self.players_active[i] == True :
                if self.bets[i] < min_bet : 
                    min_bet = self.bets[i]
                if self.bets[i] > max_bet : 
                    max_bet = self.bets[i]

        if (self.has_bet.count(True) == self.players_active.count(True))and\
        (max_bet == min_bet):
            return 1
        else:
            return 0

    def start_game(self):
        '''
        Starts the game of poker!
        Deals two cards to each player and moves state machine to betting
        '''
        self.players_active = [True]*len(self.players)
        if self.game_state==self.GS_INIT : 
            self.deck.shuffleCards()
            for hand in self.hands : 
                # First card
                num, suit = self.deck.draw()
                hand.add_card(num,suit)
                # Second card
                num, suit = self.deck.draw()
                hand.add_card(num,suit)
                # Move State Machine
            self.game_state = self.GS_BETTING
            return 1
        else :
            return 0
        

    def add_player(self, user_id):
        '''
        Adds a player to the game
        Outputs 1 - Success
                2 - User already in game
                0 - Game already started
        '''
        if self.game_state==self.GS_INIT : 
            user_not_playing = True
            for player in self.players:
                if player == user_id :
                    user_not_playing = False
                    return 2
                    break
            if user_not_playing == True :
                self.players.append(user_id)
                self.players_active.append(True)
                self.hands.append(Hand())
                self.bets.append(0)
                self.has_bet.append(False)
                return 1
        else :
            return 1
