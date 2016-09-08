from entity import Unit

class GroundUnit(Unit):

    def __init__(self):
        Unit.__init__(self)

class AirUnit(Unit):
    pass

class TestUnit(GroundUnit):

    def __init__(self):
        GroundUnit.__init__(self)
