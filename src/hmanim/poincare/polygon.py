from __future__ import annotations

from typing import Any, Sequence

import numpy as np
from manim import Animation, Arc, Difference
from manim import Polygon as MPolygon
from manim import Union, VMobject

from .disk import Disk
from .line import Line
from .point import Point


class Polygon(VMobject):
    """The Poincaré disk equivalent to Manim's `Polygon`, connecting a sequence
    of points with geodesic lines.

    Examples
    --------
    .. manim:: PolygonExample
        :save_last_frame:

        from hmanim.poincare import Disk, Point, Polygon

        class PolygonExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                polygon = Polygon(
                    Point(-0.75, 0.0),
                    Point(0.0, 0.75),
                    Point(0.75, 0.0),
                    Point(0.0, -0.75),
                    disk=disk,
                    color=BLUE,
                )
                self.add(polygon)
    """

    def __init__(self, *points: Sequence[Point], disk: Disk, **kwargs):
        self.disk = disk
        self.kwargs = kwargs
        self.helpers = []

        super().__init__(**kwargs)
        self._set_unit_points(list(points))  # type: ignore

    def _update_parameters(self):
        polygon = MPolygon(
            *[self.disk.scaled_point(p) for p in self.unit_points],
            fill_opacity=1,
        )

        side_arcs = []

        for side in self.get_sides():
            if side.is_arc:
                side_arcs.append(
                    Arc(
                        radius=side.radius,
                        start_angle=side.start_angle,
                        angle=side.angle,
                    ).shift(
                        side.center  # type: ignore
                    )
                )
            else:
                side_arcs.append(side)

        add_arcs = []
        subtract_arcs = []

        # If an arc contains oder arcs, it should be added and not remove from
        # the shape.
        for i, arc in enumerate(side_arcs):
            if isinstance(arc, Line):
                continue

            arc_contains_other_arcs = False
            center = arc.get_center()
            radius = arc.get_radius()

            for j, arc2 in enumerate(side_arcs):
                if i == j or isinstance(arc2, Line):
                    continue

                center2 = arc2.get_center()
                radius2 = arc2.get_radius()

                dist = np.linalg.norm(center - center2)

                if dist + radius2 <= radius:
                    arc_contains_other_arcs = True
                    break

            if arc_contains_other_arcs:
                add_arcs.append(arc)
            else:
                subtract_arcs.append(arc)

        polygon_union = polygon

        if len(add_arcs) > 0:
            polygon_union = Union(polygon, *add_arcs)

        diff = polygon_union

        if len(subtract_arcs) > 0:
            subtract_union = subtract_arcs[0]

            if len(subtract_arcs) > 1:
                subtract_union = Union(*subtract_arcs)

            diff = Difference(polygon_union, subtract_union)

        self.become(diff.match_style(self))

    def translated_by(self, distance: float) -> Polygon:
        """Translates the polygon by the given distance in positive x-direction.
        A negative `distance` will translate the polygon in the negative
        x-direction.

        Args:
            distance (float): The distance to translate the polygon by.

        Returns:
            Polygon: The translated polygon.

        Examples
        --------

        .. manim:: PolygonTranslatedByExample
            :save_last_frame:

            from hmanim.poincare import Disk, Point, Polygon

            class PolygonTranslatedByExample(Scene):
                def construct(self):
                    disk = Disk(
                        radius=3,
                        color=WHITE,
                    )
                    self.add(disk)

                    polygon = Polygon(
                        Point(-0.75, 0.0),
                        Point(0.0, 0.75),
                        Point(0.75, 0.0),
                        Point(0.0, -0.75),
                        disk=disk,
                        color=BLUE,
                    ).translated_by(1.0)
                    self.add(polygon)

        """
        self._set_unit_points(
            [p.translated_by(distance) for p in self.unit_points.copy()]
        )
        return self

    def rotated_by(self, angle: float) -> Polygon:
        """Rotates the polygon by the given `angle` in radians around the
        origin.

        Args:
            angle (float): The angle to rotate the polygon by.

        Returns:
            Polygon: The rotated polygon.

        Examples
        --------
        .. manim:: PolygonRotatedByExample
            :save_last_frame:

            from hmanim.poincare import Disk, Point, Polygon

            class PolygonRotatedByExample(Scene):
                def construct(self):
                    disk = Disk(
                        radius=3,
                        color=WHITE,
                    )
                    self.add(disk)

                    polygon = Polygon(
                        Point(-0.75, 0.0),
                        Point(0.0, 0.75),
                        Point(0.75, 0.0),
                        Point(0.0, -0.75),
                        disk=disk,
                        color=BLUE,
                    ).rotated_by(TAU / 8)
                    self.add(polygon)
        """
        self._set_unit_points(
            [p.rotated_by(angle) for p in self.unit_points.copy()]
        )
        return self

    def _set_unit_points(self, points: Sequence[Point]):
        self.unit_points: list[Point] = list(points)
        self._update_parameters()

    def get_sides(self) -> list[Line]:
        """Returns a list of the lines representing sides of the polygon.

        Returns:
            list[hmanim.poincare.line.Line]: The lines representing the sides of
                the polygon.
        """
        cyclic_unit_points = np.append(
            self.unit_points, self.unit_points[:1], axis=0  # type: ignore
        )

        lines = []
        for first, second in zip(cyclic_unit_points, cyclic_unit_points[1:]):
            lines.append(Line(first, second, self.disk))

        return lines


