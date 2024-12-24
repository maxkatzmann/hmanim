from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Optional, Sequence

from manim import WHITE, Animation, Group, PolarPlane

from .dot import Dot
from .line import Line
from .point import Point


class Graph(Group):
    """
    A graph consists of vertices (associated with
    :class:`hmanim.native.point.Points`) and edges (line segments between the
    points).  The edges are drawn along the hyperbolic geodesics between the
    vertices.

    Parameters
    ----------
    adjacencies
        A dictionary of the form `{vertex: [adjacent_vertices]}`. Assumes that
        all vertices are addressed by their index.
    coordinates
        A list of :class:`hmanim.native.point.Point` objects representing the
        coordinates of the vertices. The i-th entry is assumed to belong to
        vertex i.
    using_geodesics
        A boolean indicating whether the edges should be drawn along the
        hyperbolic geodesics. If `False`, the edges are drawn as straight
        lines.  Default is `True`.
    curvature
        A `float` representing the curvature of the hyperbolic plane that the
        graph lives in. Default is -1.
    vertex_radius
        A `float` representing the size of the :class:`Dot` objects representing
        the vertices. Default is 0.075.
    vertex_color
        The color of the :class:`Dot` objects representing the vertices. Default
        is `WHITE`.
    vertex_opacity
        The opacity of the :class:`Dot` objects representing the vertices.
        Default is 1.0.
    edge_stroke_width
        The width of the edges. Default is 4.0.
    edge_color
        The color of the edges. Default is `WHITE`.
    edge_opacity
        The opacity of the edges. Default is 1.0.


    Examples
    --------

    .. manim:: GraphExample
        :save_last_frame:

        from hmanim.native import Graph, Point

        class GraphExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)
                self.add(plane)

                graph = Graph(
                    adjacencies={
                        0: [1, 2],
                        1: [0],
                        2: [0],
                    },
                    coordinates=[
                        Point(2, TAU / 8),
                        Point(3, 0),
                        Point(1, TAU / 4),
                    ],
                    plane=plane,
                    vertex_color=YELLOW,
                    edge_color=YELLOW,
                )

                self.add(graph)
    """

    @staticmethod
    def read_edge_list_from_file(edge_list_path: str) -> dict[int, list[int]]:
        """Reads an edge list from a file and returns a dictionary of the form
        `{vertex: [adjacent_vertices]}`. Assumes that each line in the file
        represents one edge consisting of two integers separated by a space.
        Additionally, assumes that the graph is undirected and that each edge is
        only listed in one direction.

        Args:
            edge_list_path (str): The path to the edge list file.

        Returns:
            dict[int, list[int]]: The adjacency list of the graph.
        """
        graph = defaultdict(list)
        with open(edge_list_path, "r") as edge_list_file:
            edge_list = edge_list_file.readlines()
            for edge in edge_list:
                vertices = [int(x) for x in edge.split()]
                graph[vertices[0]].append(vertices[1])
                graph[vertices[1]].append(vertices[0])

        return graph

    @staticmethod
    def read_coordinates_from_file(coordinate_list_path: str) -> list[Point]:
        """Reads a list of coordinates from a file and returns a list of
        :class:`hmanim.native.point.Point` objects. Assumes that each line in
        the file represents one coordinate consisting of two floats separated by
        a space.  Assumes that the coordinates are given in polar coordinates.

        Args:
            coordinate_list_path (str): The path to the coordinate list file.

        Returns:
            list[hmanim.native.point.Point]: The list of coordinates.
        """
        coordinates = []
        with open(coordinate_list_path, "r") as coordinate_list_file:
            coordinate_list = coordinate_list_file.readlines()
            for coordinate in coordinate_list:
                values = [float(x) for x in coordinate.split()]
                coordinates.append(Point(radius=values[0], azimuth=values[1]))

        return coordinates

    @staticmethod
    def from_files(
        edge_list_path: str,
        coordinate_list_path: str,
        plane: PolarPlane,
        using_geodesic: bool = True,
        curvature: float = -1,
        **kwargs,
    ) -> Graph:
        """Creates a :class:`Graph` from a file containing an edge list and a
        file containing a list of coordinates. See
        :meth:`read_edge_list_from_file` and :meth:`read_coordinates_from_file`
        for more information.

        Args:
            edge_list_path (str): The path to the edge list file.
            coordinate_list_path (str): The path to the coordinate list file.
            plane (PolarPlane): The plane that the graph lives in.
            using_geodesic (bool, optional): Whether edges should be drawn using
                hyperbolic geodesics or straight lines instead. Defaults to True.
            curvature (float, optional): The curvature of the hyperbolic plane
                that the graph is living in. Defaults to -1.

        Returns:
            Graph: The graph representing the passed edge list and coordinate list.
        """
        # Reading the edge list
        adjacencies = Graph.read_edge_list_from_file(edge_list_path)

        # Reading the coordinates
        coordinates = Graph.read_coordinates_from_file(coordinate_list_path)

        return Graph(
            adjacencies,
            coordinates,
            plane=plane,
            using_geodesic=using_geodesic,
            curvature=curvature,
            **kwargs,
        )

    def __init__(
        self,
        adjacencies: dict[int, list[int]],
        coordinates: Sequence[Point],
        plane: PolarPlane,
        using_geodesic: bool = True,
        curvature: float = -1,
        vertex_radius: float = 0.075,
        vertex_color=WHITE,
        vertex_opacity: float = 1.0,
        edge_stroke_width: float = 4.0,
        edge_color=WHITE,
        edge_opacity: float = 1.0,
        **kwargs,
    ):
        self.plane = plane
        self.z_index = kwargs.get("z_index", 0)
        self.curvature = curvature
        self.using_geodesic = using_geodesic

        self.adjacencies = adjacencies
        self.coordinates = coordinates

        self.edge_map = {}
        self.edges = self._create_edges()
        self.set_edge_stroke_width(edge_stroke_width)
        self.set_edge_color(edge_color, edge_opacity)

        self.vertices = self._create_vertices()
        self.set_vertex_radius(vertex_radius)
        self.set_vertex_color(vertex_color, vertex_opacity)

        graph_objects = self.edges + self.vertices
        super().__init__(*graph_objects, **kwargs)

    def copy(self) -> Graph:
        return Graph(
            self.adjacencies,
            self.coordinates,
            self.plane,
            self.using_geodesic,
            self.curvature,
            self.vertex_radius,
            self.vertex_color,
            self.vertex_opacity,
            self.edge_stroke_width,
            self.edge_color,
            self.edge_opacity,
            z_index=self.z_index,
        )

    def set_vertex_radius(self, radius: float) -> Graph:
        """Changes the radius of :class:`Dot` objects representing the vertices.

        Args:
            radius (float): The new radius of the :class:`Dot` objects.

        Returns:
            Graph: The graph with the new vertex radius.
        """
        self.vertex_radius = radius
        for vertex in self.vertices:
            vertex.set_radius(radius)

        return self

    def set_vertex_color(self, color, opacity: float = 1.0) -> Graph:
        """Changes the color of :class:`Dot` objects representing the vertices.

        Args:
            color: The new color of the :class:`Dot` objects.
            opacity (float, optional): The opacity of the :class:`Dot` objects.
                Defaults to 1.0.

        Returns:
            Graph: The graph with the new vertex color.
        """
        self.vertex_color = color
        self.vertex_opacity = opacity
        for vertex in self.vertices:
            vertex.set_fill(color, opacity=opacity)

        return self

    def set_edge_color(self, color, opacity: float = 1.0) -> Graph:
        """Changes the color of the edges.

        Args:
            color: The new color of the edges.
            opacity (float, optional): The new opacity of the edges. Defaults to 1.0.

        Returns:
            Graph: The graph with the new edge color.
        """
        self.edge_color = color
        self.edge_opacity = opacity

        for edge in self.edges:
            edge.set_stroke(color, opacity=opacity)

        return self

    def set_edge_stroke_width(self, stroke_width: float) -> Graph:
        """Changes the stroke width of the edges.

        Args:
            stroke_width (float): The new stroke width of the edges.

        Returns:
            Graph: The graph with the new edge stroke width.
        """
        self.edge_stroke_width = stroke_width
        for edge in self.edges:
            edge.set_stroke_width(stroke_width)

        return self

    def _create_vertices(self) -> list[Dot]:
        return [
            Dot(x, self.plane, z_index=self.z_index) for x in self.coordinates
        ]

    def _create_edges(self) -> list[Line]:
        edges = []
        self.edge_map = {}
        for vertex, neighbors in self.adjacencies.items():
            start_point = self.coordinates[vertex]

            for neighbor in neighbors:
                if neighbor < vertex:
                    continue

                end_point = self.coordinates[neighbor]
                self.edge_map[(vertex, neighbor)] = len(edges)
                self.edge_map[(neighbor, vertex)] = len(edges)
                edges.append(
                    Line(
                        start_point,
                        end_point,
                        plane=self.plane,
                        using_geodesic=self.using_geodesic,
                        curvature=self.curvature,
                        z_index=self.z_index,
                    )
                )

        return edges

    def get_edge(self, u: int, v: int) -> Line | None:
        """Get the :class:`native.Line` representing the edge between vertices u and v.

        Args:
            u (int): The index of the first vertex.
            v (int): The index of the second vertex.

        Returns:
            hmanim.native.line.Line | None: The :class:`native.Line`
                representing the edge between vertices u and v.  None if the
                edge does not exist.
        """
        if not (u, v) in self.edge_map:
            return None

        edge_index = self.edge_map[(u, v)]
        return self.edges[edge_index]

    def set_center_of_projection(self, point: Point) -> Graph:
        """Change the center of projection of the graph.

        Args:
            point (hmanim.native.point.Point): The new center of projection.

        Returns:
            Graph: The graph with the new center of projection.
        """
        for edge in self.edges:
            edge.set_center_of_projection(point)

        for vertex in self.vertices:
            vertex.set_center_of_projection(point)

        return self

    def set_curvature(self, curvature: float) -> Graph:
        """Change the curvature of the hyperbolic plane that the graph lives in.
        Only affects the graph and not the other objects associated with the
        plane.

        Args:
            curvature (float): The new curvature of the hyperbolic plane.

        Returns:
            Graph: The graph with the new curvature.
        """
        self.curvature = curvature

        for edge in self.edges:
            edge.set_curvature(curvature)

        return self


