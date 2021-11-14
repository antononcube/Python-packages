# Follows the tests in
#   https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m

import unittest

from RandomDataFrameGenerator.RandomFunctions import *


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

    def test_random_string_1(self):
        res = random_string()
        self.assertTrue(isinstance(res, str))

    def test_random_string_2(self):
        res = random_string(12)
        self.assertTrue(_is_str_list(res))

    def test_random_string_3(self):
        res = random_string(size=12)
        self.assertTrue(_is_str_list(res))

    def test_random_word_1(self):
        res = random_word()
        self.assertTrue(isinstance(res, str))

    def test_random_word_2(self):
        res = random_word(size=12)
        self.assertTrue(_is_str_list(res))

    def test_random_word_2(self):
        res = random_word(size=12, kind="common")
        self.assertTrue(_is_str_list(res))

    def test_random_word_3(self):
        res = random_word(size=12, kind="Known")
        self.assertTrue(_is_str_list(res))


if __name__ == '__main__':
    unittest.main()
