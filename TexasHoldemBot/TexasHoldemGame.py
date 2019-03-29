from deck import Deck
from hand import Hand
from users import Users

import sys

class TexasHoldemGame:

    def __init__(self) : 
        # Player related variables
        self.players = []
        self.players_active = [] 
        self.hands = []
        self.chips = []
        self.bets = []
        self.all_in = []
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

        # Databse related stuff
        self.users_db = Users()

    def determine_winner(self):
        '''
        Determines what hand has the highest strength and also breaks ties
        '''
        winning_player = -1 
        lowest_rank = 10
        best_tb = 0
        for i in range(len(self.players)) :
            # Rank Hands
            self.hands[i].rank_hand()
            # Determine if rank is lowest
            if self.hands[i].rank < lowest_rank and self.players_active[i]==True :
                lowest_rank = self.hands[i].rank
                winning_player = i
                best_tb = self.hands[i].secondar_tb
            elif self.hands[i].rank == lowest_rank and self.hands[i].secondar_tb > best_tb\
             and self.players_active[i]==True : 
                lowest_rank = self.hands[i].rank
                winning_player = i
                best_tb = self.hands[i].secondar_tb
        string_out = " wins the round and earns " + str(sum(self.bets)) + " chips :moneybag:"
        
        # Modify chip counts
        print(self.bets)
        pot = sum(self.bets)
        print('Pot = ' + str(pot))
        for i in range(len(self.players)) :
            print('player - ' + str(i) + ' bet - ' + str(self.bets[i]) + ' winner = ' + str(winning_player))
            if i == winning_player : 
                self.chips[i] += pot-self.bets[i]
            else :
                self.chips[i] -= self.bets[i]
        
        return self.players[winning_player], string_out

    def fold(self,user_id):
        ''' 
        Removes player from the round
        '''
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :
            self.players_active[player_idx] = False
            print(self.players_active)

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

    def fetch_chips(self,user_id):
        '''
        Retreives how many chips a player has
        '''
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :
            return self.chips[player_idx]
        else :
            return -1

    def go_all_in(self,user_id):
        '''
        Places all of the players chips in the pot
        '''
        player_idx = self.get_player_idx(user_id)
        self.bets[player_idx] = self.chips[player_idx]
        self.has_bet[player_idx] = True
        self.all_in[player_idx] = True

    def check(self,user_id):
        # Determine if user can check
        min_bet = 10000
        max_bet = 0 
        for i in range(len(self.bets)) :
            if self.players_active[i] == True and self.all_in[i]==False:
                if self.bets[i] < min_bet : 
                    min_bet = self.bets[i]
                if self.bets[i] > max_bet : 
                    max_bet = self.bets[i]
        if min_bet == max_bet :
            player_idx = self.get_player_idx(user_id)
            self.has_bet[player_idx] = True       
            return 1
        else :
            return 0

    def call(self,user_id):
        '''
        Modified bet to equal maximum bet
        '''
        new_bet = max(self.bets)
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :
            if self.chips[player_idx] >= new_bet : 
                self.bets[player_idx] = new_bet
                self.has_bet[player_idx] = True
                print(self.bets)
                return 1
            else : 
                self.bets[player_idx] = self.chips[player_idx]
                self.has_bet[player_idx] = True
                self.all_in[player_idx] = True
                return 2
        else :
            return 0

    def raise_bet(self,user_id,amnt):
        '''
        Raises current bet by amnt
        '''
        # Find user id in player list
        player_idx = self.get_player_idx(user_id)
        new_bet = max(self.bets) + amnt
        print('new_bet= ' + str(new_bet))
        if player_idx > -1 :
            print('cur_bet= ' + str(self.bets[player_idx]))
            if self.chips[player_idx] >= new_bet: 
                print(self.bets[player_idx] - new_bet)
                self.bets[player_idx] = new_bet
                self.has_bet[player_idx] = True
                return 1
            else : 
                self.bets[player_idx] = self.chips[player_idx]
                print('player is all in')
                self.all_in[player_idx] = True
                return 2
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
                
        return "Player is not in the game"

    def check_betting_complete(self):
        '''
        Checks if betting has been completed
        '''
        # Find minimum and maximum bet of all players that have no folded and are not all in
        min_bet = 999999999
        max_bet = 0
        print(self.bets)
        for i in range(len(self.bets)) :
            # Minimum is only players active
            if (self.players_active[i] == True and self.all_in[i]==False):
                if self.bets[i] < min_bet : 
                    min_bet = self.bets[i]
            # Maxmimum can be set by any active player or someone who is all in
            if (self.players_active[i] == True or self.all_in[i]==True):
                if self.bets[i] > max_bet : 
                    max_bet = self.bets[i]
        print('Max Bet = ' + str(max_bet) + "Min Bet = " + str(min_bet))
        if ((self.has_bet.count(True) == self.players_active.count(True))and\
        (max_bet == min_bet))or(self.players_active.count(True)==1):
            return 1
        else:
            return 0

    def start_game(self):
        '''
        Starts the game of poker!
        Deals two cards to each player and moves state machine to betting
        '''
        self.players_active = [True]*len(self.players)
        self.all_in = [False]*len(self.players)
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
    
    def end_game(self):
        # Cash out each player
        for player in self.players :
            # Determine player idx 
            player_idx = self.get_player_idx(player)
            self.users_db.cash_out(player,self.chips[player_idx])
        # Clear everything else


    def leave_game(self, user_id):
        '''
        Drop user from the game and cash them out
        '''
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :        
            self.users_db.cash_out(user_id,self.chips[player_idx])
            self.players.pop(player_idx)
            self.all_in.pop(player_idx)
            self.bets.pop(player_idx)
            self.players_active.pop(player_idx)
            self.has_bet.pop(player_idx)
            self.chips.pop(player_idx)
            self.hands.pop(player_idx)

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
                # Fetch how many chips the player has
                chips = self.users_db.check_in_and_add_user(user_id)
                # Update local variables
                self.players.append(user_id)
                self.players_active.append(True)
                self.hands.append(Hand())
                self.chips.append(chips)
                self.bets.append(0)
                self.all_in.append(False)
                self.has_bet.append(False)
                return 1
        else :
            return 1