class PolygonTranslate(Animation):
    """A 'translation' along the x-axis by the passed `distance`.

    Examples
    --------
    .. manim:: PolygonTranslateExample

        from hmanim.poincare import Disk, Point, Polygon, PolygonTranslate

        class PolygonTranslateExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                polygon = Polygon(
                    Point(-0.75, 0.0),
                    Point(0.0, 0.75),
                    Point(0.75, 0.0),
                    Point(0.0, -0.75),
                    disk=disk,
                    color=BLUE,
                )
                self.add(polygon)

                self.play(
                    PolygonTranslate(
                        polygon,
                        distance=1,
                        run_time=3,
                    ),
                )
    """

    def __init__(
        self,
        polygon: Polygon,
        distance: float,
        apply_function_kwargs: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        """A 'translation along' along the x-axis by the passed `distance`."""
        self.distance = distance
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(polygon, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        # The current distance we are translating.
        current_translation_distance = self.rate_func(alpha) * self.distance

        new = self.starting_mobject.copy().translated_by(
            current_translation_distance
        )
        self.mobject.become(new)


class PolygonRotate(Animation):
    """A rotation around the origin by the passed `angle`.

    Examples
    --------
    .. manim:: PolygonRotateExample

        from hmanim.poincare import Disk, Point, Polygon, PolygonRotate

        class PolygonRotateExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                polygon = Polygon(
                    Point(-0.75, 0.0),
                    Point(0.0, 0.75),
                    Point(0.75, 0.0),
                    Point(0.0, -0.75),
                    disk=disk,
                    color=BLUE,
                )
                self.add(polygon)

                self.play(
                    PolygonRotate(
                        polygon,
                        angle=TAU / 8,
                        run_time=3,
                    ),
                )
    """

    def __init__(
        self,
        polygon: Polygon,
        angle: float,
        apply_function_kwargs: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        """A rotation around the origin by the passed `angle`."""
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(polygon, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        # The current angle we are rotating.
        current_rotation_angle = self.rate_func(alpha) * self.angle

        new = self.starting_mobject.copy().rotated_by(current_rotation_angle)
        self.mobject.become(new)


class PolygonRotatedTranslate(Animation):
    """A 'translation' by the passed `distance` along an axis that is rotated
    away from the x-axis by the passed `angle`.

    Examples
    --------
    .. manim:: PolygonRotatedTranslateExample

        from hmanim.poincare import Disk, Point, Polygon, PolygonRotatedTranslate

        class PolygonRotatedTranslateExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                polygon = Polygon(
                    Point(-0.75, 0.0),
                    Point(0.0, 0.75),
                    Point(0.75, 0.0),
                    Point(0.0, -0.75),
                    disk=disk,
                    color=BLUE,
                )
                self.add(polygon)

                self.play(
                    PolygonRotatedTranslate(
                        polygon,
                        distance=1,
                        angle=TAU / 8,
                        run_time=3,
                    ),
                )
    """

    @staticmethod
    def target_mobject(
        polygon: Polygon, distance: float, angle: float
    ) -> Polygon:
        return (
            polygon.copy()
            .rotated_by(-angle)
            .translated_by(distance)
            .rotated_by(angle)
        )

    def __init__(
        self,
        polygon: Polygon,
        distance: float,
        angle: float,
        apply_function_kwargs: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        """A 'translation along' along the x-axis by the passed `distance`."""
        self.distance = distance
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(polygon, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        # The current distance we are translating.
        current_translation_distance = self.rate_func(alpha) * self.distance

        self.mobject.become(
            PolygonRotatedTranslate.target_mobject(
                self.starting_mobject, current_translation_distance, self.angle  # type: ignore
            )
        )
