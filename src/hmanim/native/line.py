from __future__ import annotations

from manim import PolarPlane

from .point import Point
from .polygonal_chain import PolygonalChain


class Line(PolygonalChain):
    """A geodesic line segment between two :class:`Point` objects.

    Examples
    --------

    .. manim:: LineExample
        :save_last_frame:

        from hmanim.native import Line, Point

        class LineExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)
                self.add(plane)

                line = Line(
                    Point(3, 0),
                    Point(3, TAU / 8),
                    plane=plane,
                    color=YELLOW,
                )
                self.add(line)

    """

    def __init__(
        self,
        start_point: Point,
        end_point: Point,
        plane: PolarPlane,
        using_geodesic: bool = True,
        **kwargs,
    ):
        self.using_geodesic = using_geodesic

        super().__init__(
            *[start_point, end_point],
            plane=plane,
            using_geodesic=self.using_geodesic,
            **kwargs,
        )

    def copy(self) -> Line:
        return Line(
            start_point=self.get_start().copy(),
            end_point=self.get_end().copy(),
            plane=self.plane,
            using_geodesic=self.using_geodesic,
        ).match_style(self)

    def move_to(self, start_point: Point, end_point: Point) -> Line:
        self.set_native_anchors([start_point, end_point])
        return self

    def translated_by(self, distance: float) -> Line:
        self.set_native_anchors(
            [p.copy().translated_by(distance) for p in self.native_anchors]
        )
        return self

    def rotated_by(self, angle: float) -> Line:
        self.set_native_anchors(
            [p.copy().rotated_by(angle) for p in self.native_anchors]
        )
        return self

    def get_start(self) -> Point:
        return self.native_anchors[0]

    def get_end(self) -> Point:
        return self.native_anchors[1]
