from typing import Any, Dict, Optional

from manim import Animation, Mobject

from .arc import Arc, ArcScale
from .circle import Circle, CircleScale


class Scale(Animation):
    """An animation that scales a circular object.

    Examples
    --------
    .. manim:: ScaleExample

        from hmanim.native import Circle, Dot, Point, Scale

        class ScaleExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)
                self.add(plane)

                # Draw a circle.
                center = Point(3.0, 0.0)
                circle = Circle(
                    center=center,
                    radius=4.0,
                    plane=plane,
                    color=YELLOW,
                )
                self.add(circle)

                # Mark the circle center.
                dot = Dot(center, plane=plane)
                self.add(dot)

                # Scale the circle by a factor of 1.5.
                self.play(Scale(circle, 1.5))

    """

    def __new__(
        cls,
        mobject: "Mobject",
        factor: float,
        run_time=3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Animation:
        if isinstance(mobject, Circle):
            return CircleScale(
                mobject, factor, run_time, apply_function_kwargs, **kwargs
            )
        elif isinstance(mobject, Arc):
            return ArcScale(
                mobject, factor, run_time, apply_function_kwargs, **kwargs
            )
        else:
            raise TypeError("Scale only works on Circles and Arcs.")
