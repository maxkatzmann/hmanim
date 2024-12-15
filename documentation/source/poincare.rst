
Poincaré Module
===============

This module contains the objects that are used to visualize
elements in the `Poincaré disk model
<https://en.wikipedia.org/wiki/Poincaré_disk_model>`_ of the
hyperbolic plane. It represents the entirety of the
hyperbolic plane in the interior of the Euclidean unit
circle. Lines are represented as circular arcs that meet the
boundary of the unit circular orthogonally and hyperbolic
circle are equivalent to Euclidean circles with their
centers shifted.

.. note::

   At the moment, HManim does not support drawing hyperbolic
   circles in the Poincaré disk model.


Example
-------
    .. manim:: PoincareExample
        :save_last_frame:

        from hmanim.poincare import Disk, Dot, Line, Point

        class PoincareExample(Scene):
            def construct(self):
                # How we represent the unit disk
                disk = Disk(
                    radius=3,
                    color=WHITE,
                )
                self.add(disk)

                # The origin
                origin_dot = Dot(
                  Point(),
                  disk=disk,
                )
                self.add(origin_dot)

                # Two dots and a line between them
                p1 = Point(0.75, 0.0)
                p2 = Point(-0.25, 0.5)

                line = Line(
                  p1,
                  p2,
                  disk=disk,
                  color=BLUE,
                )
                self.add(line)

                self.add(
                  Dot(
                    p1,
                    disk=disk,
                    color=YELLOW,
                  )
                )

                self.add(
                  Dot(
                    p2,
                    disk=disk,
                    color=RED,
                  )
                )

Usage
-----

Drawing objects in the hyperbolic plane always starts with a
:doc:`poincare/disk` object. Every object lives in such a disk and is assigned
a `disk` parameter upon initialization, as shown in the example above.

Overview
--------

.. toctree::
   :maxdepth: 2
   :glob:

   poincare/*

