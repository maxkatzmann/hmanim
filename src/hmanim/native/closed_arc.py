from __future__ import annotations

from typing import Any, Dict, Optional

from manim import Animation, PolarPlane
from manim import Polygon as MPolygon
from manim.typing import Point2D

from .arc import Arc
from .point import Point
from .polygonal_chain import PolygonalChain


# In contrast to :class:`Arc`, :class:`ClosedArc` does not derive from
# :class:`PolygonalChain` but rather from polygon, as otherwise there are
# issue when using `FadeIn` with background fill.
class ClosedArc(MPolygon):
    """
    A circular arc whose endpoints are connected by a geodesic line segment.

    Parameters
    ----------
    center
        A :class:`hmanim.poincare.point.Point` representing the center of the circle that the
        :class:`ClosedArc` lives on.
    radius
        A `float` representing the radius of the circle that the :class:`Arc`
        lives on.
    start_angle
        A `float` representing the angle at which the closed arc starts.
        The angle is measured in radians and is measured counterclockwise
        from the positive x-axis.
    angle
        A `float` representing the angular width of the closed arc, i.e., how
        far it extends from the `start_angle`.
    plane
        The :class:`PolarPlane` in which the :class:`ClosedArc` lives.

    Examples
    --------
    .. manim:: ClosedArcExample
        :save_last_frame:

        from hmanim.native import ClosedArc, Point

        class ClosedArcExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the closed arc.
                arc = ClosedArc(
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
        *args,
        **kwargs,
    ):
        self._center = center
        self.radius = radius
        self.start_angle = start_angle
        self.angle = angle
        self.plane = plane

        points = self.get_render_points()

        super().__init__(*points, *args, **kwargs)  # type: ignore

    @property
    def center(self) -> Point:
        """The center of the circle that the :class:`ClosedArc` lives on."""
        return self._center

    @center.setter
    def center(self, center: Point):
        self._center = center

    def set_center_of_projection(self, point: Point) -> ClosedArc:
        """Change the center of projection of the :class:`ClosedArc`.

        Args:
            point (hmanim.native.point.Point): The new center of projection.

        Returns:
            ClosedArc: The updated :class:`ClosedArc`.
        """
        self.center.center_of_projection = point
        self.set_points_smoothly(self.get_render_points())  # type: ignore

        return self

    def get_render_points(self) -> list[Point2D]:
        native_render_points = self.get_native_render_points()
        return [
            p.to_point_in_plane(self.plane)
            # TODO: We should set relative to False, as soon as we deal with
            # relative_point in native_render_points().
            for p in native_render_points
        ]

    def get_native_render_points(self) -> list[Point]:
        return ClosedArc.native_render_points(
            self.center, self.radius, self.start_angle, self.angle
        )

    @staticmethod
    def native_render_points(
        center: Point, radius: float, start_angle: float, angle: float
    ) -> list[Point]:
        # We first get the points that lie on the arc...
        arc_points = Arc.native_render_anchors(
            center, radius, start_angle, angle, curvature=-1
        )

        # Since the arc is closed, we also add the points representing the
        # geodesic line between the arc ends.  Here we use `smooth_straights`
        # since otherwise the smoothing of manim has trouble connecting the arc
        # with the geodesic.
        geodesic_points = PolygonalChain.get_native_render_points_for_geodesic(
            arc_points[-1], arc_points[0], smooth_straight_geodesics=True
        )

        return arc_points + geodesic_points

    def move_to(self, center: Point) -> ClosedArc:
        self.center = center
        self.native_points = self.get_native_render_points()
        self.set_points_smoothly(self.get_render_points())  # type: ignore
        return self

    def set_radius_to(self, radius: float) -> ClosedArc:
        """Set the radius of the :class:`ClosedArc`.

        Args:
            radius (float): The new radius.

        Returns:
            ClosedArc: The updated :class:`ClosedArc`.
        """
        self.radius = radius
        self.native_points = self.get_native_render_points()
        self.set_points_smoothly(self.get_render_points())  # type: ignore
        return self

    def rotated_by(self, angle: float) -> ClosedArc:
        """Rotate the :class:`ClosedArc` by the given `angle`.

        This is rotation around the origin and NOT around the center of the arc.
        Only when the center of the arc lies on the origin, do we actually
        adjust the start_angle.

        Args:
            angle (float): The angle in radians to rotate the :class:`ClosedArc`
            by.

        Returns:
            ClosedArc: The updated :class:`ClosedArc`.
        """
        if self.center.radius == 0.0:
            self.start_angle = Point.normalize_angle(self.start_angle + angle)
            self.native_points = self.get_native_render_points()
            self.set_points_smoothly(
                self.get_render_points()  # type: ignore
            )  # Notice render_points and not native_render_points.

            return self

        return super().rotated_by(angle)  # type: ignore


class ClosedArcTranslate(Animation):
    """Translate an :class:`ClosedArc` by a given distance.

    Examples
    --------
    .. manim:: ClosedArcTranslateExample

        from hmanim.native import ClosedArc, ClosedArcTranslate, Point

        class ClosedArcTranslateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the arc.
                arc = ClosedArc(
                    center=Point(0.0, 0.0),
                    radius=4.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane
                )
                self.add(arc)

                # Translate the arc by a distance of 2.0.
                self.play(ClosedArcTranslate(arc, 2.0))

    """

    def __init__(
        self,
        arc: ClosedArc,
        distance: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """A 'translation along' along the x-axis by the passed `distance`."""
        self.start_center = arc.center
        self.distance = distance
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(arc, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # The current distance we are translating.
        current_translation_distance = self.rate_func(alpha) * self.distance

        # The center of the new arc.
        new_center = self.start_center.copy().translated_by(
            current_translation_distance
        )

        # Actually moving the arc.
        self.mobject.move_to(new_center)  # type: ignore


class ClosedArcRotate(Animation):
    """Rotate an :class:`ClosedArc` around the origin by a given angle.

    Examples
    --------
    .. manim:: ClosedArcRotateExample

        from hmanim.native import ClosedArc, ClosedArcRotate, Point

        class ClosedArcRotateExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the arc.
                arc = ClosedArc(
                    center=Point(0.0, 0.0),
                    radius=4.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane
                )
                self.add(arc)

                # Rotate the arc by TAU / 8 radians.
                self.play(ClosedArcRotate(arc, TAU / 8))

    """

    def __init__(
        self,
        arc: ClosedArc,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.initial_start_angle = arc.start_angle
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(arc, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        current_rotation_angle = self.rate_func(alpha) * self.angle

        self.mobject.start_angle = self.initial_start_angle  # type: ignore
        self.mobject.rotated_by(current_rotation_angle)

        self.mobject.set_points_smoothly(self.mobject.get_render_points())


class ClosedArcScale(Animation):
    """Scale the radius of an :class:`ClosedArc` by a given factor.

    Examples
    --------
    .. manim:: ClosedArcScaleExample

        from hmanim.native import ClosedArc, ClosedArcScale, Point

        class ClosedArcScaleExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the arc.
                arc = ClosedArc(
                    center=Point(0.0, 0.0),
                    radius=4.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane
                )
                self.add(arc)

                # Scale the arc radius by a factor of 1.5.
                self.play(ClosedArcScale(arc, 1.5))

    """

    def __init__(
        self,
        arc: ClosedArc,
        factor: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.start_radius = arc.radius
        self.factor = factor
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(arc, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        new_radius = self.start_radius * (
            1.0 + self.rate_func(alpha) * (self.factor - 1.0)
        )
        self.mobject.set_radius_to(new_radius)
