import random

class Deck : 
    def __init__(self) :
        # Initialize cards list
        self.cards = []
        # Build deck using "shuffle cards" method
        self.shuffleCards()

    def shuffleCards(self):
        # Loop through every possible card (assuming 52 cards)
        # Append a tuple containing (Card number, Suite)
        for i in range(52) : 
            self.cards.append((i//4+2,i%4))
        # Shuffle cards
        random.shuffle(self.cards)
        

    def draw(self):
        # Remove card from top of the deck
        card = self.cards.pop()
        # Parse out data from the tuple
        number = card[0]
        suit = card[1]
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