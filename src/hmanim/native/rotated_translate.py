from typing import Any, Dict, Optional

from manim import Animation

from .circle import Circle, CircleRotatedTranslate
from .dot import Dot, DotRotatedTranslate
from .vmobject import VMobject, VMobjectRotatedTranslate


class RotatedTranslate(Animation):
    """An animation that translates a :class:`VMobject` along an axis that is
    rotated away from the x-axis.

    Examples
    --------
    .. manim:: RotatedTranslateExample

        from hmanim.native import Circle, Dot, Point, RotatedTranslate

        class RotatedTranslateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw a circle.
                center = Point(0.0, 0.0)
                circle = Circle(
                    center=center,
                    radius=5.0,
                    plane=plane,
                )
                self.add(circle)

                # Draw the circle center.
                dot = Dot(center, plane=plane)
                self.add(dot)

                # Translate both the circle and the circle center.
                distance = 3.0
                angle = TAU / 8
                self.play(
                    RotatedTranslate(
                        circle,
                        distance=distance,
                        angle=angle,
                    ),
                    RotatedTranslate(
                        dot,
                        distance=distance,
                        angle=angle,
                    ),
                )
    """

    def __new__(
        cls,
        mobject: VMobject,
        distance: float,
        angle: float,
        run_time=3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Animation:
        if isinstance(mobject, Circle):
            return CircleRotatedTranslate(
                mobject,
                distance,
                angle,
                run_time,
                apply_function_kwargs,
                **kwargs
            )
        elif isinstance(mobject, VMobject):
            return VMobjectRotatedTranslate(
                mobject,
                distance,
                angle,
                run_time,
                apply_function_kwargs,
                **kwargs
            )
        elif isinstance(mobject, Dot):
            return DotRotatedTranslate(
                mobject,
                distance,
                angle,
                run_time,
                apply_function_kwargs,
                **kwargs
            )
        else:
            raise TypeError(
                "RotatedTranslate only works on Circles, Dots, and VMobject."
            )
