Welcome to HManim's documentation!
==================================

HManim is the hyperbolic extension of `Manim <https://www.manim.community/>`_.
It provides functionality for drawing and animating objects in the `hyperbolic plane
<https://en.wikipedia.org/wiki/Hyperbolic_geometry>`_.

HManim is open-source, with the code being available on `GitHub
<https://github.com/maxkatzmann/hmanim>`_.
Contributions are welcome!

The package provides two modules. The :doc:`native` allows for visualizations
in the native representation of the hyperbolic plane. It is the more
comprehensive of the two. In addition, the :doc:`poincare` allows for
visualizations in the Poincaré disk model. We refer to the documentation of the
individual models for further details.

Showcase
--------

The framework has been used to render the slides in the
following video:

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/OuHBBrLgHII" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

The corresponding code can be found on `GitHub <https://github.com/maxkatzmann/disputation>`_.

Example
-------

.. manim:: OverviewExample
    :save_last_frame:

    from hmanim import native
    from hmanim import poincare


    class OverviewExample(Scene):
        def construct(self):
            # We draw the native representation on the left.

            # Define the plane that all our hyperbolic objects live in.
            plane = PolarPlane(
               radius_max=5.0,
               size=5,
            ).to_edge(LEFT)
            self.add(plane)

            native_title = (
               Text("Native")
                  .next_to(plane, UP)
                  .shift(UP * 0.5)
            )
            self.add(native_title)

            circle_center = native.Point(3, 0)
            dot = native.Dot(
               center=circle_center,
               plane=plane,
               color=YELLOW,
            )
            self.add(dot)
            circle = native.Circle(
               center=circle_center,
               radius=4,
               plane=plane,
               color=YELLOW,
            )
            self.add(circle)

            start_point = native.Point(4, TAU * 3 / 8)
            self.add(
               native.Dot(
                  start_point,
                  plane=plane,
                  color=RED,
               )
            )
            end_point = native.Point(5, TAU * 5 / 8)
            self.add(
               native.Dot(
                  end_point,
                  plane=plane,
                  color=RED,
               )
            )

            line = native.Line(
               start_point=start_point,
               end_point=end_point,
               plane=plane,
               color=RED,
            )
            self.add(line)

            # We draw the Poincaré disk representation on the right.
            
            # How we represent the unit disk
            disk = poincare.Disk(
                radius=2.5,
                color=WHITE,
            ).to_edge(RIGHT)

            poincare_group = VGroup(disk,)
            self.add(disk)

            poincare_title = (
               Text("Poincaré Disk")
                  .next_to(disk, UP)
                  .shift(UP * 0.5)
            )
            self.add(poincare_title)
 
            # The origin
            origin_dot = poincare.Dot(
              poincare.Point(),
              disk=disk,
            )
            self.add(origin_dot)
 
            # Two dots and a line between them
            p1 = poincare.Point(0.75, 0.0)
            p2 = poincare.Point(-0.25, 0.5)
 
            line = poincare.Line(
              p1,
              p2,
              disk=disk,
              color=BLUE,
            )
            self.add(line)
 
            self.add(
              poincare.Dot(
                p1,
                disk=disk,
                color=YELLOW,
              )
            )
 
            self.add(
              poincare.Dot(
                p2,
                disk=disk,
                color=RED,
              )
            )

Installation
------------

To install HManim, simply run

.. code-block:: bash

   pip install hmanim

.. note::
   We recommend installing HManim in a virtual environment.

Usage
-----

Once installed, you can use HManim by creating a Python file (e.g.,
``scene.py``), defining a class that derives from Manim's ``Scene``, and
overriding its ``construct`` method.

.. code-block:: python

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


Then you render the scene by running

.. code-block:: bash

   python -m manim -p scene.py ExampleScene

.. note::
   Here the flag `-p` is used to show a preview of the created video once it is
   rendered.

The resulting files can then be found in the created `media` directory.

For more examples, we refer to the documentation of the individual modules.

Modules
-------

.. toctree::
   :maxdepth: 2

   native
   poincare


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
