from state import State

class StateAlive(State):

    def __init__(self,owner):
        State.__init__(self,owner)

class StateDead(State):

    def __init__(self,owner):
        State.__init__(self,owner)

    def update(self):
        print("IM DEAD")
