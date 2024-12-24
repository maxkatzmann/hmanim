from __future__ import annotations

from math import sqrt
from typing import Any, Dict, Optional

from manim import TAU, Animation, PolarPlane

from .point import Point
from .polygon import Polygon


class Circle(Polygon):
    """A shape consisting of one closed loop of vertices that all have the same
    hyperbolic distance to a `center` point.

    Parameters
    ----------
    center
        A :class:`hmanim.poincare.point.Point` representing the center of the :class:`Circle`.
    radius
        A `float` representing the radius of the :class:`Circle`.
    plane
        The :class:`PolarPlane` in which the :class:`Circle` lives.
    kwargs
        Forwarded to the parent constructor.

    Examples
    --------
    .. manim:: CircleExample
        :save_last_frame:

        from hmanim.native import Circle, Point

        class CircleExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the circle.
                circle = Circle(
                    center=Point(3.0, TAU / 8),
                    radius=5.0,
                    plane=plane
                )
                self.add(circle)
    """

    # Defines how many points lie on the path that is used to represent the
    # boundary of the circle.
    Resolution = 160

    def __init__(
        self, center: Point, radius: float, plane: PolarPlane, *args, **kwargs
    ):
        self._center = center
        self.radius = radius

        super().__init__(plane=plane, using_geodesic=False, **kwargs)

        self.set_native_anchors(self.get_native_render_anchors())

    @property
    def center(self) -> Point:
        """
        The :class:`hmanim.poincare.point.Point` representing the center of the :class:`Circle`.
        """
        return self._center

    @center.setter
    def center(self, center: Point):
        self.set_center(center)

    def copy(self) -> Circle:
        return Circle(
            self.center,
            self.radius,
            plane=self.plane,
            curvature=self.curvature,
        ).match_style(self)

    def set_center(self, center: Point) -> Circle:
        """Change the `center` of the :class:`Circle`.

        Args:
            center (hmanim.native.point.Point): The new center of the :class:`Circle`.

        Returns:
            Circle: The updated :class:`Circle`.
        """
        self._center = center
        self.set_native_anchors(self.get_native_render_anchors())
        return self

    def set_radius(self, radius: float) -> Circle:
        """Change the `radius` of the :class:`Circle`.

        Args:
            radius (float): The new radius of the :class:`Circle`.

        Returns:
            Circle: The updated :class:`Circle`.
        """
        self.radius = radius
        self.set_native_anchors(self.get_native_render_anchors())
        return self

    def set_curvature(self, curvature: float) -> Circle:
        """Change the `curvature` of the hyperbolic plane that the
        :class:`Circle` lives in.

        Args:
            curvature (float): The new curvature of the hyperbolic plane. Only
            affects the receiver and not the other elements associated with the
            `plane`.

        Returns:
            Circle: The updated :class:`Circle`.
        """
        super().set_curvature(curvature)

        self.set_native_anchors(self.get_native_render_anchors())
        return self

    def set_center_of_projection(self, point: Point) -> Circle:
        """Change the center of projection of the :class:`Circle`.

        Args:
            point (hmanim.native.point.Point): The new center of projection of the :class:`Circle`.

        Returns:
            Circle: The updated :class:`Circle`.
        """
        self.center.set_center_of_projection(point)
        self.set_native_anchors(self.get_native_render_anchors())
        return self

    def get_native_render_anchors(self) -> list[Point]:
        """
        Determines the :class:`hmanim.poincare.point.Point`
        objects on the path that represents the boundary
        of the :class:`Circle`.

        """
        angles = Circle.get_render_angles(self.center)

        # Taking the center of projection into account.  It is not as easy as
        # just computing the regular circle and applying the center of
        # projection transformation at each point, since the shape of the
        # circle depends on the center of the projection and if we want to get
        # a smooth drawing, we need to ensure that the detail angles (see
        # get_render_angles()) are at the correct position.
        relative_point = self.center.get_projection_relative_point()

        # Important!: We set `is_relative` to `True`, since we already deal
        # with placing the point relative to its center of projection here.
        return [
            Point(self.radius, angle, is_relative=True)
            .translated_by(relative_point.radius, curvature=self.curvature)
            .rotated_by(relative_point.azimuth)
            .set_center_of_projection(self.center.center_of_projection)
            for angle in angles
        ]

    @staticmethod
    def get_render_angles(center: Point) -> list[float]:
        """
        Returns the angles of the points that are used to render the boundary
        of a circle. In particular, instead of distributing the angles
        uniformly, more fine-grained angles are placed towards the origin for
        smoother rendering.
        """
        number_of_angles = 360
        uniform_angles = [
            x / float(number_of_angles) * TAU
            for x in range(0, number_of_angles)
        ]
        # Depending on how far out the center of the circle is, we
        # want to place more render points near the center, since then
        # a small angular interval of the circle is stretched a lot.
        detail_resolution = int(center.radius / 5 * Circle.Resolution)
        detail_angles = [
            TAU / 2.0 * x / (sqrt(1 + (x * x)))
            for x in range(0, detail_resolution)
        ]
        inverted_detail_angles = [TAU - x for x in reversed(detail_angles)]

        angles = sorted(
            uniform_angles + detail_angles + inverted_detail_angles
        )
        angles += [angles[0]]
        # angles = uniform_angles

        return angles


