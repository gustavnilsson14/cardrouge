from entity import Item

class Card(Item):

    def __init__(self,y):
        Item.__init__(self,y)

class Currency(Item):
    pass
