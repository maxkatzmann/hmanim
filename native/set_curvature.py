from typing import Any, Dict, Optional

from manim import Animation, Mobject

from .graph import Graph, GraphSetCurvature
from .vmobject import VMobject, VMobjectSetCurvature


class SetCurvature(Animation):
    """An animation that changes the curvature of the hyperbolic plane that an
    object lives in.

    Note
    ----
        Only affects the object but not the other objects associated with the
        corresponding hyperbolic plane.

    Examples
    --------
    .. manim:: SetCurvatureExample

        from hmanim.native import Circle, Point, PolygonalChain, SetCurvature

        class SetCurvatureExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the polygon.
                chain = PolygonalChain(
                    *[
                        Point(3.0, 0.0),
                        Point(4.0, TAU / 4),
                        Point(2.0, TAU / 2),
                        Point(1.0, TAU * 3 / 4),
                    ],
                    plane=plane
                )
                self.add(chain)

                # Draw the circle.
                circle = Circle(
                    center=Point(3.0, 0.0),
                    radius=5.0,
                    plane=plane,
                )
                self.add(circle)

                # Change the curvature
                target_curvature = -0.001
                self.play(
                    SetCurvature(
                        chain,
                        curvature=target_curvature,
                    ),
                    SetCurvature(
                        circle,
                        curvature=target_curvature,
                    )
                )


    """

    def __new__(
        cls,
        mobject: "Mobject",
        curvature: float,
        run_time=3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Animation:
        if isinstance(mobject, Graph):
            return GraphSetCurvature(
                mobject, curvature, run_time, apply_function_kwargs, **kwargs
            )
        elif isinstance(mobject, VMobject):
            return VMobjectSetCurvature(
                mobject, curvature, run_time, apply_function_kwargs, **kwargs
            )
        else:
            raise TypeError("SetCurvature only works on Graphs and VMobjects.")
