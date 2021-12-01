# Follows the tests in
#   https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m

import unittest

from RandomDataGenerators.RandomFunctions import *


def _is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def _is_str_keys_dict(obj):
    return isinstance(obj, dict) and all([isinstance(k, str) for (k, v) in obj.items()])


def _is_func_list(obj):
    return isinstance(obj, list) and \
           all([isinstance(x, type(random_word, numpy.random.poisson)) for x in obj])


def _is_func_dict(obj):
    return isinstance(obj, dict) and \
           _is_str_list(list(obj.keys())) and \
           all([isinstance(x, type(random_word)) or
                isinstance(x, type(numpy.random.poisson)) for x in list(obj.values())])


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

    def test_random_word_3(self):
        res = random_word(size=12, kind="common")
        self.assertTrue(_is_str_list(res))

    def test_random_word_4(self):
        res = random_word(size=12, kind="Known")
        self.assertTrue(_is_str_list(res))

    def test_random_pet_name_1(self):
        res = random_pet_name()
        self.assertTrue(isinstance(res, str))

    def test_random_pet_name_2(self):
        res = random_pet_name(size=12)
        self.assertTrue(_is_str_list(res))

    def test_random_pet_name_3(self):
        res = random_pet_name(size=12, species="dog")
        self.assertTrue(_is_str_list(res))

    def test_random_pet_name_4(self):
        res = random_pet_name(size=12, species="Cat")
        self.assertTrue(_is_str_list(res))

    def test_random_pretentious_job_title_1(self):
        res = random_pretentious_job_title()
        self.assertTrue(isinstance(res, str))

    def test_random_pretentious_job_title_2(self):
        res = random_pretentious_job_title(size=12)
        self.assertTrue(_is_str_list(res))

    def test_random_pretentious_job_title_3(self):
        res = random_pretentious_job_title(size=12, number_of_words=2)
        self.assertTrue(_is_str_list(res))

    def test_random_pretentious_job_title_4(self):
        res = random_pretentious_job_title(size=12, language="Bulgarian")
        self.assertTrue(_is_str_list(res))

    def test_random_pretentious_job_title_5(self):
        res = random_pretentious_job_title(size=12, language=None)
        self.assertTrue(_is_str_list(res))

    def test_random_pretentious_job_title_6(self):

        with self.assertWarnsRegex(UserWarning,
                                   r"The argument 'language' is expected to be one of.*"):
            res = random_pretentious_job_title(size=12, language="Any")

        self.assertTrue(_is_str_list(res))


if __name__ == '__main__':
    unittest.main()
