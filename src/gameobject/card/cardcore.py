from item import Card

class SelfCard(Card):
    def __init__(self,y):
        Card.__init__(self,y)

class TargetCard(Card):
    def __init__(self,y):
        Card.__init__(self,y)

class EntityCard(Card):
    def __init__(self,y):
        Card.__init__(self,y)

class DirectionCard(Card):
    def __init__(self,y):
        Card.__init__(self,y)

class MultipleTargetCard(Card):
    def __init__(self,y):
        Card.__init__(self,y)

class MultipleEntityCard(Card):
    def __init__(self,y):
        Card.__init__(self,y)

class MultipleDirectionCard(Card):
    def __init__(self,y):
        Card.__init__(self,y)

class BounceCard(Card):
    def __init__(self,y):
        Card.__init__(self,y)
