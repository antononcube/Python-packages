# Follows the tests in
#   https://resources.wolframcloud.com/FunctionRepository/resources/ChernoffFace/

import random
import unittest

import matplotlib
import matplotlib.cm
import numpy.random
from ChernoffFace.ChernoffFace import chernoff_face_parts_parameters
from ChernoffFace.ChernoffFunctions import chernoff_face
from matplotlib import figure


def _is_num_list(obj):
    return isinstance(obj, list) and all([isinstance(x, int) or isinstance(x, float) for x in obj])


def _is_figure(obj):
    return isinstance(obj, matplotlib.figure.Figure)


def _is_figure_list(obj):
    return isinstance(obj, list) and all([_is_figure(x) for x in obj])


class ChernoffFaces(unittest.TestCase):

    def test_single_chernoff_face_1(self):
        vec = [random.random() for i in range(12)]
        res = chernoff_face(vec)
        self.assertTrue(_is_figure(res))

    def test_single_chernoff_face_2(self):
        vec = [random.random() for i in range(120)]
        res = chernoff_face(vec)
        self.assertTrue(_is_figure(res))

    def test_single_chernoff_face_3(self):
        vec = [random.random() for i in range(12)]
        myKeys = list(chernoff_face_parts_parameters())[0:len(vec)]
        myDict = dict(zip(myKeys, vec))
        print(myDict)
        res = chernoff_face(myDict)
        self.assertTrue(_is_figure(res))

    def test_many_chernoff_faces_1(self):
        data = numpy.random.rand(4, 12)
        res = chernoff_face(data, color_mapper=matplotlib.cm.rainbow, make_symmetric=False)
        self.assertTrue(_is_figure(res) and len(res.axes) == 4)

    def test_many_chernoff_faces_2(self):
        data = numpy.random.rand(16, 12)
        res = chernoff_face(data, n_rows=4, make_symmetric=False)
        self.assertTrue(_is_figure(res) and len(res.axes) == 16)

    def test_many_chernoff_faces_3(self):
        data = numpy.random.rand(16, 12)
        res = chernoff_face(data, n_rows=4, n_columns=4, make_symmetric=True)
        self.assertTrue(_is_figure(res) and len(res.axes) == 16)

    def test_many_chernoff_faces_4(self):
        data = numpy.random.rand(16, 12)
        res = chernoff_face(data, long_face=True)
        self.assertTrue(_is_figure(res) and len(res.axes) == 16)

    def test_chernoff_faces_collection_1(self):
        fig = matplotlib.pyplot.figure(figsize=(6, 6), dpi=120)

        data = numpy.random.rand(16, 12)

        for i in range(4):
            fig = chernoff_face(data=data[i, :].tolist(),
                                color_mapper=matplotlib.cm.Greys,
                                figure=fig,
                                location=(1, 4, i+1))
            ax = fig.axes[-1]
            ax.set_title("index:" + str(i))

        self.assertTrue(_is_figure(fig) and len(fig.axes) == 4)


if __name__ == '__main__':
    unittest.main()
