from __future__ import annotations

from math import fmod
from typing import Any, Dict, Optional, Sequence

from manim import PI, TAU, Animation, PolarPlane
from manim import VMobject as MVMobject

from .point import Point


class VMobject(MVMobject):
    """The foundation for most hyperbolic objects, which acts as a bridge
    between hyperbolic objects and the Euclidean geometry underlying Manim.

    In a sense, it is just a collection of
    :class:`hmanim.poincare.point.Point` objects
    (`native_points`), where consecutive ones are connected by straight lines or
    geodesics.  For a :class:`Line`, the corresponding :class:`VMobject`
    consists of the start point and the end point and all the points in between
    that make up the curved geodesic.  See :meth:`set_native_points` and
    :meth:`connect_native_point` for more details.

    Parameters
    ----------
    native_points
        The :class:`hmanim.poincare.point.Point` objects
        that make up the hyperbolic object and
        between which geodesics are drawn.

    Attributes
    ----------
    Resolution (int)
        Defines how many points lie on the path that is used to represent the
        geodesic between two points.
    """

    # Defines how many points lie on the path that is used to represent the
    # geodesic between two points.
    Resolution: int = 100

    def __init__(
        self,
        *native_points: Point,
        plane: PolarPlane,
        curvature: float = -1,
        **kwargs,
    ):
        self.plane = plane
        self.curvature = curvature

        super().__init__(**kwargs)

        if native_points:
            self.set_native_points(native_points)
        else:
            self.set_native_points([])

    def set_native_points(self, native_points: Sequence[Point]):
        self.clear_native_points()

        # Iterate the remaining points and add them depending on their
        # connection type.
        for point in native_points:
            self.connect_native_point(point)

    def clear_native_points(self):
        self.native_points = []
        super().clear_points()

    def connect_native_point(
        self,
        native_point: Point,
        using_geodesic: bool = False,
        smooth_straight_geodesics: bool = False,
    ):
        if len(self.native_points) == 0:
            # We add the first native point.
            self.native_points.append(native_point)
            render_start_point = self.native_points[0].to_point_in_plane(
                self.plane
            )
            self.set_points([render_start_point])  # type: ignore

            return

        if using_geodesic:
            render_native_points = (
                VMobject.get_native_render_points_for_geodesic(
                    self.native_points[-1],
                    native_point,
                    curvature=self.curvature,
                    smooth_straight_geodesics=smooth_straight_geodesics,
                )
            )
            for render_native_point in render_native_points:
                self.connect_native_point(render_native_point)

            return

        self.native_points.append(native_point)
        render_point = native_point.to_point_in_plane(self.plane)
        super().add_line_to(render_point)  # type: ignore

    @staticmethod
    def get_native_render_points_for_geodesic(
        start_point: Point,
        end_point: Point,
        curvature: float = -1,
        smooth_straight_geodesics: bool = False,
        resolution: int = Resolution,
    ) -> list[Point]:
        """
        Determines the list of
        :class:`hmanim.poincare.point.Point` objects that
        lie on the geodesic line segment between the
        `start_point` and `end_point`.

        Parameters
        ----------
        start_point
            The start point of the geodesic.
        end_point
            The end point of the geodesic.
        curvature
            The curvature of the hyperbolic plane that the geodesic lives in.
        smooth_straight_geodesics
            When `smooth_straight_geodesics` is set to `True` we do NOT represent a
            hyperbolic line that happens to be equivalent to a Euclidean straight
            line with only two points, but rather with as many points as all other
            geodesic line segments.
        resolution
            Eventually, a geodesic line segment is represented by a chain of
            straight line segments. The `resolution` defines the number of
            straight line segments that make up the geodesic. The higher, the
            smoother the drawn geodesic.
        """

        # We don't need any render points if the start and end are the same
        # points.
        if start_point == end_point:
            return [start_point, end_point]

        # If they have the same azimuth or opposite, the geodesic is just a
        # straight line.
        if not smooth_straight_geodesics and (
            start_point.azimuth == end_point.azimuth
            or start_point.azimuth == fmod(end_point.azimuth + PI, TAU)
        ):
            return [start_point, end_point]

        # Consider the sequence of transformations that move the `start_point`
        # to the origin and the `end_point` on the x-axis in positive
        # direction.  This can be done, by first rotating the `start_point`
        # onto the x-axis in positive direction, i.e., rotating everything by
        # `-start_point.azimuth`.  Then, we translate everything by
        # `-start_point.radius`.  Finally, we rotate everything by the negative
        # of the azimuth of the rotated and translated `end_point`.

        # The angle of the first rotation
        first_rotation_angle = -start_point.azimuth

        # The distance we translate by
        translation_distance = -start_point.radius

        # The angle of the second rotation is the negative of the azimuth of
        # the rotated and translated `end_point`
        second_rotation_angle = (
            -end_point.copy()
            .rotated_by(first_rotation_angle)
            .translated_by(translation_distance, curvature=curvature)
            .azimuth
        )

        # In the following, we simply generate a sequence of points that lie on
        # the x-axis between the two transformed points, and than 'revert' the
        # transformation.
        distance = start_point.distance_to(end_point, curvature=curvature)

        transformed_render_points = [
            Point(
                x / resolution * distance,
                0.0,
                center_of_projection=start_point.center_of_projection,
            )
            for x in range(
                0, resolution + 1
            )  # + 1, since we want the end_point to be covered, too.
        ]

        # Now we revert the transformation
        return [
            p.rotated_by(-second_rotation_angle)
            .translated_by(-translation_distance, curvature=curvature)
            .rotated_by(-first_rotation_angle)
            for p in transformed_render_points
        ]

    def copy(self) -> VMobject:
        copied_points = [p.copy() for p in self.native_points]
        return VMobject(
            *copied_points, plane=self.plane, curvature=self.curvature
        ).match_style(self)

    def set_curvature(self, curvature: float) -> VMobject:
        """Change the curvature of the hyperbolic plane that the
        :class:`VMobject` lives in.

        Note
        ----
            Only affects the object itself and not the other objects that are
            associated with the corresponding hyperbolic plane.

        Args:
            curvature (float): The new (negative) curvature of the hyperbolic
                plane.

        Returns:
            VMobject: The modified :class:`VMobject`.
        """
        self.curvature = curvature
        return self

    def set_center_of_projection(self, point: Point) -> VMobject:
        """Change the center of projection of the hyperbolic plane that the
        :class:`VMobject` lives in.

        Note
        ----
            Only affects the object itself and not the other objects that are
            associated with the corresponding hyperbolic plane.

        Args:
            point (hmanim.native.point.Point): The new center of projection.

        Returns:
            VMobject: The modified :class:`VMobject`.
        """
        moved_points = [
            p.copy().set_center_of_projection(point)
            for p in self.native_points
        ]
        self.set_native_points(moved_points)
        return self

    def translated_by(self, distance: float) -> VMobject:
        """Translate all points of the :class:`VMobject` in positive x-direction
        by the passed `distance`.

        Args:
            distance (float): The distance by which to translate the points. A
            negative value will translate the points in negative x-direction.

        Returns:
            VMobject: The modified :class:`VMobject`.
        """
        # Translate all points.
        self.set_native_points(
            [
                p.copy().translated_by(distance, curvature=self.curvature)
                for p in self.native_points
            ]
        )
        return self

    def rotated_by(self, angle: float) -> VMobject:
        """Rotate all points of the :class:`VMobject` around
        the origin by the passed `angle` in radians.

        Args:
            angle (float): The angle by which to rotate the points.

        Returns:
            VMobject: The modified :class:`VMobject`.
        """
        # Rotate all points.
        self.set_native_points(
            [p.copy().rotated_by(angle) for p in self.native_points]
        )
        return self


