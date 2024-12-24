# HManim

The hyperbolic extension of [Manim](https://www.manim.community). This package
allows for using Manim's drawing and animation framework to visualize objects
in the hyperbolic plane.

For a comprehensive description we refer to the [documentation](https://maxkatzmann.github.io/hmanim/).

## Installation

You can install the package by running

``` bash
pip install hmanim
```

Note that we recommend installing HManim in a virtual environment.

## Usage

Define a scene in a Python file (e.g., `scene.py`), define a class that derives
from Manim's `Scene`, and override its `construct` method.

``` python
from hmanim import native
from manim import Scene, PolarPlane

class ExampleScene(Scene):
    def construct(self):
        plane = PolarPlane(size=5)

        circle = native.Circle(
            center=native.Point(),
            radius=5.0,
            plane=plane,
        )

        self.add(circle)
        self.play(native.Translate(circle, 3.0))
```

Then you render the scene by running

``` bash
python -m manim -p scene.py ExampleScene
```

Note that `-p` is used to show a preview of the created video once it is
rendered.

The resulting files can then be found in the created `media` directory.

For more examples, we refer to the
[documentation](https://maxkatzmann.github.io/hmanim/).

## Building the Documentation

The documentation content is split into two directories.

1. The `documentation` directory contains the source files that are used to
   build the documentation.
2. The `docs` directory contains the built documentation files that are served
   as a website.

To build the documentation, go to the `documentation` directory and run `make
html`.

## Known Issues

Changing the center of projection of an `HArc` or `HClosedArc` may lead to
graphical glitches, since the rendering is not optimized for projection changes yet.

The Poincaré module is currently missing the functionality to draw hyperbolic circles.
