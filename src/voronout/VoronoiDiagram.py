from .Boundary import Boundary
from .Point import Point

from .VoronoiEdge import VoronoiEdge
from .VoronoiRegion import VoronoiRegion

from scipy.spatial import Voronoi
from uuid import uuid4

import numpy as np

class VoronoiDiagram:
    def __init__(self, basePoints: tuple[Point]):
        # We expect basePoints to have 0, 0 (top-left), but scipy.spatial does 0, 0 (bottom-left) - so convert.
        sciPySpatialPoints = np.array(tuple(basePoint.convertPointBase() for basePoint in basePoints))        
        self._voronoiDiagram = Voronoi(sciPySpatialPoints)

        # Make the diagram's regions according to 0, 0 (bottom-left)..
        self._spatialPoints = { uuid4(): Point(x = spatialPoint[0], y = spatialPoint[1]) for spatialPoint in self._voronoiDiagram.points }
        self._spatialPointsKeys = tuple(self._spatialPoints.keys())

        self._spatialDiagramVertices = { uuid4(): Point(x = spatialDiagramVertex[0], y = spatialDiagramVertex[1]) for spatialDiagramVertex in self._voronoiDiagram.vertices}
        self._spatialDiagramVerticesKeys = tuple(self._spatialDiagramVertices.keys())

        self._spatialBoundaryVertices: dict[uuid4, Point] = {}
        self._spatialBoundaryVerticesKeys: dict[Point, uuid4] = {}

        self.voronoiRegions = { spatialPointKey: self._makeVoronoiRegion(spatialPointKey) for spatialPointKey in self._spatialPointsKeys }

        # .. and then convert to (top-left).
        self.points = {pointId: point.convertPointBase() for (pointId, point) in self._spatialPoints.items()}
        self.diagramVertices = {diagramVertexId: diagramVertex.convertPointBase() for (diagramVertexId, diagramVertex) in self._spatialDiagramVertices.items()}
        self.boundaryVertices = {boundaryVertexId: boundaryVertex.convertPointBase() for (boundaryVertexId, boundaryVertex) in self._spatialBoundaryVertices.items()}

    def _checkCalculatedMidpointInsideVoronoiRegion(self, calculatedMidpoint: Point, calculationPoint1: Point, calculationPoint2: Point) -> bool:
        otherSites = tuple((otherSite for otherSite in self._spatialPoints.values() if otherSite != calculationPoint1 and otherSite != calculationPoint2))

        calculationPoint1Dist = Point.distance(p1 = calculatedMidpoint, p2 = calculationPoint1)
        calculationPoint2Dist = Point.distance(p1 = calculatedMidpoint, p2 = calculationPoint2)

        otherSiteDistances = tuple((Point.distance(p1 = calculatedMidpoint, p2 = otherSite) for otherSite in otherSites))

        # If calculatedMidpoint is closer to an otherSite than the two points, it's in a region.
        return any((otherSiteDistance < calculationPoint1Dist and otherSiteDistance < calculationPoint2Dist for otherSiteDistance in otherSiteDistances))

    def _makeVoronoiEdge(self, firstVertexIndex: int, secondVertexIndex: int, regionIdIndex: int, neighborRegionIdIndex: int) -> VoronoiEdge:
        allDiagramVertices = firstVertexIndex > -1 and secondVertexIndex > -1
        if allDiagramVertices:
            diagramVertexIdentifier0 = self._spatialDiagramVerticesKeys[firstVertexIndex]
            diagramVertexIdentifier1 = self._spatialDiagramVerticesKeys[secondVertexIndex]

            diagramVertex0 = self._spatialDiagramVertices[diagramVertexIdentifier0]
            diagramVertex1 = self._spatialDiagramVertices[diagramVertexIdentifier1]

            maybeBoundedZero = Boundary.maybeBoundVertex(maybeBoundableVertex = diagramVertex0, otherVertex = diagramVertex1)
            if maybeBoundedZero:
                self._spatialDiagramVertices[diagramVertexIdentifier0] = maybeBoundedZero

            maybeBoundedOne = Boundary.maybeBoundVertex(maybeBoundableVertex = diagramVertex1, otherVertex = self._spatialDiagramVertices[diagramVertexIdentifier0])
            if maybeBoundedOne:
                self._spatialDiagramVertices[diagramVertexIdentifier1] = maybeBoundedOne

            return VoronoiEdge(vertexIdentifier0 = diagramVertexIdentifier0, vertexIdentifier1 = diagramVertexIdentifier1, neighborSiteIdentifier = self._spatialPointsKeys[neighborRegionIdIndex])
                
        else:
            regionSiteId = self._spatialPointsKeys[regionIdIndex]
            neighborRegionSiteId = self._spatialPointsKeys[neighborRegionIdIndex]

            regionSite = self._spatialPoints[regionSiteId]
            neighborRegionSite = self._spatialPoints[neighborRegionSiteId]

            calculatedMidpoint = Point.midpoint(regionSite, neighborRegionSite)
            midpointInOtherRegion = self._checkCalculatedMidpointInsideVoronoiRegion(calculatedMidpoint = calculatedMidpoint, calculationPoint1 = regionSite, calculationPoint2 = neighborRegionSite)

            # The diagram vertex is the one whose index is not == -1.
            diagramVertexKey = self._spatialDiagramVerticesKeys[firstVertexIndex] if firstVertexIndex > -1 else self._spatialDiagramVerticesKeys[secondVertexIndex]
            diagramVertex = self._spatialDiagramVertices[diagramVertexKey]

            # If midpointInOtherRegion, just look for the closest boundary - otherwise, it's on an edge, and we can look for the boundary the edge would eventually hit.
            closestBoundary = Boundary.findClosestBoundaryToPoint(point = calculatedMidpoint, boundaries = (Boundary.TOP, Boundary.RIGHT, Boundary.BOTTOM, Boundary.LEFT)) if midpointInOtherRegion else Boundary.findBoundaryInLineDirection(linePoint1 = diagramVertex, linePoint2 = calculatedMidpoint)

            # Where (diagramVertex, midpoint) would intersect the closest boundary.
            boundaryIntersectionPoint = Boundary.boundaryLineIntersectionPoint(lineFirstPoint = diagramVertex, lineSecondPoint = calculatedMidpoint, boundary = closestBoundary)

            # Avoid adding the same vertex multiple times.
            pointAlreadyCalculated = boundaryIntersectionPoint in self._spatialBoundaryVerticesKeys
            boundaryVerticesKey = self._spatialBoundaryVerticesKeys[boundaryIntersectionPoint] if pointAlreadyCalculated else uuid4()
            
            if not pointAlreadyCalculated:
                self._spatialBoundaryVertices[boundaryVerticesKey] = boundaryIntersectionPoint
                self._spatialBoundaryVerticesKeys[boundaryIntersectionPoint] = boundaryVerticesKey

            return VoronoiEdge(vertexIdentifier0 = diagramVertexKey, vertexIdentifier1 = boundaryVerticesKey, neighborSiteIdentifier = neighborRegionSiteId)
    
    def _makeVoronoiRegion(self, regionSiteIdentifier: uuid4) -> VoronoiRegion:
        regionSiteIdIndex = self._spatialPointsKeys.index(regionSiteIdentifier)
        edgeRegions = tuple((ridgeRegionsIndex, ridgeRegions) for (ridgeRegionsIndex, ridgeRegions) in enumerate(self._voronoiDiagram.ridge_points) if regionSiteIdIndex in ridgeRegions)

        voronoiEdges = []
        for (edgeRegionsIndex, regionAndNeighbor) in edgeRegions:
            neighborSiteIdIndex = regionAndNeighbor[0] if regionAndNeighbor[1] == regionSiteIdIndex else regionAndNeighbor[1]
            edgeVerticies = self._voronoiDiagram.ridge_vertices[edgeRegionsIndex]

            voronoiEdge = self._makeVoronoiEdge(firstVertexIndex = edgeVerticies[0], secondVertexIndex = edgeVerticies[1], regionIdIndex = regionSiteIdIndex, neighborRegionIdIndex = neighborSiteIdIndex)
            voronoiEdges.append(voronoiEdge)

        return VoronoiRegion(siteIdentifier = regionSiteIdentifier, edges = voronoiEdges)