class CircleScale(Animation):
    """Scale the radius of a :class:`Circle` by a given factor.

    Examples
    --------
    .. manim:: CircleScaleExample

        from hmanim.native import Circle, CircleScale, Point

        class CircleScaleExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the circle.
                circle = Circle(
                    center=Point(5.0, TAU / 8),
                    radius=5.0,
                    plane=plane
                )
                self.add(circle)

                # Scale the circle radius by a factor of 1.5.
                self.play(CircleScale(circle, 1.5))

    """

    def __init__(
        self,
        circle: Circle,
        factor: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.factor = factor
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(
            circle,
            run_time=run_time,
            **kwargs,
        )

    def interpolate_mobject(self, alpha: float):
        new_radius = self.starting_mobject.radius * (  # type: ignore
            1.0 + self.rate_func(alpha) * (self.factor - 1.0)
        )
        self.mobject.set_radius(new_radius)


class CircleRotatedTranslate(Animation):
    """Similar to :class:`CircleTranslate` but instead of translating along the
    x-axis, we translate along an axis that is rotated away from the x-axis by a
    given angle.

    Examples
    --------
    .. manim:: CircleRotatedTranslateExample

        from hmanim.native import Circle, CircleRotatedTranslate, Point

        class CircleRotatedTranslateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the circle.
                circle = Circle(
                    center=Point(0.0, 0.0),
                    radius=5.0,
                    plane=plane
                )
                self.add(circle)

                # Rotate the circle
                self.play(
                    CircleRotatedTranslate(
                        circle,
                        distance=3,
                        angle=TAU / 8
                    )
                )

    """

    def __init__(
        self,
        circle: Circle,
        distance: float,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.distance = distance
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(circle, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # The current distance we are translating.
        current_translation_distance = self.rate_func(alpha) * self.distance

        # The center of the new circle.
        rotated_center = self.starting_mobject.center.copy().rotated_by(
            -self.angle
        )
        translated_center = rotated_center.translated_by(
            current_translation_distance
        )
        new_center = translated_center.rotated_by(self.angle)

        # Update the points of the mobject to match the ones of the
        # translated one.
        self.mobject.set_center(new_center)


class CircleTranslate(CircleRotatedTranslate):
    """Translate a :class:`Circle` horizontally. The sign of the passed
    `distance` defines the direction of the translation.

    Examples
    --------
    .. manim:: CircleTranslateExample

        from hmanim.native import Circle, CircleTranslate, Point

        class CircleTranslateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the circle.
                circle = Circle(
                    center=Point(5.0, 0.0),
                    radius=5.0,
                    plane=plane
                )
                self.add(circle)

                # Translate the circle
                self.play(
                    CircleTranslate(
                        circle,
                        distance=-3
                    )
                )

    """

    def __init__(
        self,
        circle: Circle,
        distance: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(
            circle,
            distance=distance,
            angle=0.0,
            run_time=run_time,
            apply_function_kwargs=apply_function_kwargs,
            **kwargs,
        )


class CircleTranslateAndRotate(Animation):
    """Translate and simultaneously rotate a :class:`Circle`.

    Examples
    --------
    .. manim:: CircleTranslateAndRotateExample

        from hmanim.native import Circle, CircleTranslateAndRotate, Point

        class CircleTranslateAndRotateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the circle.
                circle = Circle(
                    center=Point(0.0, 0.0),
                    radius=5.0,
                    plane=plane
                )
                self.add(circle)

                # Rotate the circle
                self.play(
                    CircleTranslateAndRotate(
                        circle,
                        distance=3,
                        angle=TAU / 4
                    )
                )

    """

    def __init__(
        self,
        circle: Circle,
        distance: float,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.distance = distance
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(circle, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # The current distance we are translating / angle we are rotating.
        current_translation_distance = self.rate_func(alpha) * self.distance
        current_rotation_angle = self.rate_func(alpha) * self.angle

        # First we translate
        translated_center = self.starting_mobject.center.copy()
        if current_translation_distance != 0.0:
            translated_center.rotated_by(
                -self.starting_mobject.center.azimuth
            ).translated_by(
                current_translation_distance, curvature=self.mobject.curvature
            ).rotated_by(
                self.starting_mobject.center.azimuth
            )

        # Rotate and actually move the circle.
        self.mobject.set_center(
            translated_center.rotated_by(current_rotation_angle)
        )


class CircleRotate(CircleTranslateAndRotate):
    """Rotate the :class:`Circle` around the origin.

    Examples
    --------
    .. manim:: CircleRotateExample

        from hmanim.native import Circle, CircleRotate, Point

        class CircleRotateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the circle.
                circle = Circle(
                    center=Point(5.0, 0.0),
                    radius=5.0,
                    plane=plane
                )
                self.add(circle)

                # Rotate the circle
                self.play(
                    CircleRotate(
                        circle,
                        TAU / 8
                    )
                )

    """

    def __init__(
        self,
        circle: Circle,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(
            circle,
            distance=0.0,
            angle=angle,
            run_time=run_time,
            apply_function_kwargs=apply_function_kwargs,
            **kwargs,
        )
