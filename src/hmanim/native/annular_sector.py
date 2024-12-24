from __future__ import annotations

from typing import Any, Dict, Optional

from manim import Animation, PolarPlane

from .arc import Arc
from .point import Point
from .polygon import Polygon


class AnnularSector(Polygon):
    """Basically a thick circular :class:`Arc`.

    Parameters
    ----------
    center
        A :class:`hmanim.poincare.point.Point` representing the center of the circle that the
        :class:`AnnularSector` lives in.
    inner_radius
        A `float` representing the radius from which on the sector extends.
    outer_radius
        A `float` representing the radius up to which the sector extends.
    start_angle
        A `float` representing the angle at which the sector starts.
    angle
        A `float` representing the angular width of the sector, i.e., how far it
        extends from the `start_angle`.
    plane
        The :class:`PolarPlane` in which the :class:`AnnularSector` lives.

    Examples
    --------
    .. manim:: AnnularSectorExample
        :save_last_frame:

        from hmanim.native import AnnularSector, Point

        class AnnularSectorExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the sector.
                sector = AnnularSector(
                    center=Point(),
                    inner_radius=1.0,
                    outer_radius=3.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane
                )
                self.add(sector)
    """

    def __init__(
        self,
        center: Point,
        inner_radius: float,
        outer_radius: float,
        start_angle: float,
        angle: float,
        plane: PolarPlane,
        **kwargs,
    ):
        start_angle = Point.normalize_angle(start_angle)
        angle = Point.normalize_angle(angle)
        self._center = center
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.start_angle = start_angle
        self.angle = angle
        self.plane = plane

        super().__init__(plane=plane, using_geodesic=False, **kwargs)

        self.set_native_anchors(self.get_native_render_anchors())

    @property
    def center(self) -> Point:
        """The center of the annular sector.

        Returns:
            hmanim.native.point.Point: The center of the annular sector.
        """
        return self._center

    @center.setter
    def center(self, center: Point):
        self.set_center(center)

    def copy(self) -> AnnularSector:
        """Copy the annular sector including all properties.

        Returns:
            AnnularSector: The copied annular sector.
        """
        return AnnularSector(
            self.center,
            self.inner_radius,
            self.outer_radius,
            self.start_angle,
            self.angle,
            plane=self.plane,
            curvature=self.curvature,
        ).match_style(self)

    def set_center(self, center: Point) -> AnnularSector:
        self._center = center
        self.set_native_anchors(self.get_native_render_anchors())
        return self

    def translated_by(self, distance: float) -> AnnularSector:
        """Moves the annular sector by the given distance in x-direction.

        Args:
            distance (float): How far to translate.

        Returns:
            AnnularSector: The translated annular sector.
        """
        return self.set_center(
            self.center.copy().translated_by(distance, self.curvature)
        )

    def set_parameters(
        self,
        inner_radius: float,
        outer_radius: float,
        start_angle: float,
        angle: float,
    ) -> AnnularSector:
        """Change multiple of the parameters of the annular sector simultaneously.

        Args:
            inner_radius (float): The new  inner radius.
            outer_radius (float): The new outer radius.
            start_angle (float): The new start angle.
            angle (float): The new angle.

        Returns:
            AnnularSector: The annular sector with the new parameters.
        """
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.start_angle = start_angle
        self.angle = angle
        self.set_native_anchors(self.get_native_render_anchors())
        return self

    def set_angle(self, angle: float) -> AnnularSector:
        """Change the angle by which the annular sector is extends.

        Args:
            angle (float): The angle in radians.

        Returns:
            AnnularSector: The annular sector with the new angle.
        """
        return self.set_parameters(
            self.inner_radius,
            self.outer_radius,
            self.start_angle,
            Point.normalize_angle(angle),
        )

    def set_start_angle(self, start_angle: float) -> AnnularSector:
        """Change at which angle the sector starts.

        Args:
            start_angle (float): The starting angle in radians.

        Returns:
            AnnularSector: The annular sector with the new start angle.
        """
        return self.set_parameters(
            self.inner_radius,
            self.outer_radius,
            Point.normalize_angle(start_angle),
            self.angle,
        )

    def rotated_by(self, angle: float) -> AnnularSector:
        """Rotates the annular sector by the given angle around the origin.

        Args:
            angle (float): The angle in radians to rotate by.

        Returns:
            AnnularSector: The rotated annular sector.
        """
        if self.center.radius == 0.0:
            return self.set_start_angle(self.start_angle + angle)

        return super().rotated_by(angle)  # type: ignore

    def set_inner_radius(self, inner_radius: float) -> AnnularSector:
        """Define the inner radius of the annular sector.

        Args:
            inner_radius (float): The new inner radius of the annular sector.

        Returns:
            AnnularSector: The annular sector with the new inner radius.
        """
        return self.set_parameters(
            inner_radius, self.outer_radius, self.start_angle, self.angle
        )

    def set_outer_radius(self, outer_radius: float) -> AnnularSector:
        """Define the outer radius of the annular sector.

        Args:
            outer_radius (float): The new outer radius of the annular sector.

        Returns:
            AnnularSector: The annular sector with the new outer radius.
        """
        return self.set_parameters(
            self.inner_radius, outer_radius, self.start_angle, self.angle
        )

    def get_native_render_anchors(self) -> list[Point]:
        inner_points = [self.center.copy()]
        if self.inner_radius > 0:
            inner_points = Arc.native_render_anchors(
                self.center,
                self.inner_radius,
                self.start_angle,
                self.angle,
                self.curvature,
            )

        outer_points = Arc.native_render_anchors(
            self.center,
            self.outer_radius,
            self.start_angle,
            self.angle,
            self.curvature,
        )

        return (
            list(outer_points)
            + list(reversed(inner_points))
            + list(outer_points[:1])
        )


