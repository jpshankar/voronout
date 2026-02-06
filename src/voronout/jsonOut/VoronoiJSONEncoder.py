from json import JSONEncoder, loads as loadJSONString
from uuid import UUID

from ..Point import Point
from ..VoronoiDiagram import VoronoiDiagram

class VoronoiJSONEncoder(JSONEncoder):
    def _handlePointDict(self, pointDict: dict[UUID, Point]) -> dict[str, dict[str, float]]:
        return { str(key): loadJSONString(repr(value)) for (key, value) in pointDict.items() }
    
    def _handleIdDict(self, idDict: dict[UUID, tuple[UUID]]) -> dict[str, tuple[str]]:
        return { str(idKey): tuple((str(idVal) for idVal in idVals)) for (idKey, idVals) in idDict.items() }
    
    def default(self, obj):
        if isinstance(obj, VoronoiDiagram):
            regionNeighbors = self._handleIdDict(idDict = obj.regionNeighbors)
            edges = {str(diagramEdge.edgeId): {"vertex0Id": str(diagramEdge.vertex0Id), "vertex1Id": str(diagramEdge.vertex1Id)} for diagramEdge in obj.diagramEdges}
            
            return {
                'points': self._handlePointDict(obj.points),
                'vertices': self._handlePointDict(obj.vertices),
                'edges': edges,
                'regions': tuple((loadJSONString(repr(region)) for (_, region) in obj.voronoiRegions.items())),
                'regionNeighbors': regionNeighbors
            }
        else:
            return super().default(obj)