from entity import Item

class Card(Item):

    def __init__(self,y):
        Item.__init__(self,y)
        self.animation_duration = 0.1
        self.animation = 'default'
        self.target = 0

    def set_target(self,target):
        self.target = target

    def get_animation(self):
        return (self.target,self.animation)

class Currency(Item):
    pass

class Kit(Item):

    def equip(self,position,bossmonster,console,kernel):
        self.owner.bossbastard.run_alg(console,kernel)
