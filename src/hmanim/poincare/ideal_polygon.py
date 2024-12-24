from __future__ import annotations

import math
from typing import Sequence

from manim import PI

from .disk import Disk
from .ideal_point import IdealPoint
from .polygon import Polygon


class IdealPolygon(Polygon):
    """A polygon whose corners are ideal points.

    Examples
    --------
    .. manim:: IdealPolygonExample
        :save_last_frame:

        from hmanim.poincare import Disk, IdealPolygon

        class IdealPolygonExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                sides = 5
                angles = [TAU * i / sides for i in range(sides)]
                ideal_polygon = IdealPolygon(
                    *angles,
                    disk=disk,
                    color=BLUE,
                )
                self.add(ideal_polygon)
    """

    def __init__(self, *angles: Sequence[float], disk: Disk, **kwargs):
        unit_points = [IdealPoint(angle) for angle in list(angles)]  # type: ignore

        super().__init__(*unit_points, disk=disk, **kwargs)  # type: ignore

    @staticmethod
    def ideal_length(k: int) -> float:
        """Defines the distance between the center of an :class:`IdealPolygon`
        and one of its sides.

        Args:
            k (int): The number of sides of the ideal polygon.

        Returns:
            float: The distance between the center of the ideal polygon and one of its sides.

        Examples
        --------
        .. manim:: IdealPolygonLengthExample
            :save_last_frame:

            from hmanim.poincare import Disk, IdealPolygon

            class IdealPolygonLengthExample(Scene):
                def construct(self):
                    disk = Disk(
                        radius=3,
                        color=WHITE,
                    )
                    self.add(disk)

                    sides = 5
                    angles = [TAU * i / sides for i in range(sides)]
                    ideal_polygon = IdealPolygon(
                        *angles,
                        disk=disk,
                        color=BLUE,
                    )
                    self.add(ideal_polygon)

                    length = IdealPolygon.ideal_length(sides)
                    translated_polygon = ideal_polygon.copy().translated_by(
                            2 * length
                        ).rotated_by(TAU / (2 * sides)).set_color(RED)
                    self.add(translated_polygon)
        """
        return 2 * math.atanh(
            math.sqrt(1 + math.tan(PI / k) ** 2) - math.tan(PI / k)
        )
