from uuid import uuid4

from ..edges.VoronoiEdge import VoronoiEdge
from ..regions.VoronoiRegion import VoronoiRegion

import json

def _makeVoronoiEdge() -> VoronoiEdge:
    return VoronoiEdge(edgeId = uuid4(), vertex0Id = uuid4(), vertex1Id = uuid4(), edgeLength = 0.0)

testVoronoiEdge = _makeVoronoiEdge()
testOtherVoronoiEdge = _makeVoronoiEdge()

testEdgesToNeighbors = {
    testVoronoiEdge.edgeId: uuid4(),
    testOtherVoronoiEdge.edgeId: uuid4()
}

testVoronoiRegion = VoronoiRegion(siteId = uuid4(), edges = tuple((testVoronoiEdge, testOtherVoronoiEdge)), edgesToNeighbors = testEdgesToNeighbors)

def test_neighbors():
    assert testVoronoiRegion.neighbors() == tuple(testEdgesToNeighbors.values())

def test_to_json():
    regionJson = json.loads(repr(testVoronoiRegion))

    assert len(regionJson.keys()) == 2

    assert regionJson["siteId"] == str(testVoronoiRegion.siteId)
    
    assert str(testVoronoiEdge.edgeId) in regionJson["edges"]
    assert str(testOtherVoronoiEdge.edgeId) in regionJson["edges"]