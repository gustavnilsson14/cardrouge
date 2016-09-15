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

class Search:

    def binary_search(a, x, lo=0, hi=None):   # can't use a to specify default for hi
        hi = hi if hi is not None else len(a) # hi defaults to len(a)
        pos = bisect_left(a,x,lo,hi)          # find insertion position
        return (pos if pos != hi and a[pos] == x else -1) # don't walk off the end
