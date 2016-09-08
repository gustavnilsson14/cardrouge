from entity import *

class GroundUnit(Unit):

    def __init__(self,vector):
        Unit.__init__(self,vector)

class AirUnit(Unit):
    pass

class TestUnit(GroundUnit):

    def __init__(self,vector):
        GroundUnit.__init__(self,vector)
