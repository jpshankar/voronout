from uuid import uuid4

from ..VoronoiEdge import VoronoiEdge
from ..VoronoiRegion import VoronoiRegion

import json

def _makeVoronoiEdge() -> VoronoiEdge:
    return VoronoiEdge(vertexIdentifier0 = uuid4(), vertexIdentifier1 = uuid4(), neighborSiteIdentifier = uuid4())

testVoronoiEdge = _makeVoronoiEdge()
testOtherVoronoiEdge = _makeVoronoiEdge()
testVoronoiRegion = VoronoiRegion(siteIdentifier = uuid4(), edges = tuple((testVoronoiEdge, testOtherVoronoiEdge)))

def test_neighbors():
    regionNeighbors = testVoronoiRegion.neighbors()
    assert tuple((testVoronoiEdge.neighborSiteIdentifier, testOtherVoronoiEdge.neighborSiteIdentifier)) == regionNeighbors

def test_to_json():
    regionJson = json.loads(repr(testVoronoiRegion))

    assert len(regionJson.keys()) == 2

    assert regionJson["siteIdentifier"] == str(testVoronoiRegion.siteIdentifier)
    assert regionJson["edges"] == [json.loads(repr(testVoronoiEdge)), json.loads(repr(testOtherVoronoiEdge))]