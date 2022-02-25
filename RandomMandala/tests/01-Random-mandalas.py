# Follows the tests in
#   https://resources.wolframcloud.com/FunctionRepository/resources/RandomMandala/

import unittest

from RandomMandala.RandomFunctions import random_mandala
from RandomMandala.RandomMandala import figure_to_image
import matplotlib
from matplotlib import figure
from PIL import Image, ImageOps
import random


def _is_num_list(obj):
    return isinstance(obj, list) and all([isinstance(x, int) or isinstance(x, float) for x in obj])


def _is_figure(obj):
    return isinstance(obj, matplotlib.figure.Figure)


def _is_figure_list(obj):
    return isinstance(obj, list) and all([_is_figure(x) for x in obj])


class RandomMandalas(unittest.TestCase):

    def test_random_mandala_1(self):
        res = random_mandala()
        self.assertTrue(_is_figure(res))

    def test_random_mandala_2(self):
        res = random_mandala(n_rows=None, n_columns=3)
        self.assertTrue(_is_figure(res))

    def test_random_mandala_3(self):
        res = random_mandala(n_rows=3, n_columns=None)
        self.assertTrue(_is_figure(res))

    def test_random_mandala_4(self):
        res = random_mandala(radius=3, connecting_function="fill", face_color=["blue", "red"])
        self.assertTrue(_is_figure(res) and len(res.axes) == 1)

    def test_random_mandala_5(self):
        res = random_mandala(radius=3, connecting_function="line", edge_color=["blue", "red"])
        self.assertTrue(_is_figure(res) and len(res.axes) == 1)

    def test_random_mandala_6(self):
        res = random_mandala(n_rows=3, n_columns=3, figsize=(12, 12), dpi=120)
        self.assertTrue(_is_figure(res))

    def test_random_multi_mandala_1(self):
        res = random_mandala(radius=[3, 2])
        self.assertTrue(_is_figure(res))

    def test_random_multi_mandala_2(self):
        res = random_mandala(radius=[3, 2, 1])
        self.assertTrue(_is_figure(res))

    def test_random_multi_mandala_3(self):
        res = random_mandala(radius=[3, 2, 1], connecting_function="fill", face_color=["blue", "red"])
        self.assertTrue(_is_figure(res) and len(res.axes) == 1)

    def test_random_multi_mandala_4(self):
        res = random_mandala(radius=[3, 2, 1], connecting_function="line", face_color=["blue", "red"])
        self.assertTrue(_is_figure(res) and len(res.axes) == 1)

    def test_random_multi_mandala_5(self):
        res = random_mandala(radius=[3, 2, 1], connecting_function="line", face_color=["blue", "red"], alpha=1)
        self.assertTrue(_is_figure(res) and len(res.axes) == 1)

    def test_random_multi_mandala_6(self):
        res = random_mandala(radius=[3, 2, 1], connecting_function="line", color_mapper=matplotlib.cm.rainbow, alpha=0.5)
        self.assertTrue(_is_figure(res) and len(res.axes) == 1)

    def test_random_mandalas_collection_1(self):
        fig = matplotlib.pyplot.figure(figsize=(6, 6), dpi=120)

        k = 1
        for rso in [2, 3, 4, 6]:
            random.seed(122)
            fig = random_mandala(connecting_function="fill",
                                 rotational_symmetry_order=rso,
                                 figure=fig,
                                 location=(1, 4, k))
            ax = fig.axes[-1]
            ax.set_title("order:" + str(rso))
            k = k + 1

        self.assertTrue(_is_figure(fig) and len(fig.axes) == 4)

    def test_random_mandalas_collection_2(self):
        fig = matplotlib.pyplot.figure(figsize=(6, 6), dpi=120)

        k = 1
        for cf in ['fill', 'line', 'bezier', 'bezier_fill', 'random', None]:
            random.seed(122)
            fig = random_mandala(connecting_function=cf,
                                 figure=fig,
                                 location=(1, 6, k))
            ax = fig.axes[-1]
            ax.set_title("connecting with:" + str(cf))
            k = k + 1

        self.assertTrue(_is_figure(fig) and len(fig.axes) == 6)


if __name__ == '__main__':
    unittest.main()
