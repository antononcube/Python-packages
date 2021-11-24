# Follows the tests in
#   https://github.com/antononcube/R-packages/tree/master/SparseMatrixRecommender

import unittest

import pandas.core.frame
from SparseMatrixRecommender.SparseMatrixRecommender import *
from SparseMatrixRecommender.DataLoaders import *


def is_smr_dict(arg):
    return isinstance(arg, dict) and \
           all([x in {'matrices', 'tagTypeWeights', 'data', 'value'} for x in list(arg.keys())])


class SMRCreation(unittest.TestCase):
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

    def test_from_init_1(self):
        # Verify smr is "filled-in" using __init__ with a dictionary of matrices.

        smrObjNew = SparseMatrixRecommender(self.smr.take_matrices())
        self.assertTrue(is_smat_dict(smrObjNew.take_matrices()))
        self.assertTrue(smrObjNew.take_M().eq(self.smr.take_M()))


if __name__ == '__main__':
    unittest.main()
