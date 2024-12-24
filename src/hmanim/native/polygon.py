from __future__ import annotations

from .point import Point
from .polygonal_chain import PolygonalChain


class Polygon(PolygonalChain):
    """A polygon is a closed :class:`PolygonalChain`.

    Examples
    --------
    .. manim:: PolygonExample
        :save_last_frame:

        from hmanim.native import Point, Polygon

        class PolygonExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the polygon.
                polygon = Polygon(
                    *[
                        Point(3.0, 0.0),
                        Point(4.0, TAU / 4),
                        Point(2.0, TAU / 2),
                        Point(1.0, TAU * 3 / 4),
                    ],
                    plane=plane
                )
                self.add(polygon)
    """

    def __init__(self, *points: Point, plane, **kwargs):
        anchors = list(points)

        if len(anchors) > 0:
            anchors.append(anchors[0])
        super().__init__(*anchors, plane=plane, **kwargs)

    def copy(self) -> Polygon:
        return Polygon(
            *[p.copy() for p in self.native_anchors],
            plane=self.plane,
            using_geodesic=self.using_geodesic,
        ).match_style(self)
