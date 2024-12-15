from typing import Any, Dict, Optional

from manim import Animation, Mobject

from .circle import Circle, CircleTranslate
from .dot import Dot, DotTranslate
from .polygonal_chain import PolygonalChain, PolygonalChainTranslate
from .vmobject import VMobject, VMobjectTranslate


class Translate(Animation):
    """
    This translation represents a movement of a point from the origin along the
    x-axis by a specified distance.  All other points in the plane, in
    particular the passed :class:`Mobject`, are moved in such a way, that the
    distance to the moving point remain unchanged.

    Examples
    --------
    .. manim:: TranslateExample

        from hmanim.native import Circle, Point, Translate

        class TranslateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw a circle.
                circle = Circle(
                    center=Point(0.0, 0.0),
                    radius=5.0,
                    plane=plane,
                )
                self.add(circle)

                # Translate the circle horizontally by 3.
                self.play(Translate(circle, 3.0))
    """

    def __new__(
        cls,
        mobject: "Mobject",
        distance: float,
        run_time=3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Animation:
        if isinstance(mobject, Circle):
            return CircleTranslate(
                mobject, distance, run_time, apply_function_kwargs, **kwargs
            )
        if isinstance(mobject, PolygonalChain):
            return PolygonalChainTranslate(
                mobject, distance, run_time, apply_function_kwargs, **kwargs
            )
        elif isinstance(mobject, Dot):
            return DotTranslate(
                mobject, distance, run_time, apply_function_kwargs, **kwargs
            )
        elif isinstance(mobject, VMobject):
            return VMobjectTranslate(
                mobject, distance, run_time, apply_function_kwargs, **kwargs
            )
        else:
            raise TypeError(
                "Translate only works on Circles, Dots, PolygonalChains, and VMobjects and their subclasses."
            )
