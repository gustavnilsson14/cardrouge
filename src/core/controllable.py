class Controllable:
    def __init__(self, game_map, state):
        self.controllable_entities = []
        self.game_map = game_map
        self.state = state

    def add_unit(self, controllable_entity):
        if controllable_entity not in self.controllable_entities:
            self.controllable_entities.append(controllable_entity)
            return controllable_entity
        return 0

    def remove_unit(self,controllable_entity):
        if controllable_entity in self.controllable_entities:
            self.controllable_entities.remove(controllable_entity)
            controllable_entity.tile.remove_entity(controllable_entity)
            return 1
        return 0

    def spawn_animations(self):
        animations = []
        for entity in self.controllable_entities:
            if entity.active_card != 0:
                animations += [entity.active_card.get_animation()]
        return animations
