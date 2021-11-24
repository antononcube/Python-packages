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
    dfData = load_titanic_data_frame()
    smr = (SparseMatrixRecommender()
           .create_from_wide_form(data=dfData,
                                  columns=None,
                                  item_column_name="id",
                                  add_tag_types_to_column_names=False,
                                  tag_value_separator=":")
           .apply_term_weight_functions(global_weight_func="IDF",
                                        local_weight_func="None",
                                        normalizer_func="Cosine"))

    def test_to_dict_1(self):
        # Verify to_dict() produces a dictionary representing SparseMatrixRecommender object
        self.assertTrue(is_smr_dict(self.smr.to_dict()))

    def test_to_dict_2(self):
        # Verify same recommendations the original and re-created recommenders

        # SMR dict
        smr_dict = self.smr.to_dict()

        # New SMR object
        smrNew = SparseMatrixRecommender().from_dict(smr_dict)

        # Profile
        prof = {"male": 1.2, "1st": 0.5, "died": 0.4}

        # Recommendations
        recs1 = self.smr.recommend_by_profile(profile=prof, nrecs=12).take_value()
        recs2 = smrNew.recommend_by_profile(profile=prof, nrecs=12).take_value()

        # Verify is a dictionary representing SSparseMatrix object
        self.assertTrue(recs1 == recs2)


if __name__ == '__main__':
    unittest.main()
