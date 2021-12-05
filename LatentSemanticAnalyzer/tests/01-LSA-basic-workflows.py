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

    # "Standard" LSA object creation
    lsaObj = (LatentSemanticAnalyzer()
              .make_document_term_matrix(docs=docs,
                                         stop_words=True,
                                         stemming_rules=True,
                                         min_length=3)
              .apply_term_weight_functions(global_weight_func="IDF",
                                           local_weight_func="None",
                                           normalizer_func="Cosine"))

    queries = ["Notebook of differential equations solutions.",
               "Neural networking training process",
               "Anomaly finding in time series"]

    def test_expected_LSA_object(self):
        self.assertTrue(isinstance(self.lsaObj, LatentSemanticAnalyzer))
        self.assertTrue(isinstance(self.lsaObj.take_doc_term_mat(), SSparseMatrix))
        self.assertTrue(isinstance(self.lsaObj.take_weighted_doc_term_mat(), SSparseMatrix))
        self.assertTrue(self.lsaObj.take_doc_term_mat().nrow() > 570)
        self.assertTrue(self.lsaObj.take_doc_term_mat().ncol() > 2000)

    def test_extract_topics_1(self):
        self.lsaObj = self.lsaObj.extract_topics(number_of_topics=20, method="SVD", max_steps=40)

        self.assertTrue(is_s_sparse_matrix(self.lsaObj.take_W()) and is_s_sparse_matrix(self.lsaObj.take_H()))

    def test_extract_topics_2(self):
        self.lsaObj = self.lsaObj.extract_topics(number_of_topics=20, method="NNMF", max_steps=5)

        self.assertTrue(is_s_sparse_matrix(self.lsaObj.take_W()) and is_s_sparse_matrix(self.lsaObj.take_H()))

    def test_stat_thesaurus_1(self):
        # Stemmer object (to preprocess words in the pipeline below)
        stemmerObj = snowballstemmer.stemmer("english")

        # Words to show statistical thesaurus entries for
        words = ["notebook", "computational", "function", "neural", "talk", "programming"]

        # Get stat thesaurus
        res = (self.lsaObj
               .get_statistical_thesaurus(terms=stemmerObj.stemWords(words),
                                          wide_form=True,
                                          number_of_nearest_neighbors=12,
                                          method="cosine",
                                          echo=False,
                                          echo_function=None)
               .take_value())

        self.assertTrue(isinstance(res, pandas.core.frame.DataFrame) and res.shape[0] == len(words))

    def test_represent_by_terms_1(self):
        res = (self.lsaObj
               .represent_by_terms(query=self.queries, apply_lsi_functions=True)
               .take_value())

        self.assertTrue(is_s_sparse_matrix(res)) and res.rows_count() == len(self.queries)

    def test_represent_by_topics_1(self):
        res = (self.lsaObj
               .represent_by_topics(query=self.queries,
                                    apply_lsi_functions=True,
                                    method="recommendation")
               .take_value())

        self.assertTrue(is_s_sparse_matrix(res)) and res.rows_count() == len(self.queries)


if __name__ == '__main__':
    unittest.main()
