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
    # Titanic data and recommender
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

    # Mint data
    dfMint = load_mint_bubbles_transactions_data_frame()

    # Make the first recommender
    dfMintPart1 = dfMint[200:dfMint.shape[0]][["id", "Date", "Description", "Amount"]]
    smrObj1 = SparseMatrixRecommender().create_from_wide_form(data=dfMintPart1, item_column_name="id")

    # Make the second recommender
    dfMintPart2 = dfMint[0:300][["id", "Transaction.Type", "Category", "Account.Name"]]
    smrObj2 = SparseMatrixRecommender().create_from_wide_form(data=dfMintPart2, item_column_name="id")

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

    def test_outer_join_1(self):
        # Outer join of the recommenders
        smrObj3 = self.smrObj1.join(self.smrObj2, join_type="outer")

        # Expected recommender object
        self.assertTrue(isinstance(smrObj3.take_matrices(), dict))
        self.assertTrue(len(smrObj3.take_matrices()) == 6)

        # The sub-matrix names are the same dfMint column names except the ID column
        self.assertTrue(len(set.difference(set(smrObj3.take_matrices().keys()), set(self.dfMint.keys()))) == 0)
        self.assertTrue(len(set.difference(set(self.dfMint.keys()), set(smrObj3.take_matrices().keys()))) == 1)

        # The rows names are the same as the IDs in the ID column of dfMint
        self.assertTrue(smrObj3.take_M().rows_count() == self.dfMint.shape[0])
        self.assertTrue(
            len(set.difference(set(smrObj3.take_M().row_names()),
                               set(self.dfMint["id"].to_dict().values()))) == 0)
        self.assertTrue(len(set.difference(set(self.dfMint["id"].to_dict().values()),
                            set(smrObj3.take_M().row_names()))) == 0)

    def test_inner_join_1(self):
        # Inner join of the recommenders
        smrObj4 = self.smrObj1.join(self.smrObj2, join_type="inner")

        # Expected recommender object
        self.assertTrue(isinstance(smrObj4.take_matrices(), dict))
        self.assertTrue(len(smrObj4.take_matrices()) == 6)

        # The sub-matrix names are the same dfMint column names except the ID column
        self.assertTrue(len(set.difference(set(smrObj4.take_matrices().keys()),
                                           set(self.dfMint.keys()))) == 0)
        self.assertTrue(len(set.difference(set(self.dfMint.keys()),
                                           set(smrObj4.take_matrices().keys()))) == 1)

        # The rows names are the same as the IDs in the ID column of
        # the intersection of dfMintPart1[["id"]] and dfMintPart2[["id"]]
        commonIDs = set.intersection(set(self.dfMintPart1["id"].to_dict().values()),
                                     set(self.dfMintPart2["id"].to_dict().values()))
        self.assertTrue(smrObj4.take_M().rows_count() == len(commonIDs))
        self.assertTrue(len(set.difference(set(smrObj4.take_M().row_names()),
                                           commonIDs)) == 0)
        self.assertTrue(len(set.difference(commonIDs,
                                           set(smrObj4.take_M().row_names()))) == 0)

    def test_left_join_1(self):
        # Left join of the recommenders
        smrObj4 = self.smrObj1.join(self.smrObj2, join_type="left")

        # Expected recommender object
        self.assertTrue(isinstance(smrObj4.take_matrices(), dict))
        self.assertTrue(len(smrObj4.take_matrices()) == 6)

        # The sub-matrix names are the same dfMint column names except the ID column
        self.assertTrue(len(set.difference(set(smrObj4.take_matrices().keys()),
                                           set(self.dfMint.keys()))) == 0)
        self.assertTrue(len(set.difference(set(self.dfMint.keys()),
                                           set(smrObj4.take_matrices().keys()))) == 1)

        # The rows names are the same as the IDs in the ID column of dfMintPart1[["id"]]
        commonIDs = set(self.dfMintPart1["id"].to_dict().values())
        self.assertTrue(smrObj4.take_M().rows_count() == len(commonIDs))
        self.assertTrue(len(set.difference(set(smrObj4.take_M().row_names()),
                                           commonIDs)) == 0)
        self.assertTrue(len(set.difference(commonIDs,
                                           set(smrObj4.take_M().row_names()))) == 0)


if __name__ == '__main__':
    unittest.main()
