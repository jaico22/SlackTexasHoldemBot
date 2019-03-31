import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TexasHoldemGame import TexasHoldemGame
from hand import Hand
# Init game

game = TexasHoldemGame()

# Add some players
new_hand = Hand()
game.add_player('1')
new_hand_2 = Hand()
game.add_player('2')
new_hand_3 = Hand()
game.add_player('3')

# Start the game
game.start_game()

# Display Hands
print('Player 1 = ')
hand = game.print_hand('1')
print(hand)
print('Player 2 = ')
hand = game.print_hand('2')
print(hand)
print('Player 3 = ')
hand = game.print_hand('3')
print(hand)

# Check if chips are working
n_chips = game.fetch_chips('1')
print("Player 1 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips('2')
print("Player 2 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips('3')
print("Player 3 has " + str(n_chips) + " chips")

# Some betting
print('betting')
game.raise_bet('1',5)
print(game.check_betting_complete())
game.raise_bet('2',1)
print(game.check_betting_complete())
game.call('3')
print(game.check_betting_complete())
game.call('1')
print(game.check_betting_complete())
print('betting should be complete')


# Add Community Card #1,2,3
print('Community cards added')
game.add_community_card()
game.add_community_card()
game.add_community_card()
comm_card = game.print_community_cards()
print(comm_card)
game.raise_bet('1',5)
print(game.check_betting_complete())
game.raise_bet('2',1)
print(game.check_betting_complete())
game.call('3')
print(game.check_betting_complete())
game.call('1')
print(game.check_betting_complete())
print('betting should be complete')

# 4
game.add_community_card()
comm_card = game.print_community_cards()
print(comm_card)
game.raise_bet('1',5)
print(game.check_betting_complete())
game.raise_bet('2',1)
print(game.check_betting_complete())
game.fold('3')
print(game.check_betting_complete())
game.call('1')
print(game.check_betting_complete())
print('betting should be complete')

# 5
game.add_community_card()
comm_card = game.print_community_cards()
print(comm_card)
game.raise_bet('1',5)
print(game.check_betting_complete())
game.raise_bet('2',1)
print(game.check_betting_complete())
print(game.check_betting_complete())
game.call('1')
print(game.check_betting_complete())
print('betting should be complete')

print('Player 1 = ')
hand = game.print_hand('1')
print(hand)

print('Player 2 = ')
hand = game.print_hand('2')
print(hand)
print('Player 3 = ')
hand = game.print_hand('3')
print(hand)


# Check if chips are working
n_chips = game.fetch_chips('1')
print("Player 1 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips('2')
print("Player 2 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips('3')
print("Player 3 has " + str(n_chips) + " chips")

win_str = game.determine_winner()
print(win_str)

# Check if chips are working
n_chips = game.fetch_chips('1')
print("Player 1 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips('2')
print("Player 2 has " + str(n_chips) + " chips")
n_chips = game.fetch_chips('3')
print("Player 3 has " + str(n_chips) + " chips")

game.leave_game('1')
game.leave_game('2')
game.leave_game('3')
