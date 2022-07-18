from SparseMatrixRecommender.SparseMatrixRecommender import SparseMatrixRecommender
from LatentSemanticAnalyzer.LatentSemanticAnalyzer import LatentSemanticAnalyzer
from typing import Union, Optional
import pandas
import warnings


def SMR_to_LSA(smr: SparseMatrixRecommender,
               stop_words: Union[bool, list, tuple, None] = [],
               stemming_rules: Union[bool, dict, None] = None,
               words_pattern: str = r"[\w']+|[.,!?;]",
               number_of_topics: int = 12,
               min_number_of_documents_per_term: int = 12):
    dfSMat = pandas.DataFrame(columns=["Item", "Tag", "Value"], data=smr.take_M().triplets())

    dfTexts = dfSMat.groupby(["Tag"], as_index=False).agg({"Tag": ' '.join})

    aDocs = dict(zip(dfTexts["Item"], dfTexts["Tag"]))

    lsaObj = (LatentSemanticAnalyzer(aDocs)
              .make_document_term_matrix(docs=None,
                                         stop_words=stop_words,
                                         stemming_rules=stemming_rules,
                                         words_pattern=words_pattern)
              .apply_term_weight_functions(global_weight_func="IDF",
                                           local_weight_func="None",
                                           normalizer_func="Cosine"))

    if number_of_topics >= 0:
        lsaObj = (lsaObj
                  .extract_topics(number_of_topics=number_of_topics,
                                  min_number_of_documents_per_term=min_number_of_documents_per_term,
                                  method="SVD",
                                  max_steps=100)
                  .normalize_matrix_product(normalize_left=True, order_by_significance=True))

    return lsaObj
