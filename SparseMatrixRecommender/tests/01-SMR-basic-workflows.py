# Follows the tests in
#   https://github.com/antononcube/R-packages/tree/master/SparseMatrixRecommender

import unittest

import pandas.core.frame
from SparseMatrixRecommender.DataLoaders import *
from SparseMatrixRecommender.SparseMatrixRecommender import *


def is_scored_tags_dict(obj):
    return isinstance(obj, dict) and \
           all([isinstance(x, str) for x in obj.keys()]) and \
           all([isinstance(x, int) or isinstance(x, float) for x in obj.values()])


class SMRRecommendations(unittest.TestCase):
    dfMushroom = load_mushroom_data_frame()
    smr = (SparseMatrixRecommender()
           .create_from_wide_form(data=dfMushroom,
                                  columns=None,
                                  item_column_name="id",
                                  add_tag_types_to_column_names=True,
                                  tag_value_separator=":")
           .apply_term_weight_functions(global_weight_func="IDF",
                                        local_weight_func="None",
                                        normalizer_func="Cosine"))

    def test_expected_SMR_object(self):
        self.assertTrue(isinstance(self.smr, SparseMatrixRecommender)) and \
        self.assertTrue(isinstance(self.smr.take_M(), SSparseMatrix)) and \
        self.assertTrue(self.smr.take_M().nrow() > 8000) and \
        self.assertTrue(self.smr.take_M().ncol() > 110)

    def test_expected_profile_object_1(self):
        prof = self.smr.profile(history=["id.1", "id.14", "id.33"]).take_value()
        self.assertTrue(is_scored_tags_dict(prof))

    def test_expected_profile_object_2(self):
        prof = self.smr.profile(history={"id.1": 1, "id.14": 2, "id.33": 1}).take_value()
        self.assertTrue(is_scored_tags_dict(prof))

    def test_recommend_by_history_object_1(self):
        recs = self.smr.recommend(history=["id.1", "id.14", "id.33"]).take_value()
        self.assertTrue(is_scored_tags_dict(recs))

    def test_recommend_by_history_object_3(self):
        recs = (self.smr
                .recommend(history={"id.1": 1, "id.14": 2, "id.33": 1}, nrecs=12)
                .join_across(data=self.dfMushroom, on=None)
                .take_value())
        self.assertTrue(isinstance(recs, pandas.core.frame.DataFrame))

    def test_recommend_by_profile_object_1(self):
        recs = (self.smr
                .recommend_by_profile(profile=["cap-Shape:convex", "edibility:poisonous"])
                .take_value())
        self.assertTrue(is_scored_tags_dict(recs))

    def test_recommend_by_profile_object_2(self):
        recs = (self.smr
                .recommend_by_profile(profile={"cap-Shape:convex": 1.2, "edibility:poisonous": 1.4}, nrecs=12)
                .join_across(data=self.dfMushroom, on=None)
                .take_value())
        self.assertTrue(isinstance(recs, pandas.core.frame.DataFrame))


if __name__ == '__main__':
    unittest.main()
