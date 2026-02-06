from dataclasses import dataclass, field
from uuid import uuid4

from ..edges.VoronoiEdge import VoronoiEdge

@dataclass
class VoronoiRegionData:
    siteId: uuid4
    
    _edges: set[VoronoiEdge] = field(default_factory=set)
    _neighborRegionIds: set[uuid4] = field(default_factory=set)

    _edgesToNeighbors: dict[uuid4, uuid4] = field(default_factory=dict)

    def addEdge(self, edge: VoronoiEdge) -> bool:
        self._edges.add(edge)
        
    def addNeighborRegionId(self, borderingEdgeId: uuid4, neighborRegionId: uuid4):
        self._neighborRegionIds.add(neighborRegionId)
        self._edgesToNeighbors[borderingEdgeId] = neighborRegionId

    def getEdgeNeighborRegion(self, edgeId: uuid4) -> uuid4:
        if edgeId in self._edgesToNeighbors:
            return self._edgesToNeighbors[edgeId]
        else:
            return None

    def edges(self) -> tuple[VoronoiEdge]:
        return tuple(self._edges)

    def edgesToNeighbors(self) -> dict[uuid4, uuid4]:
        return self._edgesToNeighbors