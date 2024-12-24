from __future__ import annotations

from typing import Any, Dict, Optional, Sequence

from manim import Animation, PolarPlane

from .point import Point
from .vmobject import VMobject


class PolygonalChain(VMobject):
    """
    A path of :class:`hmanim.poincare.point.Point` objects
    where two consecutive points are connected by the
    geodesic line segment between them.

    Examples
    --------
    .. manim:: PolygonalChainExample
        :save_last_frame:

        from hmanim.native import Point, PolygonalChain

        class PolygonalChainExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the polygonal chain.
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

    See Also
    --------
        :class:`Polygon` for a :class:`PolygonalChain` with
        the added geodesic line segment between the last and
        the first :class:`hmanim.poincare.point.Point`.
    """

    def __init__(
        self,
        *native_anchors: Point,
        plane: PolarPlane,
        using_geodesic: bool = True,
        **kwargs,
    ):
        self.using_geodesic = using_geodesic
        super().__init__(plane=plane, **kwargs)

        self.set_native_anchors(native_anchors)

    def set_native_anchors(self, native_anchors: Sequence[Point]):
        """ 
        Change the corner
        :class:`hmanim.poincare.point.Point` objects that
        make up the polygonal chain.

        Args:
            native_anchors (Sequence[hmanim.native.point.Point]): The new corners.
        """
        self.native_anchors = native_anchors

        self.clear_native_points()

        for anchor in self.native_anchors:
            self.connect_native_point(
                anchor, using_geodesic=self.using_geodesic
            )

    def copy(self) -> PolygonalChain:
        return PolygonalChain(
            *[p.copy() for p in self.native_anchors],
            plane=self.plane,
            using_geodesic=self.using_geodesic,
        ).match_style(self)

    def translated_by(self, distance: float) -> PolygonalChain:
        """Translate the polygonal chain by a given `distance`. See
        :meth:`Point.translated_by` for more details.

        Args:
            distance (float): The distance to translate by.

        Returns:
            PolygonalChain: The translated polygonal chain.
        """
        self.set_native_anchors(
            [p.copy().translated_by(distance) for p in self.native_anchors]
        )
        return self

    def rotated_by(self, angle: float) -> PolygonalChain:
        """Rotate the polygonal chain around the origin by a given `angle` in
        radians.

        Args:
            angle (float): The angle to rotate by.

        Returns:
            PolygonalChain: The rotated polygonal chain.
        """
        self.set_native_anchors(
            [p.copy().rotated_by(angle) for p in self.native_anchors]
        )
        return self

    def set_curvature(self, curvature: float) -> PolygonalChain:
        """Set the `curvature` of the hyperbolic plane that the polygonal chain
        lives in.

        Args:
            curvature (float): The new (negative) curvature.

        Note:
            Affects only the polygonal chain object itself and not the other
            objects associated with the corresponding hyperbolic plane.

        Returns:
            PolygonalChain: The polygonal chain with the new curvature.
        """
        super().set_curvature(curvature)

        self.set_native_anchors(self.native_anchors)
        return self

    def set_center_of_projection(self, point: Point) -> PolygonalChain:
        """Set the center of projection of the polygonal chain.

        Args:
            point (hmanim.native.point.Point): The new center of projection.

        Returns:
            PolygonalChain: The polygonal chain with the new center of projection.
        """
        moved_anchors = [
            p.copy().set_center_of_projection(point)
            for p in self.native_anchors
        ]
        self.set_native_anchors(moved_anchors)
        return self


class PolygonalChainTranslate(Animation):
    """Translate a polygonal chain horizontally by a given distance.

    Examples
    --------
    .. manim:: PolygonalChainTranslateExample

        from hmanim.native import Point, PolygonalChain, PolygonalChainTranslate

        class PolygonalChainTranslateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the polygonal chain.
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

                # Translate the polygonal chain.
                self.play(
                    PolygonalChainTranslate(
                        chain,
                        distance=3
                    )
                )

    """

    def __init__(
        self,
        polygonal_chain: PolygonalChain,
        distance: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.distance = distance
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(polygonal_chain, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # The current distance we are translating.
        translation_distance = self.rate_func(alpha) * self.distance

        # The translated mobject.  We need to create copies, since we don't
        # want to modify the start_mobject.
        translated_mobject = self.starting_mobject.copy().translated_by(
            translation_distance
        )

        # Update the points of the mobject to match the ones of the
        # translated_mobject.
        self.mobject.set_native_anchors(translated_mobject.native_anchors)


class PolygonalChainRotate(Animation):
    """Rotate a polygonal chain around the origin by a given angle.

    Examples
    --------
    .. manim:: PolygonalChainRotateExample

        from hmanim.native import Point, PolygonalChain, PolygonalChainRotate

        class PolygonalChainRotateExample(Scene):
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

                # Translate the circle
                self.play(
                    PolygonalChainRotate(
                        chain,
                        angle=TAU / 4,
                    )
                )

    """

    def __init__(
        self,
        polygonal_chain: PolygonalChain,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """Animate changing the curvature of the polygon."""
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(polygonal_chain, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # The current angle we are rotating.
        rotation_angle = self.rate_func(alpha) * self.angle

        # The rotated mobject.  We need to create copies, since we don't want
        # to modify the start_mobject.
        rotated_mobject = self.starting_mobject.copy().rotated_by(
            rotation_angle
        )

        # Update the points of the mobject to match the ones of the
        # rotated_mobject.
        self.mobject.set_native_anchors(rotated_mobject.native_anchors)
