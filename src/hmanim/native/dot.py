from __future__ import annotations

from typing import Any, Dict, Optional

from manim import Animation
from manim import Dot as MDot
from manim import PolarPlane
from manim.typing import Point2D

from .point import Point


class Dot(MDot):
    """Represent a dot in the hyperbolic plane that is addressed using polar
    coordinates.

    Parameters
    ----------
    point
        The :class:`hmanim.native.point.Point` at which the dot is placed.
    plane
        The :class:`PolarPlane` in which the :class:`Dot` lives.

    Examples
    --------

    .. manim:: DotExample
        :save_last_frame:

        from hmanim.native import Dot, Point

        class DotExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                dot = Dot(Point(0, 0), plane=plane)
                self.add(dot)

    """

    def __init__(self, center: Point, plane: PolarPlane, **kwargs):
        """
        Azimuth in radians.
        """
        self.plane = plane
        self._center = center
        super().__init__(
            self.center.to_point_in_plane(self.plane), **kwargs  # type: ignore
        )

    @property
    def center(self) -> Point:
        """The :class:`hmanim.native.point.Point` at which the :class:`Dot` is
        placed."""
        return self._center

    @center.setter
    def center(self, center: Point):
        return self.set_center(center)

    def set_center(self, point: Point) -> Dot:
        """Change the :class:`hmanim.native.point.Point` at which the
        class:`Dot` is placed.

        Args:
            point (hmanim.native.point.Point): The new :class:`Point` at which
                the :class:`Dot` is placed.

        Returns:
            Dot: The :class:`Dot` that was moved.
        """
        self._center = point
        super().move_to(
            self.center.to_point_in_plane(self.plane)  # type: ignore
        )
        return self

    def move_to(self, point: Point2D) -> Dot:
        """Move the :class:`Dot` to a new :class:`Point2D`. Note that this
        method gets a point on in Cartesian coordinates and not polar ones.

        Args:
            point (Point2D): The new :class:`Point2D` to which the :class:`Dot` is moved.

        Returns:
            Dot: The :class:`Dot` that was moved.
        """
        polar_coordinates = self.plane.point_to_polar(point)  # type: ignore
        polar_point = Point(polar_coordinates[0], polar_coordinates[1])
        return self.set_center(polar_point)

    def set_center_of_projection(self, point: Point) -> Dot:
        """Change the center of projection of the :class:`Dot`.

        Args:
            point (hmanim.native.point.Point): The new center of projection.

        Returns:
            Dot: The updated :class:`Dot`.
        """
        self.center.center_of_projection = point
        return self.set_center(self.center)

    def set_radius(self, radius: float) -> Dot:
        """Set the radius of the :class:`Dot`.

        Args:
            radius (float): The new radius of the :class:`Dot`.

        Returns:
            Dot: The :class:`Dot` with the new radius.
        """
        current_radius = self.radius
        self.radius = radius
        return self.scale(radius / current_radius)


