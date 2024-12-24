from __future__ import annotations

from math import acos, acosh, copysign, cos, cosh, sinh, sqrt

from manim import PI, TAU, PolarPlane
from manim.typing import Point2D


class Point:
    """Represent a point in the hyperbolic plane using polar coordinates.

    Parameters
    ----------
    radius
        The hyperbolic distance between the :class:`Point` an the origin of the
        hyperbolic plane.
    azimuth
        The angle between the :class:`Point` and the pole (ray starting at the
        origin and extending in positive x-direction).
    center_of_projection:
        The center of projection of the hyperbolic plane.


    By default `is_relative` is `False`, meaning when converting the receiver to
    a point in the Euclidean plane, we first determine its coordinates relative
    to its center of projection and only then correct the point in Euclidean
    space.  When `is_relative` is `True`, we do NOT determine the coordinates
    relative to the center of projection (since we assume that the point is
    relative already), and correct the point in Euclidean space as is.  This can
    be useful as some classes like :class:`Circle` deal with the projection
    themselves and only need the correction.

    """

    def __init__(
        self,
        radius: float = 0,
        azimuth: float = 0,
        center_of_projection: Point | None = None,
        needs_center_of_projection: bool = True,
        is_relative: bool = False,
    ):
        # If the point needs a center of projection, we create one that
        # represents the origin.
        self.center_of_projection = center_of_projection
        if self.center_of_projection is None and needs_center_of_projection:
            self.center_of_projection = Point(needs_center_of_projection=False)
        self.is_relative = is_relative

        self.set_radius_azimuth(radius, azimuth)

    def __eq__(self, other):
        if isinstance(other, Point):
            return (
                self.radius == other.radius and self.azimuth == other.azimuth
            )
        return False

    def copy(self) -> Point:
        return Point(self.radius, self.azimuth, self.center_of_projection)

    @staticmethod
    def normalize_angle(angle: float) -> float:
        """Given an `angle` in radians, returns the equivalent angle in [0, 2 PI]."""
        normalized_angle = angle
        while normalized_angle < 0.0:
            normalized_angle += TAU

        while normalized_angle > TAU:
            normalized_angle -= TAU

        return normalized_angle

    def get_projection_relative_point(self) -> Point:
        """
        Returns a :class:`Point` whose coordinates represent the ones of the
        receiver, but as if its center of projection was the origin.

        """
        if (
            self.center_of_projection is None
            or self.center_of_projection == Point()
        ):
            return self.copy()

        return (
            self.copy()
            .rotated_by(-self.center_of_projection.azimuth)
            .translated_by(-self.center_of_projection.radius)
            .rotated_by(self.center_of_projection.azimuth)
        )

    def to_point_in_plane(self, plane: PolarPlane) -> Point2D:
        """
        Converts the receiver to a canvas :class:`Point2D`, assuming that it
        lies in the passed :class:`PolarPlane`.
        """
        # When determining which point in the plane this :class:`Point`
        # represents, we take its center of projection into account.  But only,
        # if such exists.
        if (
            self.center_of_projection is None
            or self.center_of_projection == Point()
        ):
            return plane.polar_to_point(self.radius, self.azimuth)

        # When there is a center of projection that is different from the
        # origin, we pretend that this point is the origin.  So, we translate
        # our current point such that it is relative to this point.

        relative_point = self.copy()
        if not self.is_relative:
            relative_point = self.get_projection_relative_point()

        # Finally, we apply the Euclidean translation that moves the relative
        # point to its actual location.
        return plane.polar_to_point(
            relative_point.radius, relative_point.azimuth
        ) + plane.polar_to_point(
            self.center_of_projection.radius, self.center_of_projection.azimuth
        )  # type: ignore

    def distance_to(self, other, curvature: float = -1) -> float:
        """
        Returns the hyperbolic distance between the receiver and the `other`
        :class:`Point`.
        """
        if self.radius == 0.0:
            return other.radius

        if other.radius == 0.0:
            return self.radius

        angular_diff = abs(self.azimuth - other.azimuth)
        angular_diff = min(angular_diff, TAU - angular_diff)

        distance = 0.0
        zeta = sqrt(-curvature)
        try:
            distance = (
                1.0
                / zeta
                * acosh(
                    cosh(zeta * self.radius) * cosh(zeta * other.radius)
                    - sinh(zeta * self.radius)
                    * sinh(zeta * other.radius)
                    * cos(angular_diff)
                )
            )
        except ValueError:
            pass

        return distance

    def rotated_by(self, angle: float) -> Point:
        """
        Rotates the receiver around the origin by the passed `angle` in
        radians.
        """
        self.azimuth = Point.normalize_angle(self.azimuth + angle)
        return self

    def set_radius_azimuth(self, radius: float, azimuth: float) -> Point:
        self.radius = radius
        self.azimuth = Point.normalize_angle(azimuth)

        # The following are precomputed values that should speed up later
        # computations.
        try:
            self.coshRadius = cosh(self.radius)
            self.sinhRadius = sinh(self.radius)
        except (ValueError, OverflowError):
            self.coshRadius = 0
            self.sinhRadius = 0

        return self

    def translated_by(self, distance: float, curvature: float = -1) -> Point:
        """
        This translation represents a movement of a point from the origin along
        the x-axis by a specified distance.  All other points in the plane, in
        particular the receiver :class:`Point`, are moved in such a way, that
        the distance to the moving point remain unchanged.

        Note
            Does not actually move the other objects in the plane.  But only the
            receiver.

        """
        if distance == 0:
            return self

        if self.azimuth == 0.0:
            new_radius = abs(self.radius + distance)
            new_angle = 0.0
            if self.radius + distance < 0.0:
                new_angle = PI

            self.set_radius_azimuth(new_radius, new_angle)
            return self

        if self.azimuth == PI:
            new_radius = abs(self.radius - distance)
            new_angle = 0.0
            if self.radius - distance >= 0.0:
                new_angle = PI

            self.set_radius_azimuth(new_radius, new_angle)
            return self

        reference_radius = abs(distance)
        reference_angle = 0.0
        if distance > 0:
            reference_angle = PI
        reference_point = Point(reference_radius, reference_angle)

        moving_angle = self.azimuth
        if moving_angle > PI:
            moving_angle = TAU - moving_angle
        moving_point = Point(self.radius, moving_angle)

        new_radius = moving_point.distance_to(
            reference_point, curvature=curvature
        )

        zeta = sqrt(-curvature)
        enumerator = (
            cosh(zeta * abs(distance)) * cosh(zeta * new_radius)
        ) - cosh(zeta * self.radius)
        denominator = sinh(zeta * abs(distance)) * sinh(zeta * new_radius)

        try:
            new_angle = acos(enumerator / denominator)
        except ValueError:
            # Here, a `ValueError` typically occurs when enumerator and
            # denominator are close to each other, resulting in a division that
            # is close to +/-1 (but slightly larger in absolute terms).  Since
            # acos(1) = 0 and acos(-1) = PI, we just take an angle of 0 or PI
            # as close enough.
            if copysign(1, enumerator) == copysign(1, denominator):
                new_angle = 0.0
            else:
                new_angle = PI
        except ZeroDivisionError:
            new_angle = 0.0

        if distance < 0.0:
            new_angle = PI - new_angle

        if self.azimuth > PI:
            new_angle = TAU - new_angle

        self.set_radius_azimuth(new_radius, new_angle)
        return self

    def set_center_of_projection(self, point: Point | None) -> Point:
        """Changes the center of projection of the receiver.

        Args:
            point (Point): The new center of projection.

        Returns:
            Point: The receiver with the new center of projection.
        """
        self.center_of_projection = point
        return self
