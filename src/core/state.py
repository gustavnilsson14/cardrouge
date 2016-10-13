class State:

    def __init__(self,owner):
        self.owner = owner

    def change_state(self,state):
        self.owner.state = state
