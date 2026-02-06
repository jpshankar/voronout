from uuid import uuid4

from ..edges.VoronoiEdge import VoronoiEdge

import json

def test_to_json():
    identifier0 = uuid4()
    identifier1 = uuid4()
    edgeLength = 0.0

    voronoiEdge = VoronoiEdge(edgeId = uuid4(), vertex0Id = identifier0, vertex1Id = identifier1, edgeLength = edgeLength)
    voronoiEdgeJson = json.loads(repr(voronoiEdge))

    assert len(voronoiEdgeJson.keys()) == 3

    assert voronoiEdgeJson["vertex0Id"] == str(identifier0)
    assert voronoiEdgeJson["vertex1Id"] == str(identifier1)
    assert voronoiEdgeJson["edgeLength"] == edgeLength