class VMobjectRotatedTranslate(Animation):
    """
    This translation represents a movement of a point from the origin along an
    axis (rotated away from the x-axis by the passed angle) by a specified
    distance.  All other points of the :class:`VMobject`, are moved in such a
    way, that the distance to the moving point remains unchanged.

    Note
    ----
        This class is not meant to be used directly. See
        :class:`RotatedTranslate` instead.
    """

    def __init__(
        self,
        mobject: VMobject,
        distance: float,
        angle: float = 0.0,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """A 'translation along' along the x-axis by the passed `distance`."""
        self.distance = distance
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(mobject, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # The current distance we are translating.
        current_translation_distance = self.rate_func(alpha) * self.distance

        # The center of the new circle.
        rotated_mobject = self.starting_mobject.copy().rotated_by(-self.angle)
        translated_mobject = rotated_mobject.translated_by(
            current_translation_distance
        )
        new_mobject = translated_mobject.rotated_by(self.angle)

        # Update the points of the mobject to match the ones of the
        # translated one.
        self.mobject.set_native_points(new_mobject.native_points)


class VMobjectTranslate(VMobjectRotatedTranslate):
    """
    This translation represents a movement of a point from the origin along the
    x-axis in positive direction.  All other points of the :class:`VMobject`,
    are moved in such a way, that the distance to the moving point remains
    unchanged.

    Note
    ----
        This class is not meant to be used directly. See
        :class:`Translate` instead.
    """

    def __init__(
        self,
        mobject: VMobject,
        distance: float,
        run_time: float = 3,
        apply_function_kwargs: Dict[str, Any] | None = None,
        **kwargs,
    ):
        """A rotation around the origin by the passed `angle` in radians."""
        super().__init__(
            mobject,
            distance=distance,
            angle=0.0,
            run_time=run_time,
            apply_function_kwargs=apply_function_kwargs,
            **kwargs,
        )


class VMobjectTranslateAndRotate(Animation):
    """
    Represents a movement of a point from the origin along an axis, while that
    axis is rotating around the origin at the same time.  All other points of
    the :class:`VMobject`, are moved in such a way, that the distance to the
    moving point remains unchanged.

    Note
    ----
        This class is not meant to be used directly. See
        :class:`TranslateAndRotate` instead.
    """

    def __init__(
        self,
        mobject: VMobject,
        distance: float,
        angle: float = 0.0,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """The mobject is translated and simultaneously rotated."""
        self.distance = distance
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(mobject, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # The current distance we are translating / angle we are rotating.
        current_translation_distance = self.rate_func(alpha) * self.distance
        current_rotation_angle = self.rate_func(alpha) * self.angle

        # First we translate
        translated_mobject = self.starting_mobject.copy()
        if current_translation_distance != 0.0:
            translated_mobject.rotated_by(
                -self.starting_mobject.center.azimuth
            ).translated_by(
                current_translation_distance, curvature=self.mobject.curvature
            ).rotated_by(
                self.starting_mobject.center.azimuth
            )

        # Rotate and actually move the circle.
        self.mobject.set_native_points(
            translated_mobject.rotated_by(current_rotation_angle).native_points
        )


class VMobjectRotate(VMobjectTranslateAndRotate):
    """
    Rotates all points of the :class:`VMobject` around the origin.

    Note
    ----
        This class is not meant to be used directly. See
        :class:`TranslateAndRotate` instead.
    """

    def __init__(
        self,
        mobject: VMobject,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Dict[str, Any] | None = None,
        **kwargs,
    ):
        """A rotation around the origin by the passed `angle` in radians."""
        super().__init__(
            mobject,
            distance=0.0,
            angle=angle,
            run_time=run_time,
            apply_function_kwargs=apply_function_kwargs,
            **kwargs,
        )


class VMobjectSetCurvature(Animation):
    """
    An animation that changes the `curvature` of the hyperbolic plane that the
    :class:`VMobject` lives in. However, this change only affects the receiving
    :class:`VMobject`.

    Note
    ----
        This class is not meant to be used directly. See
        :class:`SetCurvature` instead.
    """

    def __init__(
        self,
        mobject: VMobject,
        curvature: float,
        run_time: float = 3,
        apply_function_kwargs: Dict[str, Any] | None = None,
        **kwargs,
    ):
        self.curvature = curvature
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(mobject, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        # The current angle we are rotating.
        new_curvature = (
            self.rate_func(alpha) * self.curvature
            + (1.0 - self.rate_func(alpha))
            * self.starting_mobject.curvature  # type: ignore
        )

        # The translated polygon.  We need to create copies, since we don't
        # want to modify the start_chain.
        self.mobject.set_curvature(new_curvature)
