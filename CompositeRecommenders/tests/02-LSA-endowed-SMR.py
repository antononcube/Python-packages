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
    smrObj = (SparseMatrixRecommender()
              .create_from_wide_form(data=dfTitanic,
                                     columns=None,
                                     item_column_name="id",
                                     add_tag_types_to_column_names=True,
                                     tag_value_separator=":")
              .apply_term_weight_functions(global_weight_func="IDF",
                                           local_weight_func="None",
                                           normalizer_func="Cosine"))

    lsaObj = SMR_to_LSA(smr=smrObj, number_of_topics=3)

    smatWords = lsaObj.take_doc_term_mat().copy()
    smatWords = smatWords.set_column_names(["Word:" + c for c in smatWords.column_names()], )

    smatTopics = lsaObj.take_W().copy()
    smatTopics = smatTopics.set_column_names(["Topic:" + c for c in smatTopics.column_names()])

    smrObj = smrObj.annex_sub_matrices(mats={"Word": smatWords, "Topic": smatTopics})
    smrObj = smrObj.apply_term_weight_functions("None", "None", "Cosine")
    smrEndowed = LSAEndowedSMR(smrObj, lsaObj)

    def test_recommend_by_profile_and_text_1(self):
        recs1 = (self.smrEndowed
                 .recommend_by_profile_and_text([],
                                                "male 3rd survived",
                                                ignore_unknown=True,
                                                nrecs=10)
                 .take_value())
        self.assertTrue(isinstance(recs1, dict))
        self.assertTrue(len(recs1) == 10)


if __name__ == '__main__':
    unittest.main()
