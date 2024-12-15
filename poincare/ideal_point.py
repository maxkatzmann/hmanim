from __future__ import annotations

import math

from .point import Point


class IdealPoint(Point):
    """A point with infinite distance to the origin, lying on the boundary of
    the disk.

    Examples
    --------
    .. manim:: IdealPointExample
        :save_last_frame:

        from hmanim.poincare import Disk, Dot, IdealPoint

        class IdealPointExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                ideal_point = IdealPoint(TAU / 4)
                ideal_dot = Dot(
                    ideal_point,
                    disk=disk,
                    color=BLUE,
                )
                self.add(ideal_dot)
    """

    def __init__(self, angle: float):
        x = IdealPoint.get_x_from_angle(angle)
        y = IdealPoint.get_y_from_angle(angle)

        super().__init__(x, y)  # type: ignore

    @staticmethod
    def get_x_from_angle(angle: float):
        return math.cos(angle)

    @staticmethod
    def get_y_from_angle(angle: float):
        return math.sin(angle)
