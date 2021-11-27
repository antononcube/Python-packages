import random

import bezier
import matplotlib
import matplotlib.pyplot
import numpy
import seaborn
import math

from matplotlib.artist import Artist


class RandomMandala:
    _figure = None
    _axes = None
    _radius: float = 10
    _angle: float = numpy.pi / 6,
    _keep_grid_points: bool = False
    _seed_points = None
    _sym_seed_points = None
    _symmetric = False
    _points = None
    _value = None

    # ===========================================================
    # Initialize
    # ===========================================================
    def __init__(self, *args, **kwargs):

        if len(args) > 0:
            self._figure = args[0]

        if len(kwargs) > 0 and "figure" in kwargs:
            self._figure = kwargs["figure"]

    # ===========================================================
    # Takers
    # ===========================================================
    def take_figure(self):
        return self._figure

    def take_axes(self):
        return self._axes

    def take_seed_points(self):
        return self._seed_points

    def take_points(self):
        return self._points

    def take_angle(self):
        return self._angle

    def take_symmetric(self):
        return self._symmetric

    def take_value(self):
        return self._value

    # ===========================================================
    # Random seed segment
    # ===========================================================
    def make_seed_segment(self,
                          radius: float = 10.,
                          angle=numpy.pi / 6,
                          n: int = 10,
                          keep_grid_points=False):
        t1 = [radius * r * math.cos(angle) for r in numpy.arange(0, 1, 1 / n)]
        t2 = [radius * r * math.sin(angle) for r in numpy.arange(0, 1, 1 / n)]
        b = [(radius * r, 0) for r in numpy.arange(0, 1, 1 / n)]
        # t = list(zip(list(zip(t1, t2)), b))
        t = list(zip(t1, t2)) + b
        self._radius = radius
        self._angle = angle
        self._keep_grid_points = keep_grid_points
        self._seed_points = random.sample(t, len(t))
        self._value = self._seed_points
        return self

    # ===========================================================
    # Symmetric seed segment
    # ===========================================================
    def make_seed_symmetric(self, arg=None):
        if isinstance(arg, bool) and not arg:
            return self
        self._sym_seed_points = [(x[0], -x[1]) for x in self._seed_points]
        self._symmetric = True
        self._value = self._seed_points
        return self

    # ===========================================================
    # To Bezier curve
    # ===========================================================
    def to_nodes(self, points):
        nodes = numpy.array(points).transpose()
        self._value = nodes
        return self

    # ===========================================================
    # To Bezier curve
    # ===========================================================
    def to_bezier_curve(self, points):
        nodes = numpy.array(points).transpose()

        curve = bezier.Curve.from_nodes(nodes)
        self._value = curve
        return self

    # ===========================================================
    # Rotate and fill
    # ===========================================================
    def rotate_and_fill(self,
                        face_color="0.2",
                        edge_color=None,
                        location=111,
                        ax = None):
        # Make figure and axes
        if ax is None:
            if self._figure is None:
                fig, local_ax = matplotlib.pyplot.subplots()
            else:
                fig = self._figure
                if isinstance(location, tuple):
                    local_ax = fig.add_subplot(*location)
                else:
                    local_ax = fig.add_subplot(location)
        else:
            local_ax = ax
            fig = self._figure

        # Determine rotation angle and seed nodes
        alpha = self._angle
        nodes = self._seed_points

        if self._symmetric:
            alpha = 2 * alpha
            nodes = nodes + self._sym_seed_points

        nodes = numpy.array(nodes).transpose()

        # Rotation matrix
        rotMat = [[math.cos(alpha), -math.sin(alpha)], [math.sin(alpha), math.cos(alpha)]]

        # First nodes and plot
        if face_color is None:
            local_ax.plot(nodes[0], nodes[1], color=edge_color)
        else:
            local_ax.fill(nodes[0], nodes[1], fc=face_color, ec=edge_color)

        # Incremental rotation and plotting
        for i in range(1, math.floor(2 * numpy.pi / alpha)):
            nodes = numpy.dot(rotMat, nodes)
            if face_color is None:
                local_ax.plot(nodes[0], nodes[1], color=edge_color)
            else:
                local_ax.fill(nodes[0], nodes[1], fc=face_color, ec=edge_color)

        # Just mandala plot
        local_ax.set_aspect('equal')
        local_ax.axis('off')

        # Set figure, axes, value
        self._figure = fig
        self._axes = local_ax
        self._value = local_ax

        return self

    # ===========================================================
    # Rotate and bezier
    # ===========================================================
    def rotate_and_bezier(self,
                          face_color="0.2",
                          edge_color="0.2",
                          location=111,
                          ax=None):
        # Make figure and axes
        if ax is None:
            if self._figure is None:
                fig, local_ax = matplotlib.pyplot.subplots()
            else:
                fig = self._figure
                if isinstance(location, tuple):
                    local_ax = fig.add_subplot(*location)
                else:
                    local_ax = fig.add_subplot(location)
        else:
            local_ax = ax
            fig = self._figure

        # Determine rotation angle and seed nodes
        alpha = self._angle
        nodes = numpy.array(self._seed_points).transpose()

        if self._symmetric:
            alpha = 2 * alpha

        # Rotation matrix
        rotMat = [[math.cos(alpha), -math.sin(alpha)], [math.sin(alpha), math.cos(alpha)]]

        # First nodes and plot
        curve = bezier.Curve.from_nodes(nodes)
        _ = curve.plot(num_pts=256, color=edge_color, ax=local_ax)

        # Incremental rotation and plotting
        for i in range(1, math.floor(2 * numpy.pi / alpha)):
            nodes = numpy.dot(rotMat, nodes)
            curve = bezier.Curve.from_nodes(nodes)
            _ = curve.plot(num_pts=256, ax=local_ax, color=edge_color)

        # Symmetric case
        if self._symmetric:
            nodes = numpy.array(self._sym_seed_points).transpose()
            curve = bezier.Curve.from_nodes(nodes)
            _ = curve.plot(num_pts=256, ax=local_ax, color=edge_color)
            for i in range(1, math.floor(2 * numpy.pi / alpha)):
                nodes = numpy.dot(rotMat, nodes)
                curve = bezier.Curve.from_nodes(nodes)
                _ = curve.plot(num_pts=256, ax=local_ax, color=edge_color)

        # Just mandala plot
        local_ax.set_aspect('equal')
        local_ax.axis('off')

        # Set figure, axes, value
        self._figure = fig
        self._axes = local_ax
        self._value = local_ax

        return self

    # ===========================================================
    # Rotate and fill bezier polygon
    # ===========================================================
    def rotate_and_bezier_fill(self,
                               face_color=(0.01, 0.01, 0.01),
                               edge_color=(0.01, 0.01, 0.01),
                               pts_per_edge=24,
                               location=111,
                               ax=None):

        # Make figure and axes
        if ax is None:
            if self._figure is None:
                fig, local_ax = matplotlib.pyplot.subplots()
            else:
                fig = self._figure
                if isinstance(location, tuple):
                    local_ax = fig.add_subplot(*location)
                else:
                    local_ax = fig.add_subplot(location)
        else:
            fig = self._figure
            local_ax = ax

        # Determine rotation angle and seed nodes
        alpha = self._angle
        if self._symmetric:
            alpha = 2 * alpha

        nodes1 = numpy.array(self._seed_points).transpose()
        if len(self._seed_points) < 4:
            nodes1con = numpy.array([self._seed_points[-1], self._seed_points[0]]).transpose()
        else:
            nodes1con = numpy.array([self._seed_points[-1],
                                     # self._seed_points[-2],
                                     # self._seed_points[1],
                                     self._seed_points[0]]).transpose()

        # Rotation matrix
        rotMat = [[math.cos(alpha), -math.sin(alpha)], [math.sin(alpha), math.cos(alpha)]]

        # First nodes and plot
        curve1 = bezier.Curve.from_nodes(nodes1)
        curve1con = bezier.Curve.from_nodes(nodes1con)
        curved_poly = bezier.CurvedPolygon(curve1, curve1con)

        _ = curved_poly.plot(pts_per_edge=pts_per_edge, ax=local_ax, color=face_color)

        # Incremental rotation and plotting
        for i in range(1, math.floor(2 * numpy.pi / alpha)):
            nodes1 = numpy.dot(rotMat, nodes1)
            nodes1con = numpy.dot(rotMat, nodes1con)
            curve1 = bezier.Curve.from_nodes(nodes1)
            curve1con = bezier.Curve.from_nodes(nodes1con)
            curved_poly = bezier.CurvedPolygon(curve1, curve1con)
            _ = curved_poly.plot(pts_per_edge=pts_per_edge, ax=local_ax, color=face_color)

        if self._symmetric:
            self._figure = fig
            self._axes = local_ax
            self._symmetric = False
            self._angle = 2 * self._angle
            self._sym_seed_points, self._seed_points = self._seed_points, self._sym_seed_points

            self.rotate_and_bezier_fill(face_color=face_color,
                                        edge_color=edge_color,
                                        pts_per_edge=pts_per_edge,
                                        ax=local_ax)

            self._sym_seed_points, self._seed_points = self._seed_points, self._sym_seed_points
            self._symmetric = True
            self._angle = self._angle / 2

        # Just mandala plot
        local_ax.set_aspect('equal')
        local_ax.axis('off')

        # Proper scaling
        # local_ax.set_xscale("linear")
        # print(self._radius)
        # local_ax.set_xlim([-self._radius, self._radius])
        # local_ax.set_ylim([-self._radius, self._radius])

        # Set figure, axes, value
        self._figure = fig
        self._axes = local_ax
        self._value = local_ax

        return self

    # ===========================================================
    # Plot
    # ===========================================================
    def plot(self):
        matplotlib.pyplot.plot()
