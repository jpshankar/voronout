from ..Point import Point
from ..VoronoiDiagram import VoronoiDiagram

from math import isclose
from uuid import uuid4

# All sites (and expected values) calculated via https://cfbrasz.github.io/Voronoi.html (x = "50 150 400", y = "120 250 90")
siteOne = Point(x = 0.0556, y = 0.1333)
siteTwo = Point(x = 0.1667, y = 0.2778)
siteThree = Point(x = 0.4444, y = 0.1000)

# For each region in testPoints, the neighbors are the other points' regions.
sitesExpectedNeighbors = {
    siteOne: tuple((siteTwo, siteThree)),
    siteTwo: tuple((siteOne, siteThree)),
    siteThree: tuple((siteOne, siteTwo))
}

expectedDiagramVertex = Point(x = 0.2486, y = 0.0999)

expectedBoundaryVertex1 = Point(x = 0, y = 0.291)
expectedBoundaryVertex2 = Point(x = 0.2402, y = 0)
expectedBoundaryVertex3 = Point(x = 0.8241, y = 1)

def _idsByPoint(pointsById: dict[uuid4, Point]) -> dict[Point, uuid4]:
    return {point: pointId for (pointId, point) in pointsById.items()}

# Verifies that VoronoiDiagram is constructed as expected.
def test_voronoi_diagram():
    testPoints = tuple((siteOne, siteTwo, siteThree))
    voronoiDiagram = VoronoiDiagram(basePoints = testPoints)

    # We should have only one diagram vertex..
    assert len(voronoiDiagram.diagramVertices) == 1
    
    (diagramVertexId, diagramVertex) = tuple(voronoiDiagram.diagramVertices.items())[0]

    assert diagramVertex == expectedDiagramVertex

    # .. and three boundary vertices.
    assert len(voronoiDiagram.boundaryVertices) == 3

    boundaryVertices = voronoiDiagram.boundaryVertices.values()

    assert expectedBoundaryVertex1 in boundaryVertices
    assert expectedBoundaryVertex2 in boundaryVertices
    assert expectedBoundaryVertex3 in boundaryVertices
    
    # Identifiers are randomly generated, so we need to dynamically get them.
    voronoiDiagramPointsIdMap = _idsByPoint(pointsById = voronoiDiagram.points)
    
    # Check that we only have the points we passed in..
    assert len(voronoiDiagramPointsIdMap) == len(testPoints)

    # .. and then check the data in terms of each point.
    for testPoint in testPoints:
        testPointIdentifier = voronoiDiagramPointsIdMap[testPoint]
        testPointRegion = voronoiDiagram.voronoiRegions[testPointIdentifier]

        assert testPointRegion.siteIdentifier == testPointIdentifier
        
        testPointRegionNeighbors = set(testPointRegion.neighbors())

        testExpectedNeighbors = sitesExpectedNeighbors[testPoint]
        testExpectedIdentifiers = set((voronoiDiagramPointsIdMap[testExpectedNeighbor] for testExpectedNeighbor in testExpectedNeighbors))

        assert testPointRegionNeighbors == testExpectedIdentifiers

   