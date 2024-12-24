from __future__ import annotations

from typing import Any, Dict, Optional

from manim import TAU, Animation, PolarPlane

from .circle import Circle
from .point import Point
from .polygonal_chain import PolygonalChain
from .vmobject import VMobject


class Arc(PolygonalChain):
    """A circular arc.

    Parameters
    ----------
    center
        A :class:`hmanim.poincare.point.Point` representing the center of the circle that the
        :class:`Arc` lives on.
    radius
        A `float` representing the radius of the circle that the :class:`Arc`
        lives on.
    start_angle
        A `float` representing the angle at which the arc starts.
    angle
        A `float` representing the angular width of the arc, i.e., how far it
        extends from the `start_angle`.
    plane
        The :class:`PolarPlane` in which the :class:`Arc` lives.

    Examples
    --------
    .. manim:: ArcExample
        :save_last_frame:

        from hmanim.native import Arc, Point

        class ArcExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the arc.
                arc = Arc(
                    center=Point(),
                    radius=5.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane
                )
                self.add(arc)

    """

    def __init__(
        self,
        center: Point,
        radius: float,
        start_angle: float,
        angle: float,
        plane: PolarPlane,
        is_closed: bool = False,
        **kwargs,
    ):
        """
        Initialize an arc using its start angle, as well as the angle by which
        it extends from the start angle.  All angles are given in radians.

        """
        self._center = center
        self.radius = radius
        self.start_angle = start_angle
        self.angle = angle
        self.plane = plane
        self._is_closed = is_closed

        super().__init__(plane=plane, using_geodesic=False, **kwargs)

        self.set_native_anchors(self.get_native_render_anchors())

    @property
    def center(self) -> Point:
        return self._center

    @center.setter
    def center(self, center: Point):
        self.set_center(center)

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    @is_closed.setter
    def is_closed(self, is_closed: bool):
        self._is_closed = is_closed
        self.set_native_anchors(self.get_native_render_anchors())

    def get_native_render_anchors(self) -> list[Point]:
        native_arc_anchors = list(
            Arc.native_render_anchors(
                self.center,
                self.radius,
                self.start_angle,
                self.angle,
                self.curvature,
            )
        )

        if self.is_closed:
            native_arc_anchors += (
                VMobject.get_native_render_points_for_geodesic(
                    native_arc_anchors[-1],
                    native_arc_anchors[0],
                    smooth_straight_geodesics=True,
                )
            )

        return native_arc_anchors

    def copy(self) -> Arc:
        return Arc(
            self.center,
            self.radius,
            self.start_angle,
            self.angle,
            plane=self.plane,
            is_closed=self.is_closed,
            curvature=self.curvature,
        ).match_style(self)

    @staticmethod
    def native_render_anchors(
        center: Point,
        radius: float,
        start_angle: float,
        angle: float,
        curvature: float,
    ) -> list[Point]:
        arc_angles = Arc.get_render_angles(center, start_angle, angle)

        # TODO: Here we would actually want to use the
        # projection_relative_point of the center, to ensure that we get a
        # smooth arc.  However, since we interpret the arc angles to be defined
        # for a circle center at the origin and then rotate the whole arc,
        # using the relative_point currently rotates the arc in a wrong
        # direction.
        #
        # relative_point = center.get_projection_relative_point()
        relative_point = center

        points = [
            Point(
                radius, angle, center_of_projection=center.center_of_projection
            )
            .translated_by(relative_point.radius, curvature=curvature)
            .rotated_by(relative_point.azimuth)
            for angle in arc_angles
        ]

        return [points[0]] + points + [points[-1]]

    @staticmethod
    def get_render_angles(
        center: Point, start_angle: float, angle: float
    ) -> list[float]:
        """
        Determines the angle of the points on the path that represents the
        boundary of the :class:`Arc`.

        """
        # First we get the render angles of a whole circle.
        #
        # We remove the last angle since it is just the duplicate 0 angle that
        # closes the circle.
        angles = Circle.get_render_angles(center)[:-1]

        start_angle = Point.normalize_angle(start_angle)

        # Remove all angles that do not belong to the arc.  First, we check
        # whether the arc spans TAU.
        end_angle = start_angle + angle

        arc_spans_TAU = end_angle > TAU

        if arc_spans_TAU:
            normalized_end_angle = Point.normalize_angle(end_angle)
            # If the arc spans TAU, we want to keep all angles below the
            # normalized_end_angle...
            lower_angles = [
                angle for angle in angles if angle < normalized_end_angle
            ]
            # ... and everything that is above the start_angle.
            upper_angles = [angle for angle in angles if angle > start_angle]

            # Now we add them in the correct order.
            angles = (
                [start_angle]
                + upper_angles
                + lower_angles
                + [normalized_end_angle]
            )
        else:
            # If the arc does not span TAU, we simply keep all angles between
            # the start_angle and the end_angle.
            angles = [
                angle
                for angle in angles
                if angle > start_angle and angle < end_angle
            ]
            angles = [start_angle] + angles + [end_angle]

        return angles

    def set_center(self, center: Point) -> Arc:
        """Move the center of the :class:`Arc` to the given `center`.

        Args:
            center (hmanim.native.point.Point): The new center of the :class:`Arc`.

        Returns:
            Arc: The :class:`Arc` with the new center.
        """
        self._center = center
        self.set_native_anchors(self.get_native_render_anchors())
        return self

    def translated_by(self, distance: float) -> Arc:
        """Translate the :class:`Arc` horizontally by the given `distance`. A
        negative distance represents a translation in the opposite direction.

        Args:
            distance (float): The distance to translate the :class:`Arc` by.

        Returns:
            Arc: The :class:`Arc` translated by the given `distance`.
        """
        return self.set_center(
            self.center.copy().translated_by(distance, self.curvature)
        )

    def set_radius(self, radius: float) -> Arc:
        """Set the radius of the :class:`Arc`.

        Args:
            radius (float): The new radius of the :class:`Arc`.

        Returns:
            Arc: The :class:`Arc` with the new radius.
        """
        self.radius = radius
        self.set_native_anchors(self.get_native_render_anchors())
        return self

    def set_center_of_projection(self, point: Point) -> Arc:
        """Change the center of projection of the :class:`Arc`.

        Args:
            point (hmanim.native.point.Point): The new center of projection of the :class:`Arc`.

        Returns:
            Arc: The :class:`Arc` with the new center of projection.
        """
        self.center.set_center_of_projection(point)
        super().set_center_of_projection(point)
        return self

    def set_start_angle(self, start_angle: float) -> Arc:
        """Set the start angle of the :class:`Arc`.

        Args:
            start_angle (float): The new start angle of the :class:`Arc`.

        Returns:
            Arc: The :class:`Arc` with the new start angle.
        """
        self.start_angle = Point.normalize_angle(start_angle)
        self.set_native_anchors(self.get_native_render_anchors())
        return self

    def set_angle(self, angle: float) -> Arc:
        """Set the angle of the :class:`Arc`.

        Args:
            angle (float): The new angle of the :class:`Arc`.

        Returns:
            Arc: The :class:`Arc` with the new angle.
        """
        self.angle = angle
        self.set_native_anchors(self.get_native_render_anchors())
        return self

    def rotated_by(self, angle: float) -> Arc:
        """Rotate the :class:`Arc` by the given `angle`. Note that the
        :class:`Arc` is rotated around the origin of its `plane`.

        Args:
            angle (float): The angle to rotate the :class:`Arc` by.

        Returns:
            Arc: The :class:`Arc` rotated by the given `angle`.
        """
        if self.center.radius == 0.0:
            return self.set_start_angle(self.start_angle + angle)

        return super().rotated_by(angle)  # type: ignore


