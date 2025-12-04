from dataclasses import dataclass
from uuid import uuid4

from .VoronoiEdge import VoronoiEdge

@dataclass(frozen=True)
class VoronoiRegion:
    siteIdentifier: uuid4
    edges: tuple[VoronoiEdge]

    def neighbors(self) -> tuple[uuid4]:
        return tuple((edge.neighborSiteIdentifier for edge in self.edges))
    
    def __repr__(self) -> str:
        edges = ",".join(tuple(repr(edge) for edge in self.edges))
        return f'{{"siteIdentifier": "{str(self.siteIdentifier)}", "edges": [{edges}]}}'