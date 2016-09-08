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


class IsoConverter():

    def to_iso(point):
        x = point.x - point.y
        y = (point.x + point.y) / 2
        return Point(x, y)

    def to_2d(point):
        x = (2*point.y + point.x)/2
        y = (2*point.y - point.x)/2
        return Point(x, y)
