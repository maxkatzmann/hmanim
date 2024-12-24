from typing import Any, Dict, Optional

from manim import Animation

from .circle import Circle, CircleTranslateAndRotate
from .dot import Dot, DotTranslateAndRotate
from .vmobject import VMobject, VMobjectTranslateAndRotate


class TranslateAndRotate(Animation):
    """An animation that translates a :class:`VMobject` along an axis that is
    simultaneously rotating.  In a sense, this is a wrapper class that
    automatically decides which animation to apply to a given object, without
    having to specify whether it should be a :class:`CircleTranslateAndRotate`,
    :class:`DotTranslateAndRotate`, etc.

    Note
    ----
        In contrast to a rotated translate (e.g.,
        :class:`CircleRotatedTranslate`), here the translation axis is rotated
        while the translation is happening.

    Examples
    --------
    .. manim:: TranslateAndRotateExample

        from hmanim.native import Circle, Dot, Point, TranslateAndRotate

        class TranslateAndRotateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)
                self.add(plane)

                # Draw a circle.
                center = Point(3.0, 0.0)
                circle = Circle(
                    center=center,
                    radius=5.0,
                    plane=plane,
                    color=YELLOW,
                )
                self.add(circle)

                # Draw the circle center.
                dot = Dot(
                    center,
                    plane=plane,
                    color=YELLOW,
                )
                self.add(dot)

                # Rotate both the circle and the circle center.
                distance = 3.0
                angle = TAU / 4
                self.play(
                    TranslateAndRotate(
                        circle,
                        distance=distance,
                        angle=angle
                    ),
                    TranslateAndRotate(
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
            return CircleTranslateAndRotate(
                mobject,
                distance,
                angle,
                run_time,
                apply_function_kwargs,
                **kwargs
            )
        elif isinstance(mobject, Dot):
            return DotTranslateAndRotate(
                mobject,
                distance,
                angle,
                run_time,
                apply_function_kwargs,
                **kwargs
            )
        elif isinstance(mobject, VMobject):
            return VMobjectTranslateAndRotate(
                mobject,
                distance,
                angle,
                run_time,
                apply_function_kwargs,
                **kwargs
            )
        else:
            raise TypeError(
                "TranslateAndRotate only works on Circles, Dots, and VMobject."
            )
