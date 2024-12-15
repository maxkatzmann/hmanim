from __future__ import annotations

import math
from typing import Sequence

import numpy as np
from manim import PI, Circle, line_intersection, perpendicular_bisector

from .ideal_point import IdealPoint
from .point import Point


class Disk(Circle):
    """The Poincaré disk in which other hyperbolic objects live.

    Examples
    --------
    .. manim:: DiskExample
        :save_last_frame:

        from hmanim.poincare import Disk, Point

        class DiskExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)
    """

    def point_by_inverting(self, p: Point) -> Point:
        """Invert a class:`hmanim.poincare.point.Point` in the disk.

        Note
        ----
            For more information on the inversion, see
            https://en.wikipedia.org/wiki/Inversive_geometry#Inversion_in_a_circle.

        Parameters
            point (hmanim.poincare.point.Point): The point to invert.

        Returns
            The inverted point.

        Examples
        --------

        .. manim:: DiskPointInversionExample
            :save_last_frame:

            from hmanim.poincare import Disk, Dot, Point

            class DiskPointInversionExample(Scene):
                def construct(self):
                    disk = Disk(radius=3, color=WHITE)
                    self.add(disk)

                    point = Point(0.5, 0.25)
                    inverted = disk.point_by_inverting(point)
                    self.add(
                        Dot(
                            point,
                            disk=disk,
                            color=BLUE,
                        ),
                        Dot(
                            inverted,
                            disk=disk,
                            color=RED,
                        ),
                    )

        """
        x = p.get_x()
        y = p.get_y()
        xPrime = x / ((x * x) + (y * y))
        yPrime = y / ((x * x) + (y * y))

        return Point(xPrime, yPrime)  # type: ignore

    def scaled_point(self, p: Point) -> np.ndarray:
        """Used to convert a point from within unit disk (as is used to
        represent the Poincaré disk) to the scaled version that we use for
        drawing.  Essentially, this allows us to draw the Poincaré (unit) disk
        as a disk of arbitrary radius on the canvas.

        Args:
            p (hmanim.poincare.point.Point): The point to scale.

        Returns:
            np.ndarray: The coordinates of the scaled point.
        """
        return p.coordinates * self.radius + self.get_center()

    def point_from_scaled(self, coordinates: Sequence[float]) -> Point:
        """The inverse of the :meth:`scaled_point` method. Converts a point from
        the canvas to the unit disk.

        Args:
            coordinates (Sequence[float]): The coordinates of the point which we
            want to convert back to a point within the unit disk.

        Returns:
            hmanim.poincare.point.Point: The point within the unit disk.
        """
        scaled = (coordinates - self.get_center()) / self.radius  # type: ignore
        return Point(scaled[0], scaled[1])

    @staticmethod
    def circle_intersect(
        c0: np.ndarray, r0: float, c1: np.ndarray, r1: float
    ) -> tuple[np.ndarray, np.ndarray] | None:
        """Finds the intersection of two circles.

        Args:
            c0 (np.ndarray): The center of the first circle.
            r0 (float): The radius of the first circle.
            c1 (np.ndarray): The center of the second circle.
            r1 (float): The radius of the second circle.

        Returns:
            tuple[np.ndarray, np.ndarray] | None: The coordinates of the
            intersection points. If there are no intersection points, then
            `None` is returned.

        Examples
        --------

        .. manim:: CircleIntersectionExample
            :save_last_frame:

            from hmanim.poincare import Disk, Point

            class CircleIntersectionExample(Scene):
                def construct(self):
                    circle1 = Circle(radius=3, color=WHITE)
                    circle2 = Circle(radius=2, color=WHITE).move_to(np.array([1, 1, 0]))
                    self.add(circle1, circle2)

                    intersections = Disk.circle_intersect(
                        circle1.get_center(),
                        circle1.radius,
                        circle2.get_center(),
                        circle2.radius,
                    )

                    if intersections is not None:
                        self.add(
                            Dot(intersections[0], color=RED),
                            Dot(intersections[1], color=RED),
                        )
        """
        d = np.linalg.norm(c0 - c1)

        if d > r0 + r1:
            return None

        if d < abs(r0 - r1):
            return None

        if d == 0 and r0 == r1:
            return None

        a = (r0**2 - r1**2 + d**2) / (2 * d)
        h = math.sqrt(r0**2 - a**2)

        x0 = c0[0]
        y0 = c0[1]

        x1 = c1[0]
        y1 = c1[1]

        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d

        i1x = x2 + h * (y1 - y0) / d
        i1y = y2 - h * (x1 - x0) / d

        i2x = x2 - h * (y1 - y0) / d
        i2y = y2 + h * (x1 - x0) / d

        return (np.array([i1x, i1y, 0]), np.array([i2x, i2y, 0]))

    def coordinates_of_geodesic_circle_through_ideal(
        self, p1: IdealPoint, p2: IdealPoint
    ) -> tuple[np.ndarray, float, bool] | None:
        """Determines the coordinates of the circle that passes through the
        ideal points `p1` and `p2`. The part of the corresponding circle that
        lies in the inside of the disk represents the geodesic line between the
        two points.

        Args:
            p1 (IdealPoint): The first ideal point.
            p2 (IdealPoint): The second ideal point.

        Returns:
            tuple[np.ndarray, float, bool] | None: The coordinates of the center
            of the circle, the radius of the circle, and a boolean indicating
            whether the circle center lies within the disk.

        Examples
        --------

        .. manim:: IdealGeodesicCircleExample
            :save_last_frame:

            from hmanim.poincare import Disk, Dot, IdealPoint

            class IdealGeodesicCircleExample(Scene):
                def construct(self):
                    disk = Disk(
                        radius=3,
                        color=WHITE,
                    )
                    self.add(disk)

                    p1 = IdealPoint(angle=0)
                    p2 = IdealPoint(angle=TAU / 8)

                    center, radius, in_disk = disk.coordinates_of_geodesic_circle_through_ideal(
                        p1, p2
                    )

                    circle = Circle(
                        radius=radius,
                        color=BLUE,
                    ).move_to(center)

                    self.add(
                        circle,
                        Dot(
                            p1,
                            disk=disk,
                            color=RED,
                        ),
                        Dot(
                            p2,
                            disk=disk,
                            color=RED,
                        ),
                    )

        """
        a1 = p1.get_angle()
        a2 = p2.get_angle()

        angle_half = (a2 - a1) / 2
        angle_between = a1 + angle_half

        alpha = abs(angle_half)
        gamma = PI / 2 - alpha

        scaled_center = np.array([0, 0, 0]) + self.get_center()
        scaled_radius = 0

        try:
            d = self.radius / math.sin(gamma)
            scaled_center = np.array(
                [d * math.cos(angle_between), d * math.sin(angle_between), 0] + self.get_center()
            )
            scaled_radius = np.linalg.norm(
                self.scaled_point(p1) - scaled_center
            )
        except:
            pass

        return scaled_center, scaled_radius, True  # type: ignore

    def coordinates_of_geodesic_circle_through(
        self, p1: Point | IdealPoint, p2: Point | IdealPoint
    ) -> tuple[np.ndarray, float, bool] | None:
        """Determines the coordinates of the circle that passes through the
        (potentially ideal) points `p1` and `p2`. The part of the corresponding
        circle that lies in the inside of the disk represents the geodesic line
        segment between the two points.

        Args:
            p1 (hmanim.poincare.point.Point | IdealPoint): The first point.
            p2 (hmanim.poincare.point.Point | IdealPoint): The second point.

        Returns:
            tuple[np.ndarray, float, bool] | None: The coordinates of the center
            of the circle, the radius of the circle, and a boolean indicating
            whether the circle center lies within the disk.

        Examples
        --------

        .. manim:: GeodesicCircleExample
            :save_last_frame:

            from hmanim.poincare import Disk, Dot, Point

            class GeodesicCircleExample(Scene):
                def construct(self):
                    disk = Disk(
                        radius=3,
                        color=WHITE,
                    )
                    self.add(disk)

                    p1 = Point(0.75, 0.0)
                    p2 = Point(0.66, 0.25)

                    center, radius, in_disk = disk.coordinates_of_geodesic_circle_through(
                        p1, p2
                    )

                    circle = Circle(
                        radius=radius,
                        color=BLUE,
                    ).move_to(center)

                    self.add(
                        circle,
                        Dot(
                            p1,
                            disk=disk,
                            color=RED,
                        ),
                        Dot(
                            p2,
                            disk=disk,
                            color=RED,
                        ),
                    )
        """
        if isinstance(p1, IdealPoint) and isinstance(p2, IdealPoint):
            return self.coordinates_of_geodesic_circle_through_ideal(p1, p2)
        elif isinstance(p1, IdealPoint):
            temp = p2.copy()
            p2 = p1.copy()
            p1 = temp

        p3 = self.point_by_inverting(p1)
        try:
            pd1 = self.scaled_point(p1)
            pd2 = self.scaled_point(p2)
            pd3 = self.scaled_point(p3)

            intersection = line_intersection(
                perpendicular_bisector([p1.coordinates, p2.coordinates]),
                perpendicular_bisector([p2.coordinates, p3.coordinates]),
            )
            center = Point(intersection[0], intersection[1])
            radius = np.linalg.norm(p1.coordinates - intersection)

            # Scale to match disk
            scaled_center = center.coordinates * self.radius + self.get_center()
            scaled_radius = radius * self.radius

            return scaled_center, scaled_radius, True  # type: ignore
        except:
            return None
