# Voronout is..

.. a Python module that, given a set of points on a 2D plane bounded by `0 <= x <= 1` and `0 <= y <= 1`, outputs JSON describing the Voronoi diagram computed from those points.

The Voronoi computation is [SciPy's](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html#scipy.spatial.Voronoi). Voronout translates that into more easily parsible JSON:

```
{
    "points": {.."<pointUUID>": {"x": <point.x>, "y": <point.y>}..},
    "diagramVertices": {.."<diagramVertexUUID>": {"x": <diagramVertex.x>, "y": <diagramVertex.y>}..},
    "boundaryVertices": {.."<boundaryVertexUUID>": {"x": <point.x>, "y": <point.y>}..},
    "regions": [
        ..
        {
            "siteIdentifier": "<pointUUID>",
            "edges": [
                ..
                {
                    "vertexIdentifier0": <diagramVertexUUID/boundaryVertexUUID>,
                    "vertexIdentifier1": <diagramVertexUUID/boundaryVertexUUID>,
                    "neighborSiteIdentifier": <pointUUID>
                }
                ..
            ]
        }
        ..
    ]
}
```

`points` are the points provided to compute the diagram. Each point (`site`) is associated with a `region`, a section of the 2D plane containing all points closer to the region's particular `site` than to any other.

`points`, like all coordinate data in this JSON, are indexed by unique UUID. This allows us to describe the region in terms of those UUIDs.

The primary use of that is with `diagramVertices` and `boundaryVertices`. They're not region sites - they're the vertices of the edges that bound the regions. Since any given Voronoi edge vertex is likely to be part of multiple edges, it looks better to describe that vertex by its associated UUID than to copy the same coordinate data multiple times.

`diagramVertices` are calculated when creating the Voronoi diagram. `boundaryVertices` are calculated when processing the created diagram. It's possible that the diagram could include edges with vertices outside the plane - x > 1 or < 0, y > 1 or < 0. This is correctly part of the diagram, but not optimal in terms of the 2D plane's boundaries.

### We keep the diagram within the plane by..

* Determining which of its four boundaries it would intersect with
* Figuring out where the boundary and the edge, two lines, would intersect
* Replacing the " outside the plane " vertice with that point of intersection
* Storing that point of intersection in `boundaryVertices`

`regions` combines the above information:

* `siteIdentifier` indicates which `point` the region was computed with respect to
* `edges` is the edges bounding the region
    * Each `edge` indicates the two vertices composing it and, via `neighborSiteIdentifier`, the region immediately opposite to it

# How do we generate and use that information?

We first determine our list of points, taking (0, 0) as the top left corner of the plane:

```Python
basePoints = tuple((
    Point(.25, .25),
    Point(.40, .75),
    Point(.75, .25),
    Point(.60, .75),
    Point(.40, .40),
    Point(.30, .30),
    Point(.60, .30)
))
```

(The 0/1 bounding allows for intuitive specification of points. Instead of calculating the exact x and y coords in terms of the space width height you want, you can come up with (x = <25% of width>, y = <25% of width>) and scale up appropriately when processing the generated diagram.) 

We then generate the diagram.

```Python
from src.voronout import VoronoiDiagram
voronoiDiagram = VoronoiDiagram(basePoints = basePoints)
```

From there, we can either process the info ourselves..

```Python
for voronoiRegion in voronoiDiagram.voronoiRegions.values():
    for voronoiRegionEdge in voronoiRegion.edges:
        # Do whatever you want with the borders of the region..
```

.. or write it out as JSON for something else to process:

```Python
from src.voronout import toJson
toJson(voronoiDiagram = voronoiDiagram, voronoiJsonPath = "voronoi.json")
```

# Example!