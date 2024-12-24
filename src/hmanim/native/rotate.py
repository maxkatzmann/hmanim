from typing import Any, Dict, Optional

from manim import Animation

from .circle import Circle, CircleRotate
from .closed_arc import ClosedArc, ClosedArcRotate
from .dot import Dot, DotRotate
from .polygonal_chain import PolygonalChain, PolygonalChainRotate
from .vmobject import VMobject, VMobjectRotate


class Rotate(Animation):
    """An animation that rotates a :class:`VMobject` around the origin by a
    given angle. In a sense, this is a wrapper class that automatically decides
    which rotation to apply to a given object, without having to specify whether
    it should be a :class:`CircleRotate`, :class:`DotRotate`,
    :class:`PolygonalChainRotate`, :class:`ClosedArcRotate`, etc.

    Examples
    --------
    .. manim:: RotateExample

        from hmanim.native import Circle, Dot, Point, Rotate

        class RotateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw a circle.
                center = Point(3.0, 0.0)
                circle = Circle(
                    center=center,
                    radius=5.0,
                    plane=plane,
                )
                self.add(circle)

                # Draw the circle center.
                dot = Dot(center, plane=plane)
                self.add(dot)

                # Rotate both the circle and the circle center.
                angle = TAU / 4
                self.play(
                    Rotate(circle, angle),
                    Rotate(dot, angle),
                )

    """

    def __new__(
        cls,
        mobject: VMobject,
        angle: float,
        run_time=3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Animation:
        if isinstance(mobject, Circle):
            return CircleRotate(
                mobject, angle, run_time, apply_function_kwargs, **kwargs
            )
        elif isinstance(mobject, Dot):
            return DotRotate(
                mobject, angle, run_time, apply_function_kwargs, **kwargs
            )
        elif isinstance(mobject, ClosedArc):
            return ClosedArcRotate(
                mobject, angle, run_time, apply_function_kwargs, **kwargs
            )
        elif isinstance(mobject, PolygonalChain):
            return PolygonalChainRotate(
                mobject, angle, run_time, apply_function_kwargs, **kwargs
            )
        elif isinstance(mobject, VMobject):
            return VMobjectRotate(
                mobject, angle, run_time, apply_function_kwargs, **kwargs
            )
        else:
            raise TypeError(
                "Rotate only works on Circles, ClosedArcs, Dots, "
                "PolygonalChains, VMobjects and their subclasses."
            )
