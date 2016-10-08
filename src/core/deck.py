import random

class Card_list:

    def __init__(self, cards = []):
        self.list = cards

    def add(self, card):
        self.list += card

    def shuffle(self):
        random.shuffle(self.list)

    def remove(self, index):
        self.list.pop(index)

    def discard(self):
        self.list = []

class Deck(Card_list):

    def __init__(self, cards = []):
        Card_list.__init__(self, cards)

    def draw_card(self):
        return self.list.pop()

class Hand(Card_list):

    def __init__(self, cards = []):
        Card_list.__init__(self, cards)

    def play_card(self, index):
        self.list.pop(index)

class Discard_pile(Card_list):
    def __init__(self, cards = []):
        Card_list.__init__(self, cards)
