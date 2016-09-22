class Controllable:
    def __init__(self, game_map):
        self.controllable_entities = []
        self.game_map = game_map

    def addUnit(self, controllable_entity):
        self.controllable_entities.append(controllable_entity)
