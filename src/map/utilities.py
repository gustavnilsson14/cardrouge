class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def as_tuple(self):
        return (self.x, self.y)

    def x(self):
        return self.x

    def y(self):
        return self.y

    def to_iso():
        self = IsoConverter().to_iso(self)


class IsoConvertableObject:

    def to_iso(self,vector):
        x = vector[0] - vector[1]
        y = (vector[0] + vector[1]) / 2
        return (x,y)

    def to_2d(self,vector):
        x = (2*vector[1] + vector[0])/2
        y = (2*vector[1] - vector[0])/2
        return (x,y)
