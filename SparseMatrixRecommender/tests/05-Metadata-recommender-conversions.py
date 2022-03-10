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

    def test_to_metadata_smr_1(self):
        # Verify we get a recommender object with the simplest signature.

        smrAge = self.smrTitanic.to_metadata_recommender(tag_type_to="passengerAge")

        # Verify we got recommender and expected SSparseMatrix object
        self.assertTrue(isinstance(smrAge, SparseMatrixRecommender))
        self.assertTrue(isinstance(smrAge.take_M(), SSparseMatrix))

    def test_to_metadata_smr_2(self):
        # Verify we get a recommender object with a more extensive signature.

        smrAge = (self
                  .smrTitanic
                  .to_metadata_recommender(tag_type_to="passengerAge",
                                           tag_types=["passengerSex", "passengerClass", "passengerSurvival"]))

        # Verify we got recommender and expected SSparseMatrix object
        self.assertTrue(isinstance(smrAge, SparseMatrixRecommender))
        self.assertTrue(isinstance(smrAge.take_M(), SSparseMatrix))

    def test_to_metadata_smr_3(self):
        # Verify we get the same recommenders with the simplest signature and the extended signature.

        smrAge1 = (self.smrTitanic
                   .to_metadata_recommender(tag_type_to="passengerAge", tag_types=None))

        smrAge2 = (self.smrTitanic
                   .to_metadata_recommender(tag_type_to="passengerAge",
                                            tag_types=["passengerSex", "passengerClass", "passengerSurvival"]))

        # Verify we got the same recommender SSparseMatrix object
        self.assertTrue(smrAge1.take_M().eq(smrAge2.take_M()))

    def test_to_metadata_smr_4(self):
        # Verify same recommendations the original and re-created recommenders

        smrAge = self.smrTitanic.to_metadata_recommender(tag_type_to="passengerAge", tag_types=["passengerSex"])

        smat1 = cross_tabulate(self.dfTitanic, "passengerAge", "passengerSex")

        # Verify we got recommender and expected SSparseMatrix object
        self.assertTrue(isinstance(smrAge, SparseMatrixRecommender))
        self.assertTrue(isinstance(smrAge.take_M(), SSparseMatrix))

        # Verify we got same matrices
        smrAge.take_M().eq(smat1)

    def test_to_metadata_smr_5(self):
        # Verify same recommendations the original and re-created recommenders

        smrAge = self.smrTitanic.to_metadata_recommender(tag_type_to="passengerAge", tag_types=["passengerSex"])

        smat1 = cross_tabulate(self.dfTitanic, "passengerAge", "passengerSex")

        # Verify we got recommender and expected SSparseMatrix object
        self.assertTrue(isinstance(smrAge, SparseMatrixRecommender))
        self.assertTrue(isinstance(smrAge.take_M(), SSparseMatrix))

        # Verify we got same matrices
        smrAge.take_M().eq(smat1)


if __name__ == '__main__':
    unittest.main()