class GraphSetCurvature(Animation):
    """Change the curvature of the hyperbolic plane that the
    graph lives in.

    Examples
    --------

    .. manim:: GraphSetCurvatureExample

        from hmanim.native import Graph, GraphSetCurvature, Point

        class GraphSetCurvatureExample(Scene):
            def construct(self):
                # The plane that all our hyperbolic objects live in.
                plane = PolarPlane(size=5)
                self.add(plane)

                graph = Graph(
                    adjacencies={
                        0: [1, 2],
                        1: [0],
                        2: [0],
                    },
                    coordinates=[
                        Point(2, TAU / 8),
                        Point(3, 0),
                        Point(1, TAU / 4),
                    ],
                    plane=plane,
                    vertex_color=YELLOW,
                    edge_color=YELLOW,
                )

                self.play(
                    GraphSetCurvature(
                        graph,
                        -0.001,
                    )
                )
    """

    def __init__(
        self,
        graph: Graph,
        curvature: float,
        run_time: float = 3,
        apply_function_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """Animate changing the curvature of the polygon."""
        self.curvature = curvature
        self.apply_function_kwargs = (
            apply_function_kwargs if apply_function_kwargs is not None else {}
        )

        super().__init__(graph, run_time=run_time, **kwargs)

    def interpolate_mobject(self, alpha: float):
        # The current angle we are rotating.
        new_curvature = (
            self.rate_func(alpha) * self.curvature
            + (1.0 - self.rate_func(alpha))
            * self.starting_mobject.curvature  # type: ignore
        )

        # The translated polygon.  We need to create copies, since we don't
        # want to modify the start_chain.
        self.mobject.set_curvature(new_curvature)
