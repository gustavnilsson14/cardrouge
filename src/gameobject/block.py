from entity import Block

class GroundBlock(Block):

    def __init__(self):
        Block.__init__(self)
        self.image = "res/sprites/blocks/cliffgrass.png"

class RampBlock(Block):

    def __init__(self):
        Block.__init__(self)
        self.walkable = 1
        self.offset_next_height = -10
        self.image = "res/sprites/blocks/clifframp.png"

class LavaBlock(Block):
    pass
