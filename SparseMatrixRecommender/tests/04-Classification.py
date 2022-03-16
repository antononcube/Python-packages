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
                                  numerical_columns_as_categorical=True,
                                  tag_value_separator=":")
           .apply_term_weight_functions(global_weight_func="IDF",
                                        local_weight_func="None",
                                        normalizer_func="Cosine"))

    def test_classification_1(self):
        # Verify Titanic classification result using 50 n_top_nearest_neighbors
        profile1 = ["male", "3rd"]

        res1 = (self.smr
                .classify_by_profile(tag_type="passengerSurvival",
                                     profile=profile1,
                                     n_top_nearest_neighbors=50,
                                     normalize=False)
                .take_value())

        self.assertTrue(res1 == {"died": 38., "survived": 12})

    def test_classification_2(self):
        # Verify Titanic classification result using 120 n_top_nearest_neighbors
        profile2 = ["female", "1st"]

        res2 = (self.smr
                .classify_by_profile(tag_type="passengerSurvival",
                                     profile=profile2,
                                     n_top_nearest_neighbors=120,
                                     normalize=False)
                .take_value())

        self.assertTrue(res2 == {"survived": 115, "died": 5})

    def test_classification_3(self):
        # Verify Titanic classification with unknown tags
        profile2 = ["female", "1st", "BlahBlah"]

        res2 = (self.smr
                .classify_by_profile(tag_type="passengerSurvival",
                                     profile=profile2,
                                     n_top_nearest_neighbors=120,
                                     normalize=False,
                                     ignore_unknown=True)
                .take_value())

        self.assertTrue(res2 == {"survived": 115, "died": 5})


if __name__ == '__main__':
    unittest.main()
