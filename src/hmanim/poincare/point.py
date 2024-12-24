from __future__ import annotations

import math
from typing import Sequence

import numpy as np


class Point:
    """A point in the Poincaré disk, identified by its Cartesian coordinates.

    Examples
    --------
    .. manim:: PointExample
        :save_last_frame:

        from hmanim.poincare import Disk, Dot, Point

        class PointExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                # Denote the distance in x-direction.
                x_label = LabeledLine(
                    label = "0.6",
                    start=disk.scaled_point(Point()),
                    end=disk.scaled_point(Point(0.6, 0.0)),
                )
                self.add(x_label)

                # Denote the distance in y-direction.
                y_label = LabeledLine(
                    label = "0.3",
                    start=disk.scaled_point(Point(0.6, 0.0)),
                    end=disk.scaled_point(Point(0.6, 0.3)),
                )
                self.add(y_label)

                # The corresponding point.
                point = Point(0.6, 0.3)

                dot = Dot(
                    point,
                    disk=disk,
                    color=BLUE,
                )
                self.add(dot)

    """

    def __init__(self, *coordinates: Sequence[float]):
        # Make sure we have the right format
        self.coordinates = np.pad(list(coordinates), (0, 3), "constant")[:3]

    def get_x(self) -> float:
        """The x-coordinate of the point.

        Returns:
            float: The x-coordinate of the point.
        """
        return self.coordinates[0]

    def get_y(self) -> float:
        """The y-coordinate of the point.

        Returns:
            float: The y-coordinate of the point.
        """
        return self.coordinates[1]

    def __repr__(self):
        return f"Point({self.get_x()}, {self.get_y()})"

    def copy(self) -> Point:
        """Create a copy of the point.

        Returns:
            hmanim.poincare.point.Point: A copy of the point.
        """
        return Point(*self.coordinates)

    def translated_by(self, distance: float) -> Point:
        """Translate the point by the given `distance` in positive x-direction.
        A negative distance will translate the point in the negative
        x-direction.

        Args:
            distance (float): The distance to translate the point by.

        Returns:
            hmanim.poincare.point.Point: The translated point.

        Examples
        --------
        .. manim:: PointTranslatedByExample
            :save_last_frame:

            from hmanim.poincare import Disk, Dot, Point

            class PointTranslatedByExample(Scene):
                def construct(self):
                    disk = Disk(
                        radius=3,
                        color=WHITE,
                    )
                    self.add(disk)

                    # The point to be translated.
                    point = Point(-0.75, 0.25)
                    dot = Dot(
                        point,
                        disk=disk,
                        color=RED,
                    )
                    self.add(dot)

                    for i in range(1, 5):
                        dot = Dot(
                            point.copy().translated_by(i),
                            disk=disk,
                            color=BLUE,
                        )
                        self.add(dot)
        """
        z = complex(self.get_x(), self.get_y())
        zPrime = ((math.exp(distance) + 1) * z + math.exp(distance) - 1) / (
            (math.exp(distance) - 1) * z + math.exp(distance) + 1
        )
        self.coordinates = np.array([zPrime.real, zPrime.imag, 0.0])
        return self

    def rotated_by(self, angle: float) -> Point:
        """Rotate the point by the given `angle` in radians around the origin.

        Args:
            angle (float): The angle to rotate the point by.

        Returns:
            hmanim.poincare.point.Point: The rotated point.

        Examples
        --------
        .. manim:: PointRotatedByExample
            :save_last_frame:

            from hmanim.poincare import Disk, Dot, Point

            class PointRotatedByExample(Scene):
                def construct(self):
                    disk = Disk(
                        radius=3,
                        color=WHITE,
                    )
                    self.add(disk)

                    # The point to be rotated.
                    point = Point(0.75, 0.0)
                    dot = Dot(
                        point,
                        disk=disk,
                        color=RED,
                    )
                    self.add(dot)

                    for i in range(1, 5):
                        dot = Dot(
                            point.copy().rotated_by(i * TAU / 8),
                            disk=disk,
                            color=BLUE,
                        )
                        self.add(dot)
        """
        angle_half = angle / 2.0
        z = complex(self.get_x(), self.get_y())
        zPrime = (
            complex(math.cos(angle_half), math.sin(angle_half)) * z
        ) / complex(math.cos(angle_half), -math.sin(angle_half))
        self.coordinates = np.array([zPrime.real, zPrime.imag, 0.0])
        return self

    def get_angle(self) -> float:
        """Get the angle in radians by which the point is rotated away from the
        origin.

        Returns:
            float: The angle in radians.

        Examples
        --------
        .. manim:: PointGetAngleExample
            :save_last_frame:

            from hmanim.poincare import Disk, Dot, IdealPoint, Point

            class PointGetAngleExample(Scene):
                def construct(self):
                    disk = Disk(
                        radius=3,
                        color=WHITE,
                    )
                    self.add(disk)

                    origin = Point()
                    origin_dot = Dot(
                        origin,
                        disk=disk,
                        color=WHITE,
                    )
                    self.add(origin_dot)

                    point = Point(0.4, 0.2)
                    dot = Dot(
                        point,
                        disk=disk,
                        color=BLUE,
                    )
                    self.add(dot)

                    ideal_point = IdealPoint(point.get_angle())
                    ideal_dot = Dot(
                        ideal_point,
                        disk=disk,
                        color=RED,
                    )
                    self.add(ideal_dot)
        """
        return math.atan2(self.get_y(), self.get_x())

    def is_ideal(self) -> bool:
        """Check if the point is an ideal point.

        Returns:
            bool: `True` if the point is an ideal point, `False` otherwise.
        """
        return np.linalg.norm(self.coordinates) == 1

    def is_origin(self) -> bool:
        """Check if the point is the origin.

        Returns:
            bool: `True` if the point is the origin, `False` otherwise.
        """
        return np.all(self.coordinates == 0)  # type: ignore
