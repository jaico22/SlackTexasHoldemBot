import random

class Deck : 
    def __init__(self) :
        self.card_numbers = [i / 4 + 2 for i in range(0,52)]
        self.card_suits   = [i % 4 for i in range(52)]

    def shuffleCards(self):
        self.card_numbers = [i / 4 + 2 for i in range(0,52)]
        self.card_suits = [i % 4 for i in range(52)]
        random.shuffle(self.card_numbers)
        random.shuffle(self.card_suits)

    def draw(self):
        number = self.card_numbers.pop()
        suit = self.card_suits.pop()
        return number, suit

    def printCard(self,number,suit):
        response = ""
        if number > 1 and number <= 10 :
            response += str(number) + " of "
        elif number == 11 :
            response += "Jack of "
        elif number == 12 :
            response += "Queen of "
        elif number == 13 :
            response += "King of "
        elif number == 14 :
            response += "Ace of "
        if suit == 0 :
            response += "Spades"
        elif suit == 1 :
            response += "Clubs"
        elif suit == 2 :
            response += "Diamonds"
        elif suit == 3 :
            response += "Hearts"
        return response