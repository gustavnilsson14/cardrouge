import random

class Deck:

    def __init__(self, cards = []):
        self.deck = cards
        print("A new deck was created!")

    def add_top(self, card):
        self.deck += card
        print("Added card to top ", self.deck)

    def add_bottom(self, card):
        self.deck.insert(0, card)

    def shuffle(self):
        random.shuffle(self.deck)

    def remove_card(self, index):
        self.deck.pop(index)

    def draw_card(self):
        return self.deck.pop()
