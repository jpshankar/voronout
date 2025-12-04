from dataclasses import dataclass
from uuid import uuid4

@dataclass(frozen=True)
class VoronoiEdge:
    vertexIdentifier0: uuid4
    vertexIdentifier1: uuid4
    neighborSiteIdentifier: uuid4

    def __repr__(self) -> str:
        return f'{{"vertexIdentifier0": "{str(self.vertexIdentifier0)}", "vertexIdentifier1": "{str(self.vertexIdentifier1)}", "neighborSiteIdentifier": "{str(self.neighborSiteIdentifier)}"}}'