from deck import Deck
from hand import Hand
from users import Users
from player import Player

import sys

class TexasHoldemGame:

    def __init__(self) : 
        # Player related variables
        self.players = []
        self.num_active_players = 0

        # Blind Related Values
        self.big_blind_player = 0
        self.small_blind_player = 1
        self.big_blind = 15
        self.small_blind = 5
        self.max_bet = 0

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
        sum_bets = 0 
        for player in self.players : 
            # Increment bet sum
            sum_bets += player.bet
            # Rank Hands
            player.hand.rank_hand()
            # Determine if rank is lowest
            if player.hand.rank < lowest_rank and player.active :
                lowest_rank = player.hand.rank
                winning_player = player
                best_tb = player.hand.secondar_tb
            elif player.hand.rank == lowest_rank and player.hand.secondar_tb > best_tb\
             and player.active : 
                lowest_rank = player.hand.rank
                winning_player = player
                best_tb = player.hand.secondar_tb
        string_out = " wins the round and earns " + str(sum_bets) + " chips :moneybag:"
        
        # Modify chip counts
        pot = sum_bets
        for player in self.players : 
            if player == winning_player : 
                player.chips += pot-player.bet
            else :
                player.chips -= player.bet
        
        return winning_player.user_id, string_out

    def fold(self,user_id):
        ''' 
        Removes player from the round
        '''
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :
            self.players[player_idx].active = False

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
        for player in self.players : 
            player.has_bet = False
        
        if len(self.community_cards.card_nums) < 5 :
            num, suit = self.deck.draw()
            # Add to community pile
            self.community_cards.add_card(num,suit)
            # Add to each hand
            for player in self.players : 
                player.hand.add_card(num,suit)
        else : 
            self.determine_winner()
        
    def get_player_idx(self,user_id):
        '''
        Returns index in players list where user is found
        '''
        for i in range(len(self.players)):
            if self.players[i].user_id == user_id :
                return i
        return -1

    def fetch_chips(self,user_id):
        '''
        Retreives how many chips a player has
        '''
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :
            return self.players[player_idx].chips
        else :
            return -1

    def go_all_in(self,user_id):
        '''
        Places all of the players chips in the pot
        '''
        player_idx = self.get_player_idx(user_id)
        self.players[player_idx].bet = self.players[player_idx].chips
        self.players[player_idx].has_bet = True
        self.players[player_idx].all_in= True

    def check(self,user_id):
        # Determine if user can check
        min_bet = 10000
        max_bet = 0 
        # Check if checking is a valid move
        for player in self.players : 
            if player.active and not player.all_in : 
                if player.bet < min_bet : 
                    min_bet = player.bet 
                if player.bet > max_bet : 
                    max_bet = player.bet
        # If it is, mark player as 'has bet' and move on
        if min_bet == max_bet : 
            player_idx = self.get_player_idx(user_id)
            self.players[player_idx].has_bet = True
            return 1
        else : 
            return 0 

    def call(self,user_id):
        '''
        Modified bet to equal maximum bet
        '''
        new_bet = self.max_bet 
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :
            player = self.players[player_idx]
            if player.chips >= new_bet : 
                player.bet = new_bet
                player.has_bet = True
                return 1
            else : 
                player.bets = player.chips
                player.has_bet = True
                player.all_in = True
                return 2
        else :
            return 0

    def raise_bet(self,user_id,amnt):
        '''
        Raises current bet by amnt
        '''
        # Find user id in player list
        player_idx = self.get_player_idx(user_id)
        new_bet = self.max_bet + amnt
        if player_idx > -1 :
            player = self.players[player_idx]
            # Increase max bet when player is valid
            self.max_bet += amnt
            if player.chips >= new_bet: 
                player.bet += amnt
                player.has_bet = True
                return 1
            else : 
                # Go all in if the bet is larger than their chip count
                self.go_all_in(user_id)
                return 2
        else:
            return 0
            

    def print_hand(self,user_id):
        ''' 
        Returns a string containing description of hand
        '''
        # Find user id in player list
        for player in self.players : 
            if player.user_id == user_id : 
                hand_string = player.hand.print_hand()
                return hand_string
                
        return "Player is not in the game"

    def check_betting_complete(self):
        '''
        Checks if betting has been completed
        '''
        # Find minimum and maximum bet of all players that have no folded and are not all in
        min_bet = 999999999
        max_bet = 0
        has_bet_count = 0
        active_count = 0
        for player in self.players :
            # Minimum is only players active
            if player.active and not player.all_in : 
                if player.bet < min_bet : 
                    min_bet = player.bet
            # Maxmimum can be set by any active player or someone who is all in
            if player.active or player.all_in :
                if player.bet > max_bet : 
                    max_bet = player.bet
            # Check count of players who have bet
            if player.has_bet : 
                has_bet_count += 1
            # Count number of active players
            if player.active : 
                active_count += 1
        print('Max Bet = ' + str(max_bet) + "Min Bet = " + str(min_bet))
        if ((active_count == has_bet_count) and (max_bet == min_bet))or(active_count == 1):
            return 1
        else:
            return 0

    def start_game(self):
        '''
        Starts the game of poker!
        Deals two cards to each player and moves state machine to betting
        '''
        # Reset player values
        for player in self.players : 
            player.reset()
        # Reset max bet
        self.max_bet = 0
        if self.game_state==self.GS_INIT : 
            self.deck.shuffleCards()
            for player in self.players : 
                # First card
                num, suit = self.deck.draw()
                player.hand.add_card(num,suit)
                # Second card
                num, suit = self.deck.draw()
                player.hand.add_card(num,suit)
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
            self.users_db.cash_out(player,self.players[player_idx].chips)
        # Clear everything else


    def leave_game(self, user_id):
        '''
        Drop user from the game and cash them out
        '''
        player_idx = self.get_player_idx(user_id)
        if player_idx > -1 :        
            self.users_db.cash_out(user_id,self.players[player_idx].chips)
            self.players.pop(player_idx)

    def count_n_active_players(self) : 
        cnt = 0 
        for player in self.players : 
            if player.active : 
                cnt += 1
        return cnt

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
                if player.user_id == user_id :
                    user_not_playing = False
                    return 2
                    
            if user_not_playing == True :
                # Fetch how many chips the player has
                chips = self.users_db.check_in_and_add_user(user_id)
                self.players.append(Player(user_id,chips))
                # Incrememnt number of active player
                
                return 1
        else :
            return 1
