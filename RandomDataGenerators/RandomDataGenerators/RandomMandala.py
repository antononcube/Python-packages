import random

import bezier
import matplotlib
import numpy
import seaborn
import math

from matplotlib.artist import Artist


class RandomMandala:
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
    def __init__(self):
        pass

    # ===========================================================
    # Takers
    # ===========================================================
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
    def make_seed_symmetric(self):
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
    def rotate_and_fill(self, face_color="0.2", edge_color=None):
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
        matplotlib.pyplot.fill(nodes[0], nodes[1], fc=face_color, ec=edge_color)

        # Incremental rotation and plotting
        for i in range(1, math.floor(2 * numpy.pi / alpha)):
            nodes = numpy.dot(rotMat, nodes)
            matplotlib.pyplot.fill(nodes[0], nodes[1], fc=face_color, ec=edge_color)

        # Result
        self._value = nodes

        return self

    # ===========================================================
    # Rotate and bezier
    # ===========================================================
    def rotate_and_bezier(self, face_color="0.2", edge_color="0.2"):
        # Determine rotation angle and seed nodes
        alpha = self._angle
        nodes = numpy.array(self._seed_points).transpose()

        if self._symmetric:
            alpha = 2 * alpha

        # Rotation matrix
        rotMat = [[math.cos(alpha), -math.sin(alpha)], [math.sin(alpha), math.cos(alpha)]]

        # First nodes and plot
        curve = bezier.Curve.from_nodes(nodes)
        ax: Artist = curve.plot(num_pts=256, color=edge_color)

        # Incremental rotation and plotting
        for i in range(1, math.floor(2 * numpy.pi / alpha)):
            nodes = numpy.dot(rotMat, nodes)
            curve = bezier.Curve.from_nodes(nodes)
            _ = curve.plot(num_pts=256, ax=ax, color=edge_color)

        # Symmetric case
        if self._symmetric:
            nodes = numpy.array(self._sym_seed_points).transpose()
            curve = bezier.Curve.from_nodes(nodes)
            _ = curve.plot(num_pts=256, ax=ax, color=edge_color)
            for i in range(1, math.floor(2 * numpy.pi / alpha)):
                nodes = numpy.dot(rotMat, nodes)
                curve = bezier.Curve.from_nodes(nodes)
                _ = curve.plot(num_pts=256, ax=ax, color=edge_color)

        return self

    # ===========================================================
    # Rotate and fill bezier polygon
    # ===========================================================
    def rotate_and_bezier_fill(self, face_color=(0.01, 0.01, 0.01), edge_color="0.2", pts_per_edge=12, ax=None):

        # Determine rotation angle and seed nodes
        alpha = 2 * self._angle
        nodes1 = numpy.array(self._seed_points).transpose()
        nodes1con = numpy.array([self._seed_points[-1], self._seed_points[0]]).transpose()

        # Rotation matrix
        rotMat = [[math.cos(alpha), -math.sin(alpha)], [math.sin(alpha), math.cos(alpha)]]

        # First nodes and plot
        curve1 = bezier.Curve.from_nodes(nodes1)
        curve1con = bezier.Curve.from_nodes(nodes1con)
        curved_poly = bezier.CurvedPolygon(curve1, curve1con)

        if ax is None:
            local_ax: Artist = curved_poly.plot(pts_per_edge=pts_per_edge, color=face_color)
        else:
            local_ax = ax
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
            self._symmetric = False
            self._sym_seed_points, self._seed_points = self._seed_points, self._sym_seed_points

            self.rotate_and_bezier_fill(face_color=face_color,
                                        edge_color=edge_color,
                                        pts_per_edge=pts_per_edge,
                                        ax=local_ax)

            self._sym_seed_points, self._seed_points = self._seed_points, self._sym_seed_points
            self._symmetric = True

        return self

    # ===========================================================
    # Plot
    # ===========================================================
    def plot(self):
        matplotlib.pyplot.plot()
