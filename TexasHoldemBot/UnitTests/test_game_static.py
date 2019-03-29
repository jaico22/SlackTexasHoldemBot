import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TexasHoldemGame import TexasHoldemGame
from hand import Hand
# Init game

game = TexasHoldemGame()
p_1_uid = '999'
p_2_uid = '1239'
p_3_uid = 'asdas012d'

# Add some players
new_hand = Hand()
game.add_player(p_1_uid)
new_hand_2 = Hand()
game.add_player(p_2_uid)

# Start the game
game.start_game()

# Display Hands
print('Player 1 = ')
hand = game.print_hand(p_1_uid)
print(hand)
print('Player 2 = ')
hand = game.print_hand(p_2_uid)
print(hand)


# Check if chips are working
n_chips = game.fetch_chips(p_1_uid)
print("Player 1 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips(p_2_uid)
print("Player 2 has " + str(n_chips) + " chips")


# Some betting
print('betting')
game.raise_bet(p_1_uid,5)
print(game.check_betting_complete())

game.raise_bet(p_2_uid,800000)
print(game.check_betting_complete())

game.fold(p_1_uid)
print(game.check_betting_complete())

'''
# Add Community Card #1,2,3
print('Community cards added')
game.add_community_card()
game.add_community_card()
game.add_community_card()
comm_card = game.print_community_cards()
print(comm_card)
game.raise_bet(p_1_uid,5)
print(game.check_betting_complete())
game.raise_bet(p_2_uid,1)
print(game.check_betting_complete())
game.call(p_3_uid)
print(game.check_betting_complete())
game.call(p_1_uid)
print(game.check_betting_complete())
print('betting should be complete')

# 4
game.add_community_card()
comm_card = game.print_community_cards()
print(comm_card)
game.raise_bet(p_1_uid,5)
print(game.check_betting_complete())
game.raise_bet(p_2_uid,1)
print(game.check_betting_complete())
game.fold(p_3_uid)
print(game.check_betting_complete())
game.call(p_1_uid)
print(game.check_betting_complete())
print('betting should be complete')

# 5
game.add_community_card()
comm_card = game.print_community_cards()
print(comm_card)
game.raise_bet(p_1_uid,5)
print(game.check_betting_complete())
game.raise_bet(p_2_uid,1)
print(game.check_betting_complete())
print(game.check_betting_complete())
game.call(p_1_uid)
print(game.check_betting_complete())
print('betting should be complete')

print('Player 1 = ')
hand = game.print_hand(p_1_uid)
print(hand)

print('Player 2 = ')
hand = game.print_hand(p_2_uid)
print(hand)
print('Player 3 = ')
hand = game.print_hand(p_3_uid)
print(hand)


# Check if chips are working
n_chips = game.fetch_chips(p_1_uid)
print("Player 1 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips(p_2_uid)
print("Player 2 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips(p_3_uid)
print("Player 3 has " + str(n_chips) + " chips")

win_str = game.determine_winner()
print(win_str)

# Check if chips are working
n_chips = game.fetch_chips(p_1_uid)
print("Player 1 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips(p_2_uid)
print("Player 2 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips(p_3_uid)
print("Player 3 has " + str(n_chips) + " chips")

game.leave_game(p_1_uid)
game.leave_game(p_2_uid)
game.leave_game(p_3_uid)
'''