class AnnularSectorStretchAngle(Animation):
    """Animate the change of the angular width that a :class:`AnnularSector`
    spans.

    Examples
    --------
    .. manim:: AnnularSectorStretchAngleExample

        from hmanim.native import AnnularSector, AnnularSectorStretchAngle, Point

        class AnnularSectorStretchAngleExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the sector.
                sector = AnnularSector(
                    center=Point(),
                    inner_radius=1.0,
                    outer_radius=3.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane
                )
                self.add(sector)

                # Stretch the sector.
                self.play(
                    AnnularSectorStretchAngle(
                        sector,
                        angle=TAU / 4,
                        run_time=3
                    )
                )
    """

    def __init__(
        self,
        sector: AnnularSector,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        self.angle = angle
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(sector, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        current_angle = self.starting_mobject.angle * (  # type: ignore
            1.0 - self.rate_func(alpha)
        ) + self.angle * self.rate_func(alpha)

        self.mobject.set_angle(current_angle)


class AnnularSectorStretchRadiiAndAngleInverse(Animation):
    """
    Like stretch angle but stretches in the inverse direction and adjusts the
    radii simultaneously.

    Examples
    --------
    .. manim:: AnnularSectorStretchRadiiAndAngleInverseExample

        from hmanim.native import AnnularSector, AnnularSectorStretchRadiiAndAngleInverse, Point

        class AnnularSectorStretchRadiiAndAngleInverseExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the sector.
                sector = AnnularSector(
                    center=Point(),
                    inner_radius=1.0,
                    outer_radius=3.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane
                )
                self.add(sector)

                # Stretch the sector.
                self.play(
                    AnnularSectorStretchRadiiAndAngleInverse(
                        sector,
                        inner_radius=2.0,
                        angle=TAU / 4,
                        run_time=3
                    )
                )

    """

    def __init__(
        self,
        sector: AnnularSector,
        angle: float | None = None,
        inner_radius: float | None = None,
        outer_radius: float | None = None,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.angle = angle
        if self.angle is None:
            self.angle = sector.angle
        self.inner_radius = inner_radius
        if self.inner_radius is None:
            self.inner_radius = sector.inner_radius
        self.outer_radius = outer_radius
        if self.outer_radius is None:
            self.outer_radius = sector.outer_radius
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(sector, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        assert self.angle is not None
        assert self.inner_radius is not None
        assert self.outer_radius is not None

        current_angle = self.starting_mobject.angle * (
            1.0 - self.rate_func(alpha)  # type: ignore
        ) + self.angle * self.rate_func(alpha)
        angle_distance = self.starting_mobject.angle - current_angle

        current_inner_radius = self.starting_mobject.inner_radius * (
            1.0 - self.rate_func(alpha)  # type: ignore
        ) + self.inner_radius * self.rate_func(alpha)

        current_outer_radius = self.starting_mobject.outer_radius * (
            1.0 - self.rate_func(alpha)  # type: ignore
        ) + self.outer_radius * self.rate_func(alpha)

        self.mobject.set_parameters(
            current_inner_radius,
            current_outer_radius,
            self.starting_mobject.start_angle + angle_distance,
            current_angle,
        )


class AnnularSectorStretchAngleInverse(
    AnnularSectorStretchRadiiAndAngleInverse
):
    """Like stretch angle but stretches in the inverse direction.

    Examples
    --------
    .. manim:: AnnularSectorStretchAngleInverseExample

        from hmanim.native import AnnularSector, AnnularSectorStretchAngleInverse, Point

        class AnnularSectorStretchAngleInverseExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)

                # Draw the sector.
                sector = AnnularSector(
                    center=Point(),
                    inner_radius=1.0,
                    outer_radius=3.0,
                    start_angle=0.0,
                    angle=TAU / 8,
                    plane=plane
                )
                self.add(sector)

                # Stretch the sector.
                self.play(
                    AnnularSectorStretchAngleInverse(
                        sector,
                        angle=TAU / 4,
                        run_time=3
                    )
                )
    """

    def __init__(
        self,
        sector: AnnularSector,
        angle: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(
            sector,
            angle=angle,
            run_time=run_time,
            apply_function_kwargs=apply_function_kwargs,
            **kwargs,
        )
