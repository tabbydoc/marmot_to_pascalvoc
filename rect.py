# -⁠*-⁠ coding: utf-⁠8 -⁠*-⁠

# rectangle
class Rect:
    """Rectangle class.
    @remark The origin of the coordinate system is at the left-bottom corner of page.\n
    The unit of length is "pound", which is 1/⁠72 inch.
    """
    def __init__(self, x0, y0, x1, y1):
        """
        @param x0 the less of left and right
        @param y0 the less of top and bottm
        @param x1 the greater of left and right
        @param y1 the greater of top and bottom
        @remark If x0 is greater than x1, they are swapped to build the rect.
        So for the y's.
        """
        self._x0 = min(x0, x1)
        self._y0 = min(y0, y1)
        self._x1 = max(x0, x1)
        self._y1 = max(y0, y1)

    def x0(self):
        return self._x0

    def y0(self):
        return self._y0

    def x1(self):
        return self._x1

    def y1(self):
        return self._y1

    def width(self):
        return abs(self._x1-self._x0)

    def height(self):
        return abs(self._y1-self._y0)

    def area(self):
        return self.width() * self.height()

    # def isEligible(self):
    #     return not (self._x0 > self._x1 or self._y0 > self._y1)

    def isOverlap(self, rect):
        """
        @param rect the other rectangle
        @return True if rect overlaps with this rect;\n
        False elsewise.
        """
        return min(self._x1, rect._x1) > max(self._x0, rect._x0) and    \
               min(self._y1, rect._y1) > max(self._y0, rect._y0)

    def isInside(self, rect):
        """
        @param rect the other rectangle
        @return True if this rect is inside rect;
        False elsewise.
        """
        return self._x0 > rect._x0 and  \
               self._y0 > rect._y0 and  \
               self._x1 < rect._x1 and  \
               self._y1 < rect._y1

    def distanceX(self, rect):
        """
        @param rect the other rectangle
        @return distance along x axis.
        @remark If the rects overlap along x axis,
        distanceX will return a negative value, whose abstract value indicates
        how much they overlap along x axis;\n
        elsewise the distance is positive.
        """
        return max(self._x0, rect._x0) - min(self._x1, rect._x1)

    def distanceY(self, rect):
        """
        @param rect the other rectangle
        @return distance along y axis.
        @remark Similar to distanceX except that the distance is along y axis.
        """
        return max(self._y0, rect._y0) - min(self._y1, rect._y1)

    def __str__(self):
        return '[x0:%.2f, y0:%.2f, x1:%.2f, y1:%.2f]' % \
               (self._x0, self._y0, self._x1, self._y1)

    @staticmethod
    def intersection(lhs, rhs):
        """
        @param lhs one rectangle
        @param rhs the other rectangle
        @return intersection of two rectangles.
        @remark This is a static method.\n
        Make sure lhs.isOverlap(rhs) returns True, or the returned
        rectangle is ill formed.
        """
        return Rect(max(lhs._x0, rhs._x0),
                    max(lhs._y0, rhs._y0),
                    min(lhs._x1, rhs._x1),
                    min(lhs._y1, rhs._y1))

    @staticmethod
    def union(lhs, rhs):
        """
        @param lhs one rectangle
        @param rhs the other rectangle
        @return Union of two rectangles.
        @remark This is a static method.
        """
        return Rect(min(lhs._x0, rhs._x0),
                    min(lhs._y0, rhs._y0),
                    max(lhs._x1, rhs._x1),
                    max(lhs._y1, rhs._y1))

