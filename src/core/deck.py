import random

class CardList:

    def __init__(self, cards):
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

    def in_list(self,card):
        if card in self.list:
            return 1
        return 0

class Deck(CardList):

    def __init__(self, cards):
        CardList.__init__(self, cards)

    def draw_card(self):
        if len(self.list) == 0:
            return 0
        return self.list.pop()

class Hand(CardList):

    def __init__(self, cards, max_size = 10):
        CardList.__init__(self, cards)
        self.max_size = max_size

    def play_card(self, card):
        if card not in self.list:
            return 0
        self.list.remove(card)
        return 1

    def is_full(self):
        if len(self.list) < self.max_size:
            return 0
        return 1

class Discard_pile(CardList):
    def __init__(self, cards):
        CardList.__init__(self, cards)
