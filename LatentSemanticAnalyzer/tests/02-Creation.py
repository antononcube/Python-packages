# Follows the tests in
#   https://github.com/antononcube/R-packages/tree/master/LSAMon-R

import unittest

import pandas.core.frame
import snowballstemmer
from LatentSemanticAnalyzer.DataLoaders import *
from LatentSemanticAnalyzer.LatentSemanticAnalyzer import *


def is_scored_tags_dict(obj):
    return isinstance(obj, dict) and \
           all([isinstance(x, str) for x in obj.keys()]) and \
           all([isinstance(x, int) or isinstance(x, float) for x in obj.values()])


class LSAWorkflows(unittest.TestCase):
    # Resource data documents
    dfAbstracts = load_abstracts_data_frame()

    # Make a dictionary with id-document pairs
    docs = dict(zip(dfAbstracts.ID, dfAbstracts.Abstract))

    queries = ["Notebook of differential equations solutions.",
               "Neural networking training process",
               "Anomaly finding in time series"]

    def test_expected_LSA_object_1(self):
        # "Standard" LSA object creation
        lsaObj = (LatentSemanticAnalyzer()
                  .make_document_term_matrix(docs=self.docs,
                                             stop_words=True,
                                             stemming_rules=True,
                                             min_length=3)
                  .apply_term_weight_functions(global_weight_func="IDF",
                                               local_weight_func="None",
                                               normalizer_func="Cosine"))

        self.assertTrue(isinstance(lsaObj, LatentSemanticAnalyzer))
        self.assertTrue(isinstance(lsaObj.take_doc_term_mat(), SSparseMatrix))
        self.assertTrue(isinstance(lsaObj.take_weighted_doc_term_mat(), SSparseMatrix))
        self.assertTrue(lsaObj.take_doc_term_mat().nrow() > 570)
        self.assertTrue(lsaObj.take_doc_term_mat().ncol() > 2000)

    def test_expected_LSA_object_2(self):
        # "Standard" LSA object creation
        lsaObj = (LatentSemanticAnalyzer(self.docs)
                  .make_document_term_matrix(docs=None,
                                             stop_words=True,
                                             stemming_rules=True,
                                             min_length=3)
                  .apply_term_weight_functions(global_weight_func="IDF",
                                               local_weight_func="None",
                                               normalizer_func="Cosine"))

        self.assertTrue(isinstance(lsaObj, LatentSemanticAnalyzer))
        self.assertTrue(isinstance(lsaObj.take_doc_term_mat(), SSparseMatrix))
        self.assertTrue(isinstance(lsaObj.take_weighted_doc_term_mat(), SSparseMatrix))
        self.assertTrue(lsaObj.take_doc_term_mat().nrow() > 570)
        self.assertTrue(lsaObj.take_doc_term_mat().ncol() > 2000)


if __name__ == '__main__':
    unittest.main()
