# Follows the tests in
#   https://github.com/antononcube/R-packages/tree/master/SparseMatrixRecommender

import unittest

import pandas.core.frame
from SparseMatrixRecommender.SparseMatrixRecommender import *
from SparseMatrixRecommender.DataLoaders import *


def is_smr_dict(arg):
    return isinstance(arg, dict) and \
           all([x in {'matrices', 'tagTypeWeights', 'data', 'value'} for x in list(arg.keys())])


class SMRRepresentation(unittest.TestCase):
    dfTitanic = load_titanic_data_frame()
    smrTitanic = (SparseMatrixRecommender()
                  .create_from_wide_form(data=dfTitanic,
                                         columns=None,
                                         item_column_name="id",
                                         add_tag_types_to_column_names=False,
                                         tag_value_separator=":")
                  .apply_term_weight_functions(global_weight_func="None",
                                               local_weight_func="None",
                                               normalizer_func="None"))

    def test_remove_tag_types_1(self):
        # Verify we get a recommender object with the simplest signature.

        smr2 = self.smrTitanic.remove_tag_types(tag_types="passengerAge")

        tagTypes = list(self.smrTitanic.take_matrices().keys())

        # Verify we got recommender and expected SSparseMatrix object
        self.assertTrue(isinstance(smr2, SparseMatrixRecommender))
        self.assertTrue(isinstance(smr2.take_M(), SSparseMatrix))

        tagTypes2 = list(smr2.take_matrices().keys())
        self.assertTrue(len(tagTypes2) == len(tagTypes) - 1)
        self.assertTrue(len(set.difference(set(tagTypes), set(tagTypes2))), 1)
        self.assertTrue(list(set.difference(set(tagTypes), set(tagTypes2)))[0], "passengerAge")

    def test_remove_tag_types_2(self):
        # Verify we get a recommender object with the simplest signature.

        smr2 = self.smrTitanic.remove_tag_types(tag_types=["passengerAge", "passengerSex"])

        tagTypes = list(self.smrTitanic.take_matrices().keys())

        # Verify we got recommender and expected SSparseMatrix object
        self.assertTrue(isinstance(smr2, SparseMatrixRecommender))
        self.assertTrue(isinstance(smr2.take_M(), SSparseMatrix))

        tagTypes2 = list(smr2.take_matrices().keys())
        self.assertTrue(len(tagTypes2) == len(tagTypes) - 2)
        self.assertTrue(len(set.difference(set(tagTypes), set(tagTypes2))) == 2)
        self.assertTrue(len(set.difference(set(tagTypes), set(tagTypes2), set(["passengerAge", "passengerSex"]))) == 0)


if __name__ == '__main__':
    unittest.main()
