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

    def test_should_1(self):
        # Verify we get same IDs using pandas for should.

        obj = self.dfTitanic.copy()
        obj = obj[((obj["passengerSex"] == "male") |
                   (obj["passengerClass"] == "1st"))]

        res = (self.smrTitanic
               .retrieve_by_query_elements(should=["male", "1st"], must=[], must_not=[])
               .take_value())

        self.assertEqual(len(res), obj.shape[0])
        self.assertEqual(list(res.keys()).sort(), list(obj.id).sort())

    def test_should_2(self):
        # Verify we get same IDs using should and recommendation by profile.

        obj = self.dfTitanic.copy()
        obj = obj[((obj["passengerSex"] == "male") |
                   (obj["passengerClass"] == "1st"))]

        res = (self.smrTitanic
               .retrieve_by_query_elements(should=["male", "1st"], must=[], must_not=[])
               .take_value())

        res2 = (self.smrTitanic
                .recommend_by_profile(profile=["male", "1st"], nrecs=None)
                .take_value())

        self.assertEqual(list(res.keys()).sort(), list(res2.keys()).sort())

    def test_must_and_must_not_1(self):
        # Verify we get same IDs using pandas for must and must-not.

        obj = self.dfTitanic.copy()
        obj = obj[((obj["passengerSex"] == "male") &
                   (obj["passengerClass"] == "1st") &
                   (obj["passengerSurvival"] != "survived"))]

        res = (self.smrTitanic
               .retrieve_by_query_elements(should=[],
                                           must=["male", "1st"],
                                           must_not=["survived"])
               .take_value())

        self.assertEqual(len(res), obj.shape[0])
        self.assertEqual(list(res.keys()).sort(), list(obj.id).sort())

    def test_must_and_must_not_2(self):
        # Verify we get same IDs having non-empty should.

        res = (self.smrTitanic
               .retrieve_by_query_elements(should=[],
                                           must=["male", "1st"],
                                           must_not=["survived"])
               .take_value())

        res2 = (self.smrTitanic
                .retrieve_by_query_elements(should=["30"],
                                            must=["male", "1st"],
                                            must_not=["survived"])
                .take_value())

        self.assertEqual(len(res), len(res2))

    def test_ignore_unknown_tags_1(self):
        # Verify we get same IDs using pandas.

        res = (self.smrTitanic
               .retrieve_by_query_elements(should=[],
                                           must=["male", "1st"],
                                           must_not=["survived"])
               .take_value())

        res2 = (self.smrTitanic
                .retrieve_by_query_elements(should=["30", "age:30"],
                                            must=["male", "sex:male", "1st", "class:1st"],
                                            must_not=["survived", "survival:survived"],
                                            ignore_unknown=True)
                .take_value())

        self.assertEqual(len(res), len(res2))


if __name__ == '__main__':
    unittest.main()
