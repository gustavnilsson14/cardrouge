from entity import Block

class GroundBlock(Block):

    def __init__(self):
        Block.__init__(self)
        self.image = "res/sprites/blocks/cliffgrass.png"

class RampBlock(Block):

    def __init__(self):
        Block.__init__(self)
        self.image = "res/sprites/blocks/clifframp.png"

class LavaBlock(Block):
    pass
