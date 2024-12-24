from __future__ import annotations

from typing import Any, Dict, Optional

from manim import Animation
from manim import Dot as MDot

from .disk import Disk
from .point import Point


class Dot(MDot):
    """The Poincaré disk equivalent to Manim's `Dot`.

    This is basically a convenience wrapper, that automatically handles scaling
    in the :class:`Disk` associated with the dot.

    Examples
    --------

    .. manim:: DotExample
        :save_last_frame:

        from hmanim.poincare import Disk, Dot, Point

        class DotExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                dot = Dot(
                    Point(0.75, 0.25),
                    disk=disk,
                    color=BLUE,
                )
                self.add(dot)
    """

    def __init__(self, p: Point, disk: Disk, **kwargs):
        self.disk = disk
        self.point_in_unit_disk = p
        super().__init__(
            self.disk.scaled_point(self.point_in_unit_disk), **kwargs
        )

    def move_to(self, p: Point):
        """Move the dot to the given :class:`hmanim.poincare.point.Point`.

        Args:
            p (hmanim.poincare.point.Point): The point to move the dot to.
        """
        self.point_in_unit_disk = p
        super().move_to(self.disk.scaled_point(self.point_in_unit_disk))


class DotTranslate(Animation):
    """An animation that translates a :class:`Dot` along the x-axis.

    Examples
    --------
    .. manim:: DotTranslateExample

        from hmanim.poincare import Disk, Dot, DotTranslate, Point

        class DotTranslateExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)
                dot = Dot(
                    Point(-0.75, 0.25),
                    disk=disk,
                    color=BLUE,
                )
                self.add(dot)

                self.play(DotTranslate(dot, 3))
    """

    def __init__(
        self,
        dot: Dot,
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

        super().__init__(dot, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        # We animate a translation by creating circles at the intermediate
        # positions.

        # The current distance we are translating.
        current_translation_distance = self.rate_func(alpha) * self.distance

        # The center of the new circle.
        new_center = self.starting_mobject.point_in_unit_disk.copy().translated_by(  # type: ignore
            current_translation_distance
        )

        # Actually moving the circle.
        self.mobject.move_to(new_center)


class DotRotate(Animation):
    """An animation that rotates a :class:`Dot` around the origin.

    Examples
    --------
    .. manim:: DotRotateExample

        from hmanim.poincare import Disk, Dot, DotRotate, Point

        class DotRotateExample(Scene):
            def construct(self):
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)
                dot = Dot(
                    Point(0.75, 0.0),
                    disk=disk,
                    color=BLUE,
                )
                self.add(dot)

                self.play(DotRotate(dot, TAU / 4))
    """

    def __init__(
        self,
        dot: Dot,
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

        super().__init__(dot, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        # The current angle we are rotating.
        current_rotation_angle = self.rate_func(alpha) * self.angle

        # The center of the new circle.
        new_center = self.starting_mobject.point_in_unit_disk.copy().rotated_by(  # type: ignore
            current_rotation_angle
        )

        # Actually moving the circle.
        self.mobject.move_to(new_center)
