from uuid import uuid4

from ..VoronoiEdge import VoronoiEdge

import json

def test_to_json():
    identifier0 = uuid4()
    identifier1 = uuid4()
    neighborIdentifier = uuid4()

    voronoiEdge = VoronoiEdge(vertexIdentifier0 = identifier0, vertexIdentifier1 = identifier1, neighborSiteIdentifier = neighborIdentifier)
    voronoiEdgeJson = json.loads(repr(voronoiEdge))

    assert len(voronoiEdgeJson.keys()) == 3

    assert voronoiEdgeJson["vertexIdentifier0"] == str(identifier0)
    assert voronoiEdgeJson["vertexIdentifier1"] == str(identifier1)
    assert voronoiEdgeJson["neighborSiteIdentifier"] == str(neighborIdentifier)