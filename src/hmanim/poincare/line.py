from __future__ import annotations

import math
from typing import Any, Dict, Optional

import numpy as np
from manim import PI, Animation, Arc
from manim import Line as MLine
from manim import VMobject

from .disk import Disk
from .point import Point


class Line(VMobject):
    """The Poincaré disk equivalent to Manim's `Line`. Lines are actually line
    segments that follow the geodesic between two points.

    Examples
    --------
    .. manim:: LineExample
        :save_last_frame:

        from hmanim.poincare import Disk, Line, IdealPoint, Point

        class LineExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                line = Line(
                    Point(-0.75, 0.0),
                    Point(-0.25, 0.5),
                    disk=disk,
                    color=BLUE,
                )
                self.add(line)

                ideal_line = Line(
                    IdealPoint(angle=0),
                    IdealPoint(angle=TAU / 4),
                    disk=disk,
                    color=RED,
                )
                self.add(ideal_line)
    """

    def __init__(self, p1: Point, p2: Point, disk: Disk, **kwargs):
        self.disk = disk
        self.kwargs = kwargs
        self.is_arc = True

        super().__init__(**kwargs)

        # Set points after potential styling using kwargs.
        self._set_unit_points(p1, p2)

    def _set_unit_points(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

        self.update_parameters()

    def update_parameters(self):
        circle_coords = self.disk.coordinates_of_geodesic_circle_through(
            self.p1, self.p2
        )

        assert circle_coords is not None
        c, r, is_circle = circle_coords

        if not is_circle or self.p1.is_origin() or self.p2.is_origin():
            scaled_p1 = self.disk.scaled_point(self.p1)
            scaled_p2 = self.disk.scaled_point(self.p2)
            self.become(
                MLine(scaled_p1, scaled_p2, **self.kwargs).match_style(self)
            )
            self.is_arc = False
            return

        p1Scaled = self.disk.scaled_point(self.p1)
        p2Scaled = self.disk.scaled_point(self.p2)

        angle1 = self._angle_relative_to_center(p1Scaled, c)
        angle2 = self._angle_relative_to_center(p2Scaled, c)

        self.start_angle = angle1
        self.angle = angle2 - angle1

        if self.angle > PI:
            self.angle = -((2 * PI) - self.angle)
        elif self.angle < -PI:
            self.angle = (2 * PI) + self.angle

        self.radius = r
        self.center = c  # type: ignore
        arc = Arc(
            radius=self.radius, start_angle=self.start_angle, angle=self.angle
        ).shift(
            self.center  # type: ignore
        )
        self.become(arc.match_style(self))
        self.is_arc = True

    def _angle_relative_to_center(
        self, p: np.ndarray, center: np.ndarray
    ) -> float:
        x = p[0] - center[0]
        y = p[1] - center[1]

        angle = math.atan2(y, x)
        return angle

    def move_to(self, p1: Point, p2: Point) -> Line:
        """Move the line to new end points.

        Args:
            p1 (hmanim.poincare.point.Point): The new start point.
            p2 (hmanim.poincare.point.Point): The new end point.

        Returns:
            Line: The line with the new end points.

        Examples
        --------
        .. manim:: LineMoveToExample

            from hmanim.poincare import Disk, Line, Point

            class LineMoveToExample(Scene):
                def construct(self):
                    disk = Disk(
                        radius=3,
                        color=WHITE,
                    )
                    self.add(disk)

                    line = Line(
                        Point(-0.75, 0.0),
                        Point(-0.25, 0.5),
                        disk=disk,
                        color=BLUE,
                    )
                    self.add(line)

                    self.play(line.animate(run_time=3).move_to(
                        Point(0.75, 0.0),
                        Point(0.25, 0.5),
                    ))

        """
        self._set_unit_points(p1, p2)
        return self

    def translated_by(self, distance: float) -> Line:
        """Translate the line by the passed `distance` in positive direction
        parallel to the x-axis. A negative `distance` translates the line
        in negative x-direction.

        Args:
            distance (float): The distance to translate the line by.

        Returns:
            Line: The translated line.

        """
        self._set_unit_points(
            self.p1.translated_by(distance), self.p2.translated_by(distance)
        )

        return self

    def copy(self) -> Line:
        """Create a copy of the line.

        Returns:
            Line: The copy of the line.
        """
        return Line(self.p1, self.p2, self.disk).match_style(self)


class LineTranslate(Animation):
    """A 'translation' of both endpoints along the x-axis by the passed
    `distance`.

    Examples
    --------

    .. manim:: LineTranslateExample

        from hmanim.poincare import Disk, Line, LineTranslate, Point

        class LineTranslateExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                line = Line(
                    Point(-0.75, 0.0),
                    Point(-0.25, 0.5),
                    disk=disk,
                    color=BLUE,
                )
                self.add(line)

                self.play(LineTranslate(line, 3))

    """

    def __init__(
        self,
        line: Line,
        distance: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        """A 'translation along' along the x-axis by the passed `distance`."""
        self.distance = distance
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(line, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        # We animate a translation by creating circles at the intermediate
        # positions.

        # The current distance we are translating.
        current_translation_distance = self.rate_func(alpha) * self.distance

        # The new points.
        p1 = self.starting_mobject.p1.copy().translated_by(  # type: ignore
            current_translation_distance
        )
        p2 = self.starting_mobject.p2.copy().translated_by(  # type: ignore
            current_translation_distance
        )

        # Actually moving the circle.
        self.mobject.move_to(p1, p2)


class LineRotate(Animation):
    """A rotation of the endpoints of the line around the origin by the passed
    `angle`.

    Examples
    --------

    .. manim:: LineRotateExample

        from hmanim.poincare import Disk, Line, LineRotate, Point

        class LineRotateExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                line = Line(
                    Point(-0.75, 0.0),
                    Point(-0.25, 0.5),
                    disk=disk,
                    color=BLUE,
                )
                self.add(line)

                self.play(LineRotate(line, TAU / 2))

    """

    def __init__(
        self,
        line: Line,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        """A rotation around the origin by the passed `angle`."""
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(line, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        # The current distance we are translating.
        current_rotation_angle = self.rate_func(alpha) * self.angle

        # The new points.
        p1 = self.starting_mobject.p1.copy().rotated_by(current_rotation_angle)  # type: ignore
        p2 = self.starting_mobject.p2.copy().rotated_by(current_rotation_angle)  # type: ignore

        # Actually moving the circle.
        self.mobject.move_to(p1, p2)
