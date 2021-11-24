import unittest

from LatentSemanticAnalyzer import LatentSemanticAnalyzer
from LatentSemanticAnalyzer.DataLoaders import *


def is_lsa_dict(arg):
    return isinstance(arg, dict) and all([x in arg for x in ['matrices', 'W', 'H', 'stemmingRules', 'stopWords']])


class SMRRepresentation(unittest.TestCase):
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
    # Queries
    queries = ["Notebook of differential equations solutions.",
               "Neural networking training process",
               "Anomaly finding in time series"]

    def test_to_dict_1(self):
        # Verify to_dict() produces a dictionary representing LatentSemanticAnalyzer object
        self.assertTrue(is_lsa_dict(self.lsaObj.to_dict()))

    def test_to_dict_2(self):
        # Verify same term-representations the original and re-created LSA objects

        # LSA dict
        lsa_dict = self.lsaObj.to_dict()

        # New LSA object
        lsaObjNew = LatentSemanticAnalyzer().from_dict(lsa_dict)

        # Representations by terms
        recs1 = self.lsaObj.represent_by_terms(query=self.queries, apply_lsi_functions=True).take_value()
        recs2 = lsaObjNew.represent_by_terms(query=self.queries, apply_lsi_functions=True).take_value()

        self.assertTrue(recs1.eq(recs2))

    def test_to_dict_3(self):
        # Verify same topics-representations the original and re-created LSA objects

        # Extract topics
        self.lsaObj = self.lsaObj.extract_topics(number_of_topics=40, method="SVD", max_steps=60)
        # LSA dict
        lsa_dict = self.lsaObj.to_dict()

        # New LSA object
        lsaObjNew = LatentSemanticAnalyzer().from_dict(lsa_dict)

        # Representations by terms
        recs1 = self.lsaObj.represent_by_topics(query=self.queries, apply_lsi_functions=True).take_value()
        recs2 = lsaObjNew.represent_by_topics(query=self.queries, apply_lsi_functions=True).take_value()

        self.assertTrue(recs1.eq(recs2))


if __name__ == '__main__':
    unittest.main()