class DotTranslate(Animation):
    """
    This translation represents a movement of a point from the origin along the
    x-axis by a specified distance.  All other points in the plane, in
    particular the :class:`Dot`, are moved in such a way, that the distance to
    the moving point remain unchanged.

    Examples
    --------
    .. manim:: DotTranslateExample

        from hmanim.native import Dot, DotTranslate, Point

        class DotTranslateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the dot.
                dot = Dot(Point(), plane=plane)
                self.add(dot)

                # Translate the dot horizontally by 5.
                self.play(DotTranslate(dot, 5.0))

    """

    def __init__(
        self,
        dot: Dot,
        distance: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """A 'translation along' along the x-axis by the passed `distance`."""
        self.distance = distance
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(dot, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # We animate a translation by creating circles at the intermediate
        # positions.

        # The current distance we are translating.
        current_translation_distance = self.rate_func(alpha) * self.distance

        # The center of the new circle.
        new_center = self.starting_mobject.center.copy().translated_by(
            current_translation_distance
        )

        # Actually moving the circle.
        self.mobject.set_center(new_center)


class DotRotate(Animation):
    """Rotates the :class:`Dot` around the origin by a given angle.

    Examples
    --------
    .. manim:: DotRotateExample

        from hmanim.native import Dot, DotRotate, Point

        class DotRotateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the dot.
                dot = Dot(Point(5.0, 0.0), plane)
                self.add(dot)

                # Rotate the dot by TAU / 4 radians.
                self.play(DotRotate(dot, TAU / 4))

    """

    def __init__(
        self,
        dot: Dot,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(dot, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        current_translation_angle = self.rate_func(alpha) * self.angle

        # The new center of the dot.
        new_center = self.starting_mobject.center.copy().rotated_by(
            current_translation_angle
        )

        # Actually moving the dot.
        self.mobject.set_center(new_center)


class DotTranslateAndRotate(Animation):
    """Translate the :class:`Dot` by a given distance and rotate the axis along
    which it is being translated by at the same time.

    Examples
    --------
    .. manim:: DotTranslateAndRotateExample

        from hmanim.native import Dot, DotTranslateAndRotate, Point

        class DotTranslateAndRotateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)
                self.add(plane)

                # Draw the dot.
                dot = Dot(Point(0.0, 0.0), plane)
                self.add(dot)

                # Translate and rotate the dot.
                self.play(
                    DotTranslateAndRotate(
                        dot,
                        distance=4,
                        angle=TAU / 4
                    )
                )

    """

    def __init__(
        self,
        dot: Dot,
        distance: float,
        angle: float = 0.0,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.distance = distance
        self.angle = angle
        self.start_center = dot.center.copy()
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(dot, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # The current distance we are translating / angle we are rotating.
        current_translation_distance = self.rate_func(alpha) * self.distance
        current_rotation_angle = self.rate_func(alpha) * self.angle

        # First we translate
        rotated_center = self.starting_mobject.center.copy().rotated_by(
            -self.start_center.azimuth
        )
        new_center = rotated_center.translated_by(current_translation_distance)
        rotated_new_center = new_center.rotated_by(
            self.starting_mobject.center.azimuth
        )

        # Then we rotate
        final_center = rotated_new_center.copy().rotated_by(
            current_rotation_angle
        )

        # Actually moving the dot.
        self.mobject.set_center(final_center)


class DotSetRadialCoordinate(Animation):
    """Sets the radial coordinate of the :class:`Dot` to a given value.

    Examples
    --------
    .. manim:: DotSetRadialCoordinateExample

        from hmanim.native import Dot, DotSetRadialCoordinate, Point

        class DotSetRadialCoordinateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)
                self.add(plane)

                # Draw the dot.
                dot = Dot(Point(1.0, TAU / 8), plane)
                self.add(dot)

                # Translate and rotate the dot.
                self.play(
                    DotSetRadialCoordinate(
                        dot,
                        radius=4.0
                    )
                )

    """

    def __init__(
        self,
        dot: Dot,
        radius: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.radius = radius
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(dot, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # The current distance we are translating / angle we are rotating.
        current_radius = (
            1.0 - self.rate_func(alpha)
        ) * self.starting_mobject.center.radius + self.rate_func(
            alpha
        ) * self.radius

        new_center = Point(
            radius=current_radius, azimuth=self.starting_mobject.center.azimuth
        )

        # Actually moving the dot.
        self.mobject.set_center(new_center)


class DotRotatedTranslate(Animation):
    """Similar to :class:`DotTranslate` but instead of translating along the
    x-axis, we translate along an axis that is rotated away from the x-axis by a
    given angle.

    Examples
    --------
    .. manim:: DotRotatedTranslateExample

        from hmanim.native import Dot, DotRotatedTranslate, Point

        class DotRotatedTranslateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the dot.
                dot = Dot(
                    center=Point(0.0, 0.0),
                    plane=plane,
                )
                self.add(dot)

                # Translate the dot.
                self.play(
                    DotRotatedTranslate(
                        dot,
                        distance=3,
                        angle=TAU / 8
                    )
                )

    """

    def __init__(
        self,
        dot: Dot,
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

        super().__init__(dot, run_time=run_time, **kwargs)

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
