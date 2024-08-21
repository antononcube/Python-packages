import numpy as np
import unittest
from OutlierIdentifiers import *

class TestOutlierIdentifiers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        np.random.seed(2342)
        rand_data = np.random.uniform(-10, 100, 200)
        rand_data2 = np.random.uniform(140, 160, 19)
        rand_data3 = np.random.uniform(-50, -30, 12)
        cls.rand_data = np.random.permutation(np.concatenate((rand_data, rand_data2, rand_data3)))

    def test_outlier_identifier_equivalences(self):
        rand_data = self.rand_data

        self.assertTrue(np.array_equal(
            outlier_identifier(data=rand_data, identifier=splus_quartile_identifier_parameters, value=True),
            outlier_identifier(data=rand_data, lower_and_upper_thresholds=splus_quartile_identifier_parameters(rand_data), value=True)
        ))

        self.assertTrue(np.array_equal(
            outlier_identifier(data=rand_data, identifier=hampel_identifier_parameters, value=True),
            outlier_identifier(data=rand_data, identifier=None, lower_and_upper_thresholds=hampel_identifier_parameters(rand_data), value=True)
        ))

        self.assertTrue(np.array_equal(
            outlier_identifier(data=rand_data, identifier=splus_quartile_identifier_parameters, value=False),
            outlier_identifier(data=rand_data, lower_and_upper_thresholds=splus_quartile_identifier_parameters(rand_data), value=False)
        ))

        self.assertTrue(np.array_equal(
            outlier_identifier(data=rand_data, identifier=hampel_identifier_parameters, value=False),
            outlier_identifier(data=rand_data, identifier=None, lower_and_upper_thresholds=hampel_identifier_parameters(rand_data), value=False)
        ))

    def test_top_outlier_identifier_equivalences(self):
        rand_data = self.rand_data

        self.assertTrue(np.array_equal(
            top_outlier_identifier(data=rand_data, identifier=quartile_identifier_parameters, value=True),
            top_outlier_identifier(data=rand_data, lower_and_upper_thresholds=quartile_identifier_parameters(rand_data), value=True)
        ))

        self.assertTrue(np.array_equal(
            top_outlier_identifier(data=rand_data, identifier=hampel_identifier_parameters, value=True),
            top_outlier_identifier(data=rand_data, identifier=None, lower_and_upper_thresholds=hampel_identifier_parameters(rand_data), value=True)
        ))

        self.assertTrue(np.array_equal(
            top_outlier_identifier(data=rand_data, identifier=quartile_identifier_parameters, value=False),
            top_outlier_identifier(data=rand_data, lower_and_upper_thresholds=quartile_identifier_parameters(rand_data), value=False)
        ))

        self.assertTrue(np.array_equal(
            top_outlier_identifier(data=rand_data, identifier=hampel_identifier_parameters, value=False),
            top_outlier_identifier(data=rand_data, identifier=None, lower_and_upper_thresholds=hampel_identifier_parameters(rand_data), value=False)
        ))

        self.assertTrue(np.array_equal(
            top_outlier_identifier(data=rand_data, identifier=hampel_identifier_parameters, value=False),
            outlier_identifier(data=rand_data, identifier=lambda x: top_outliers_only_thresholds(hampel_identifier_parameters(x)), value=False)
        ))

    def test_bottom_outlier_identifier_equivalences(self):
        rand_data = self.rand_data

        self.assertTrue(np.array_equal(
            bottom_outlier_identifier(data=rand_data, identifier=quartile_identifier_parameters, value=True),
            bottom_outlier_identifier(data=rand_data, lower_and_upper_thresholds=quartile_identifier_parameters(rand_data), value=True)
        ))

        self.assertTrue(np.array_equal(
            bottom_outlier_identifier(data=rand_data, identifier=hampel_identifier_parameters, value=True),
            bottom_outlier_identifier(data=rand_data, identifier=None, lower_and_upper_thresholds=hampel_identifier_parameters(rand_data), value=True)
        ))

        self.assertTrue(np.array_equal(
            bottom_outlier_identifier(data=rand_data, identifier=quartile_identifier_parameters, value=False),
            bottom_outlier_identifier(data=rand_data, lower_and_upper_thresholds=quartile_identifier_parameters(rand_data), value=False)
        ))

        self.assertTrue(np.array_equal(
            bottom_outlier_identifier(data=rand_data, identifier=hampel_identifier_parameters, value=False),
            bottom_outlier_identifier(data=rand_data, identifier=None, lower_and_upper_thresholds=hampel_identifier_parameters(rand_data), value=False)
        ))

        self.assertTrue(np.array_equal(
            bottom_outlier_identifier(data=rand_data, identifier=hampel_identifier_parameters, value=False),
            outlier_identifier(data=rand_data, identifier=lambda x: bottom_outliers_only_thresholds(hampel_identifier_parameters(x)), value=False)
        ))

    def test_outlier_position_equivalences(self):
        rand_data = self.rand_data

        self.assertTrue(np.array_equal(
            outlier_position(data=rand_data, identifier=quartile_identifier_parameters),
            outlier_position(data=rand_data, lower_and_upper_thresholds=quartile_identifier_parameters(rand_data))
        ))

        self.assertTrue(np.array_equal(
            outlier_position(data=rand_data, identifier=hampel_identifier_parameters),
            outlier_position(data=rand_data, identifier=None, lower_and_upper_thresholds=hampel_identifier_parameters(rand_data))
        ))

    def test_top_outlier_position_equivalences(self):
        rand_data = self.rand_data

        self.assertTrue(np.array_equal(
            top_outlier_position(data=rand_data, identifier=quartile_identifier_parameters),
            top_outlier_position(data=rand_data, lower_and_upper_thresholds=quartile_identifier_parameters(rand_data))
        ))

        self.assertTrue(np.array_equal(
            top_outlier_position(data=rand_data, identifier=hampel_identifier_parameters),
            top_outlier_position(data=rand_data, identifier=None, lower_and_upper_thresholds=hampel_identifier_parameters(rand_data))
        ))

    def test_bottom_outlier_position_equivalences(self):
        rand_data = self.rand_data

        self.assertTrue(np.array_equal(
            bottom_outlier_position(data=rand_data, identifier=quartile_identifier_parameters),
            bottom_outlier_position(data=rand_data, lower_and_upper_thresholds=quartile_identifier_parameters(rand_data))
        ))

        self.assertTrue(np.array_equal(
            bottom_outlier_position(data=rand_data, identifier=hampel_identifier_parameters),
            bottom_outlier_position(data=rand_data, identifier=None, lower_and_upper_thresholds=hampel_identifier_parameters(rand_data))
        ))

if __name__ == '__main__':
    unittest.main()
