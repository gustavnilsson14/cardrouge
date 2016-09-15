from entity import Block

class SolidBlock(Block):
    def __init__(self,y):
        Block.__init__(self,y)
        self.image = "res/sprites/blocks/cliffgrass.png"
        self.stop_draw = 1
        self.solid = 1
        #self.friction = 1

class HollowBlock(Block):
    def __init__(self,y):
        Block.__init__(self,y)
        #self.density = 1
        self.image = "res/sprites/blocks/cliffgrass.png"

class GroundBlock(SolidBlock):

    def __init__(self,y):
        SolidBlock.__init__(self,y)
        self.image = "res/sprites/blocks/cliffgrass.png"

class RampBlock(SolidBlock):

    def __init__(self,y):
        SolidBlock.__init__(self,y)
        self.walkable = 1
        self.offset_next_height = -10
        self.image = "res/sprites/blocks/clifframp.png"

class WaterBlock(HollowBlock):

    def __init__(self,y):
        HollowBlock.__init__(self,y)
        self.image = "res/sprites/blocks/water7.png"

class LavaBlock(Block):
    pass
