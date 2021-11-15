# Follows the tests in
#   https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m

import unittest

import pandas.core.frame
from RandomDataFrameGenerator.RandomFunctions import *
from RandomDataFrameGenerator.RandomDataFrameGenerator import *


def _is_num_list(obj):
    return isinstance(obj, list) and all([isinstance(x, int) or isinstance(x, float) for x in obj])


def _is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def _is_str_keys_dict(obj):
    return isinstance(obj, dict) and all([isinstance(k, str) for (k, v) in obj.items()])


def _is_func_list(obj):
    return isinstance(obj, list) and \
           all([isinstance(x, type(random_word)) or isinstance(x, type(numpy.random.poisson)) for x in obj])


def _is_func_dict(obj):
    return isinstance(obj, dict) and \
           _is_str_list(list(obj.keys())) and \
           all([isinstance(x, type(random_word)) or isinstance(x, type(numpy.random.poisson)) for x in
                list(obj.values())])


class BasicFunctionalities(unittest.TestCase):

    def test_random_data_frame_1(self):
        res = random_data_frame()
        self.assertTrue(isinstance(res, pandas.core.frame.DataFrame))

    def test_random_data_frame_2(self):
        res = random_data_frame(12)
        self.assertTrue(isinstance(res, pandas.core.frame.DataFrame) and res.shape[0] == 12)

    def test_random_data_frame_3(self):
        res = random_data_frame(None, 12)
        self.assertTrue(isinstance(res, pandas.core.frame.DataFrame) and res.shape[1] == 12)

    def test_random_data_frame_4(self):
        res = random_data_frame(12, 5)
        self.assertTrue(isinstance(res, pandas.core.frame.DataFrame) and res.shape == (12, 5))

    def test_random_data_frame_5(self):
        res = random_data_frame(12, ['a', 'b', 'c'])
        self.assertTrue(isinstance(res, pandas.core.frame.DataFrame) and res.shape == (12, 3))

    def test_random_data_frame_6(self):
        res = random_data_frame(12, None, column_names_generator=random_word)
        self.assertTrue(isinstance(res, pandas.core.frame.DataFrame) and _is_str_list(list(res.columns)))

    def test_random_data_frame_7(self):
        res = random_data_frame(12, None, column_names_generator=random_string, row_names=True)
        self.assertTrue(
            isinstance(res, pandas.core.frame.DataFrame) and _is_str_list(list(res.columns)) \
            and _is_str_list(list(res.index)))

    def test_random_data_frame_8(self):
        gspec = {"kotka": lambda size: numpy.random.normal(loc=100, scale=10, size=size),
                 "krem": numpy.random.poisson,
                 'sasa': random_string,
                 'word': random_word,
                 'mark': random_pet_name}

        res = random_data_frame(12, list(gspec.keys()), generators=gspec)
        self.assertTrue(
            isinstance(res, pandas.core.frame.DataFrame)
            and _is_num_list(list(res.kotka))
            and _is_num_list(list(res.krem))
            and _is_str_list(list(res.sasa)))


if __name__ == '__main__':
    unittest.main()
