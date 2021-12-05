import random

import snowballstemmer
from LatentSemanticAnalyzer.DataLoaders import *
from LatentSemanticAnalyzer.LatentSemanticAnalyzer import *

# Collection of texts
dfAbstracts = load_abstracts_data_frame()
docs = dict(zip(dfAbstracts.ID, dfAbstracts.Abstract))

# Stemmer object (to preprocess words in the pipeline below)
stemmerObj = snowballstemmer.stemmer("english")

# Words to show statistical thesaurus entries for
words = ["notebook", "computational", "function", "neural", "talk", "programming"]

# Reproducible results
random.seed(987)

# LSA pipeline
lsaObj = (LatentSemanticAnalyzer()
          .make_document_term_matrix(docs=docs,
                                     stop_words=True,
                                     stemming_rules=True,
                                     min_length=3)
          .apply_term_weight_functions(global_weight_func="IDF",
                                       local_weight_func="None",
                                       normalizer_func="Cosine")
          .extract_topics(number_of_topics=40, min_number_of_documents_per_term=10, method="NNMF", max_steps=16)
          .echo_topics_interpretation(number_of_terms=12, wide_form=True)
          .echo_statistical_thesaurus(terms=stemmerObj.stemWords(words),
                                      wide_form=True,
                                      number_of_nearest_neighbors=12,
                                      method="cosine",
                                      echo_function=lambda x: print(x.to_string())))