class ArcScale(Animation):
    """Scale the radius of an :class:`Arc` by a given factor.

    Examples
    --------
    .. manim:: ArcScaleExample

        from hmanim.native import Arc, ArcScale, Point

        class ArcScaleExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the arc.
                arc = Arc(
                    center=Point(0.0, 0.0),
                    radius=5.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane,
                )
                self.add(arc)

                # Scale the arc radius by a factor of 1.5.
                self.play(ArcScale(arc, 1.5))

    """

    def __init__(
        self,
        arc: Arc,
        factor: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.factor = factor
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(arc, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        new_radius = self.starting_mobject.radius * (  # type: ignore
            1.0 + self.rate_func(alpha) * (self.factor - 1.0)
        )
        self.mobject.set_radius(new_radius)


class ArcStretchAngle(Animation):
    """Stretch the angle of an :class:`Arc` to a new value.

    Examples
    --------
    .. manim:: ArcStretchAngleExample

        from hmanim.native import Arc, ArcStretchAngle, Point

        class ArcStretchAngleExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the arc.
                arc = Arc(
                    center=Point(0.0, 0.0),
                    radius=5.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane,
                )
                self.add(arc)

                # Stretch the angle of the arc.
                self.play(ArcStretchAngle(arc, TAU / 4))

    """

    def __init__(
        self,
        arc: Arc,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(arc, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        current_angle = self.starting_mobject.angle * (
            1.0 - self.rate_func(alpha)  # type: ignore
        ) + self.angle * self.rate_func(alpha)

        self.mobject.set_angle(current_angle)


class ArcStretchAngleInverse(Animation):
    """Like :class:`ArcStretchAngle` but stretches in the inverse direction.

    Examples
    --------
    .. manim:: ArcStretchAngleInverseExample

        from hmanim.native import Arc, ArcStretchAngleInverse, Point

        class ArcStretchAngleInverseExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the arc.
                arc = Arc(
                    center=Point(0.0, 0.0),
                    radius=5.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane,
                )
                self.add(arc)

                # Stretch the angle of the arc.
                self.play(ArcStretchAngleInverse(arc, TAU / 4))

    """

    def __init__(
        self,
        arc: Arc,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(arc, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        current_angle = self.starting_mobject.angle * (
            1.0 - self.rate_func(alpha)  # type: ignore
        ) + self.angle * self.rate_func(alpha)
        angle_distance = self.starting_mobject.angle - current_angle

        self.mobject.set_angle(current_angle).set_start_angle(
            self.starting_mobject.start_angle + angle_distance
        )
