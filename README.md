# HManim

The hyperbolic extension of [Manim](https://www.manim.community). This package
allows for using Manim's drawing and animation framework to visualize objects
in the hyperbolic plane.

For a comprehensive description we refer to the documentation. (TODO: add link)

## Installation

TODO: Add installation instructions.

## Building the Documentation

Go to  the `docs` directory and run `make html`.

## Known Issues

Changing the center of projection of an `HArc` or `HClosedArc` may lead to
graphical glitches, since the rendering is not optimized for projection changes yet.

The Poincaré module is currently missing the functionality to draw hyperbolic circles.
