import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TexasHoldemGame import TexasHoldemGame
from hand import Hand

# Init game
game = TexasHoldemGame()
game_state = 0

while True :
    ## Init, wait for players
    if game_state == 0 :
        usr_input = input('Type in Player Name or "start: "')
        if usr_input == 'start' :
            game.start_game()
            for current_player_string in game.players : 
                hand_string = game.print_hand(current_player_string)
                print(hand_string)
            game_state = 1
        else : 
            game.add_player(usr_input)
    ## State 1 : Set Blinds
    if game_state == 1 :
        game_state = 2 
        cur_player = 0
        print('Betting has commenced')
        print('Example Commands:')
        print('   raise N : raises bet by N coinds')
        print('   all in : go all in!')
        print('   check')
        print('   fold ')
    ## State 2 : Betting 
    if game_state == 2 :
        current_player_string = str(game.players[cur_player])
        if game.players[cur_player].active and not game.players[cur_player].all_in: 

            print(current_player_string + " please place bets/call/fold")
            usr_input = input()
            print(usr_input[:3])
            valid_command = False
            if usr_input[:5] == 'raise': 
                print('raising')
                valid_command = True
                game.raise_bet(game.players[cur_player],int(usr_input[6:]))
            elif usr_input[:6] == 'all in' :
                print('all in')
                valid_command = True
                game.go_all_in(game.players[cur_player])
            elif usr_input[:4] == 'fold':
                game.fold(game.players[cur_player])
                valid_command = True
            elif usr_input[:4] == 'call' :
                print('calling')
                valid_command = True
                res = game.call(game.players[cur_player])
                if res==0 :
                    print('Error: invalid player')
            elif usr_input[:5] == 'check' :
                valid_command = False
                res = game.check(game.players[cur_player])
                if res == 1 :
                    valid_command = True
                else :
                    print('You must bet or fold')
        # Increment player counter
        if valid_command : 
            cur_player = ((cur_player+1) % len(game.players))
        print(cur_player)
        if game.check_betting_complete() :
            print('Betting completed')
            game_state = 3
            # if everyone folds, go to state 4
            if game.count_n_active_players() == 1 :
                game_state = 4
    if game_state == 3 :
        if len(game.community_cards.card_nums) < 5 :
            game.add_community_card()
            while len(game.community_cards.card_nums) < 3 :
                game.add_community_card()
            comm_string = game.print_community_cards()
            print("Community" + comm_string)
            game_state = 2
        else :
            game_state = 4
    if game_state == 4 :
        win_str = game.determine_winner()
        print(win_str)
        # Check if chips are working
        for player in game.players : 
            n_chips = game.fetch_chips(player)
            print(player + " has " + str(n_chips) + " chips")

        game_state = 5
        
