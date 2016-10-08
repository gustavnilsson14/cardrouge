from bisect import bisect_left
import math

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
        for index,entity in enumerate(a):
            if entity.y == x:
                return index
        return None
        #TODO: magic sparkles
        '''
        hi = hi if hi is not None else len(a) # hi defaults to len(a)
        print(a,x,lo,hi)
        pos = bisect_left(a,x,lo,hi)          # find insertion position
        return (pos if pos != hi and a[pos] == x else -1) # don't walk off the end
        '''

class Raycast:

    def cast(start, target):
        raycast_line = Raycast.bresenhamLine(start.pos, target.pos)
        return raycast_line


    def is_traversable(target):
        pass

    def swap(a, b):
        c = a;
        a = b;
        b = c;
        return (a,b)

    def bresenhamLine(start ,target):
        result = []

        x0 = start[0]
        y0 = start[1]
        x1 = target[0]
        y1 = target[1]

        steep = int(math.fabs(y1 - y0)) > int(math.fabs(x1 - x0))

        if steep:
            (x0, y0) = Raycast.swap(x0, y0)
            (x1, y1) = Raycast.swap(x1, y1)

        if x0 > x1:
            (x0, x1) = Raycast.swap(x0, x1)
            (y0, y1) = Raycast.swap(y0, y1)


        deltax = x1 - x0
        deltay = int(math.fabs(y1 - y0))
        error = 0
        y = y0
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1

        for x in range(x0, x1):
            if steep:
                result += [(y, x)]
            else:
                result += [(x, y)]
            error += deltay
            if 2 * error >= deltax:
                y += ystep
                error -= deltax


        return result;

class TupleHelper:

    @staticmethod
    def add_i(tuple1,i):
        if len(tuple1) == 2:
            return (tuple1[0]+i,tuple1[1]+i)
        if len(tuple1) == 3:
            return (tuple1[0]+i,tuple1[1]+i,tuple1[2]+i)
        if len(tuple1) == 4:
            return (tuple1[0]+i,tuple1[1]+i,tuple1[2]+i,tuple1[3]+i)
        return (0,0)

    @staticmethod
    def add_t(tuple1,tuple2):
        if len(tuple1) == 2:
            return (tuple1[0]+tuple2[0],tuple1[1]+tuple2[1])
        if len(tuple1) == 3:
            return (tuple1[0]+tuple2[0],tuple1[1]+tuple2[1],tuple1[2]+tuple2[2])
        if len(tuple1) == 4:
            return (tuple1[0]+tuple2[0],tuple1[1]+tuple2[1],tuple1[2]+tuple2[2],tuple1[3]+tuple2[3])
        return (0,0)
