from dataclasses import dataclass
from math import sqrt

import numpy as np

from .utils import boundValue

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __init__(self, x, y):
        object.__setattr__(self, "x", boundValue(value = x))
        object.__setattr__(self, "y", boundValue(value = y))

    @classmethod
    def distance(cls, p1: Point, p2: Point) -> float:
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        return boundValue(value = sqrt(pow(dx, 2) + pow(dy, 2)))

    @classmethod
    def midpoint(cls, p1: Point, p2: Point) -> Point:
        midpointX = boundValue(value = (p1.x + p2.x)/2)
        midpointY = boundValue(value = (p1.y + p2.y)/2)

        return Point(x = midpointX, y = midpointY)
    
    # For converting between 0, 0 (top-left) and 0, 0 (bottom-left).
    def convertPointBase(self):
        return Point(x = self.x, y = boundValue(value = 1 - self.y))
    
    # For ease of JSON conversion.
    def __repr__(self) -> str:
        return f'{{"x": {self.x}, "y": {self.y}}}'
    
    # For using Point in scipy.spatial methods that take ArrayLike parameters.
    def __array__(self, dtype=None, copy=None):
        return np.array(tuple((self.x, self.y)))