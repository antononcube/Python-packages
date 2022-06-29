import unittest
from ROCFunctions import roc_functions


class PropsRetrieval(unittest.TestCase):

    def test_properties(self):
        self.assertTrue(isinstance(roc_functions('properties'), list))

    def test_functions_1(self):
        self.assertTrue(isinstance(roc_functions('functions'), list))

    def test_functions_2(self):
        self.assertTrue(callable(roc_functions('functions')[0]))

    def test_function_names(self):
        self.assertTrue(isinstance(roc_functions('FunctionNames'), list))

    def test_no_args(self):
        self.assertEqual(roc_functions(), roc_functions('Functions'))


if __name__ == '__main__':
    unittest.main()
