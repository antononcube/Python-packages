import unittest

from JavaScriptD3.Random import *


class RandomCalls(unittest.TestCase):

    def test_1(self):
        res = js_d3_random_mandala()
        self.assertTrue(isinstance(res, str))

    def test_2(self):
        res = js_d3_random_mandala(count=6,
                                   radius=1,
                                   rotational_symmetry_order=12,
                                   symmetric_seed=True,
                                   number_of_seed_elements=6,
                                   fill="Salmon",
                                   fmt="html")
        self.assertTrue(isinstance(res, str))


if __name__ == '__main__':
    unittest.main()
