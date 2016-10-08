from entity import Item

class Card(Item):

    def __init__(self,y):
        Item.__init__(self,y)


class Combat_card(Card):

    def __init__(self,y):
        Card.__init__(self,y)

class Magic_card(Card):
    def __init__(self,y):
        Card.__init__(self,y)

class Currency(Item):
    pass
