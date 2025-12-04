from ..Point import Point
from ..Boundary import Boundary

import pytest

testBoundaries = tuple((Boundary.LEFT, Boundary.RIGHT))

testFirstPoint = Point(x = 0.3, y = 0.4)
testSecondPoint = Point(x = -0.1, y = -0.2)

def test_find_closest_boundary_point_before():
    pointBefore = Point(x = 1.1, y = 0)
    assert Boundary.findClosestBoundaryToPoint(point = pointBefore, boundaries = testBoundaries) == Boundary.RIGHT

def test_find_closest_boundary_point_after():
    pointAfter = Point(x = 0.9, y = 0)
    assert Boundary.findClosestBoundaryToPoint(point = pointAfter, boundaries = testBoundaries) == Boundary.RIGHT

findBoundaryTestData = [
    [Point(x = 0.6, y = 0.4), Boundary.RIGHT], # Quadrant 1, angle < 45 degrees (counter-clockwise from east)
    [Point(x = 0.4, y = 0.6), Boundary.TOP], # Quadrant 1, 45 degrees < angle < 90 degrees
    [Point(x = -0.4, y = 0.6), Boundary.TOP], # Quadrant 2, 90 degrees < angle < 135 degrees
    [Point(x = -0.6, y = 0.4), Boundary.LEFT], # Quadrant 2, 135 degrees < angle < 180 degrees
    [Point(x = -0.6, y = -0.4), Boundary.LEFT], # Quadrant 3, 180 degrees < angle < 225 degrees
    [Point(x = -0.4, y = -0.6), Boundary.BOTTOM], # Quadrant 3, 225 degrees < angle < 270 degres
    [Point(x = 0.4, y = -0.6), Boundary.BOTTOM], # Quadrant 4, 270 degrees < angle < 315 degrees
    [Point(x = 0.6, y = -0.4), Boundary.RIGHT] # Quadrant 4, 315 degrees < angle < 360 degrees
]

@pytest.mark.parametrize("linePoint, expectedBoundary", findBoundaryTestData)
def test_find_boundary_in_line_direction(linePoint: Point, expectedBoundary: Boundary):
    quadrantPoint = Point(x = 0, y = 0)
    assert Boundary.findBoundaryInLineDirection(linePoint1 = quadrantPoint, linePoint2 = linePoint) == expectedBoundary

def test_find_boundary_line_intersection_point_no_bounding():
    intersectionPoint = Boundary.boundaryLineIntersectionPoint(lineFirstPoint = testFirstPoint, lineSecondPoint = Point(x = -0.1, y = 0), boundary = Boundary.LEFT)
    
    # (0.3, 0.4) -> (-0.1, 0) would intersect at (0, 0.1) - no bounding needed
    assert intersectionPoint.x == 0
    assert intersectionPoint.y == 0.1

def test_find_boundary_line_intersection_point_bounded():
    intersectionPoint = Boundary.boundaryLineIntersectionPoint(lineFirstPoint = testFirstPoint, lineSecondPoint = testSecondPoint, boundary = Boundary.LEFT)
    
    # (0.3, 0.4) -> (-0.1, -0.2) would intersect at (0, -0.05) - we'd bound it to (0.0333, 0)
    assert intersectionPoint.x == 0.0333
    assert intersectionPoint.y == 0

def test_bound_vertex_x_left():
    boundLeftXPoint = Point(x = -0.1, y = 0.2)

    boundedXPoint = Boundary.maybeBoundVertex(maybeBoundableVertex = boundLeftXPoint, otherVertex = testFirstPoint)
    
    # " Bounding " expected results were calculated via solving dy = (dy/dx) * dx as described in Boundary.maybeBoundVertex.
    assert boundedXPoint.x == 0
    assert boundedXPoint.y == 0.25

def test_bound_vertex_x_right():
    boundRightXPoint = Point(x = 1.1, y = 0.2)

    boundedXPoint = Boundary.maybeBoundVertex(maybeBoundableVertex = boundRightXPoint, otherVertex = testFirstPoint)
    
    assert boundedXPoint.x == 1
    assert boundedXPoint.y == 0.225

def test_bound_vertex_y_bottom():
    boundBottomYPoint = Point(x = 0.1, y = -0.1)

    boundedYPoint = Boundary.maybeBoundVertex(maybeBoundableVertex = boundBottomYPoint, otherVertex = testFirstPoint)

    assert boundedYPoint.x == 0.14
    assert boundedYPoint.y == 0

def test_bound_vertex_y_top():
    boundBottomYPoint = Point(x = 0.1, y = 1.1)

    boundedYPoint = Boundary.maybeBoundVertex(maybeBoundableVertex = boundBottomYPoint, otherVertex = testFirstPoint)

    assert boundedYPoint.x == 0.1286
    assert boundedYPoint.y == 1

# x and y both needing bounding are possible edge cases.
def test_bound_vertex_x_and_y_negative():
    boundXAndYPoint = Point(x = -0.1, y = -0.2)

    boundedXAndYPoint = Boundary.maybeBoundVertex(maybeBoundableVertex = boundXAndYPoint, otherVertex = testFirstPoint)

    assert boundedXAndYPoint.x == 0.0333
    assert boundedXAndYPoint.y == 0

def test_bound_vertex_x_and_y_positive():
    boundXAndYPoint = Point(x = 1.1, y = 1.2)

    boundedXAndYPoint = Boundary.maybeBoundVertex(maybeBoundableVertex = boundXAndYPoint, otherVertex = testFirstPoint)

    assert boundedXAndYPoint.x == 0.9
    assert boundedXAndYPoint.y == 1

def test_bound_vertex_not_needed():
    boundingNotNeededPoint = Point(x = 0.1, y = 0.2)

    maybeBoundedPoint = Boundary.maybeBoundVertex(maybeBoundableVertex = boundingNotNeededPoint, otherVertex = testFirstPoint)

    assert not maybeBoundedPoint

