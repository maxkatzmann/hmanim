from math import sqrt

import numpy as np
from colour import Color
from manim import (
    ImageMobject,
    ManimColor,
    color_to_int_rgba,
    config,
    interpolate_color,
)


class Background(ImageMobject):
    """A radial gradient background that can be used to visualize the
    exponential expansion of space.

    Examples
    --------
    .. manim:: BackgroundExample
        :save_last_frame:

        from colour import Color
        from hmanim.native import Background

        class BackgroundExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                background = Background(
                    Color("#0021FF"),
                    Color("#D13B1D"),
                    expansion=0.25
                ).scale(2)

                self.add(background)
    """

    def __init__(
        self,
        inner_color: Color,
        outer_color: Color,
        width: int = 270,
        height: int = 270,
        expansion: float = 0.5,
    ):
        """
        Creates an :class:`Background` (which is an :class:`ImageMobject`) that
        shows a radial gradient with the `inner_color` in the center, that is
        interpolated to the `outer_color` towards the edge of the image.

        The `size` determines the how many pixels are used to render the
        gradient.  Eventually, the image is scaled to fill a 1920x1920 canvas.

        The `expansion` is a value in [0, inf] that determines how quickly the
        gradient expands.  Values closer to 0 lead to a faster expansion, while
        values larger than 1 lead to a slower expansion.

        """
        size = max(width, height)
        x_axis = np.linspace(-1, 1, size)[:, None]
        y_axis = np.linspace(-1, 1, size)[None, :]

        intensities = np.power(
            np.sqrt(x_axis**2 + y_axis**2) / sqrt(2), expansion
        )
        intensities = [[min(x, 1) for x in arr] for arr in intensities]

        # Cut off edges to get the preferred size
        x_extension = int((size - width) / 2)
        intensities = [
            arr[x_extension : size - x_extension] for arr in intensities
        ]
        y_extension = int((size - height) / 2)
        intensities = intensities[y_extension : size - y_extension]

        pixel_array = np.uint8(
            [
                [
                    color_to_int_rgba(
                        interpolate_color(
                            ManimColor(inner_color),  # type: ignore
                            ManimColor(outer_color),  # type: ignore
                            alpha,
                        )
                    )
                    for alpha in x
                ]
                for x in intensities
            ]
        )

        super().__init__(pixel_array)
        self.scale(1080 / size * config.aspect_ratio)
