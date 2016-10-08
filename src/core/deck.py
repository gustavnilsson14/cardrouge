import random

class CardList:

    def __init__(self, cards = []):
        self.list = cards

    def add(self, card):
        if card == 0:
            return 0
        self.list += [card]

    def shuffle(self):
        random.shuffle(self.list)

    def remove(self, index):
        if len(self.list) == 0:
            return 0;
        self.list.pop(index)

    def discard(self):
        self.list = []

class Deck(CardList):

    def __init__(self, cards = []):
        CardList.__init__(self, cards)

    def draw_card(self):
        if len(self.list) == 0:
            return 0;
        return self.list.pop()

class Hand(CardList):

    def __init__(self, cards = [], max_size = 5):
        CardList.__init__(self, cards)
        self.max_size = max_size

    def play_card(self, index):
        if len(self.list) == 0:
            return 0;
        return self.list.pop(index)


class Discard_pile(CardList):
    def __init__(self, cards = []):
        CardList.__init__(self, cards)
