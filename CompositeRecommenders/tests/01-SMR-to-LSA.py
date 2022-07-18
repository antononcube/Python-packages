import unittest

from SparseMatrixRecommender.DataLoaders import *
from SparseMatrixRecommender.SparseMatrixRecommender import *
from CompositeRecommenders.LSAEndowedSMR import LSAEndowedSMR
from CompositeRecommenders.SMR_to_LSA import SMR_to_LSA


def is_scored_tags_dict(obj):
    return isinstance(obj, dict) and \
           all([isinstance(x, str) for x in obj.keys()]) and \
           all([isinstance(x, int) or isinstance(x, float) for x in obj.values()])


class SMRRecommendations(unittest.TestCase):
    dfTitanic = load_titanic_data_frame()
    smr = (SparseMatrixRecommender()
           .create_from_wide_form(data=dfTitanic,
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
        self.assertTrue(self.smr.take_M().nrow() > 1000) and \
        self.assertTrue(self.smr.take_M().ncol() > 11)

    def test_derive_LSA_object(self):
        lsaObj = SMR_to_LSA(smr=self.smr, number_of_topics=3)
        self.assertTrue(lsaObj.take_doc_term_mat().nrow() > 1000)
        self.assertTrue(lsaObj.take_W().nrow() > 1000)
        self.assertTrue(lsaObj.take_W().ncol() == 3)


if __name__ == '__main__':
    unittest.main()
