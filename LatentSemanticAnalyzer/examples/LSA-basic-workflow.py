import random
import pandas
from SparseMatrixRecommender import SparseMatrixRecommender
from LatentSemanticAnalyzer.LatentSemanticAnalyzer import *
from LatentSemanticAnalyzer.DocumentTermMatrixConstruction import *
from LatentSemanticAnalyzer.DataLoaders import *
import snowballstemmer

dfAbstracts = load_abstracts_data_frame()

print(dfAbstracts.head())

docs = dict(zip(dfAbstracts.ID, [str(x) for x in dfAbstracts.Abstract.tolist()]))

lsaObj = (LatentSemanticAnalyzer()
          .make_document_term_matrix(docs=docs,
                                     stop_words=True,
                                     stemming_rules=True,
                                     min_length=3)
          .apply_term_weight_functions(global_weight_func="IDF",
                                       local_weight_func="None",
                                       normalizer_func="Cosine"))

print("Document-term matrix:")
print(repr(lsaObj.take_doc_term_mat()))

(LatentSemanticAnalyzer(docs)
 .make_document_term_matrix(stemming_rules=False, stop_words=None)
 .apply_term_weight_functions(global_weight_func="IDF", local_weight_func="None", normalizer_func="Cosine")
 .extract_topics(number_of_topics=12,
                 method="NNMF",
                 max_steps=12,
                 min_number_of_documents_per_term=20)
 .echo_topics_table(number_of_terms=12))

# Further document-term matrix print-outs
# mat = lsaObj.take_doc_term_mat()
# wmat = lsaObj.take_weighted_doc_term_mat()
# focus_col_names = wmat.column_sums_dict()
# focus_col_names = [k for k, v in sorted(focus_col_names.items(), key=lambda item: -item[1])]
# print(focus_col_names[0:12])
# ids_sample = random.sample(wmat.row_names(), 20)
# lsaObj.take_weighted_doc_term_mat()[:, focus_col_names[1:40]][ids_sample, :].print_matrix(n_digits=20)

# Extract 40 topics with min number of documents per term 10
lsaObj = lsaObj.extract_topics(number_of_topics=40, min_number_of_documents_per_term=10)

# print("Topics (left) factor:")
# lsaObj.take_H().print_matrix(n_digits=25)

print(120 * "=")
print("Statistical thesaurus")
print(120 * "-")

stemmerObj = snowballstemmer.stemmer("english")
words = ["notebook", "computational", "function", "neural", "talk", "programming"]
words = stemmerObj.stemWords(words)

lsaObj = lsaObj.echo_statistical_thesaurus(terms=words,
                                           number_of_nearest_neighbors=12,
                                           method="cosine",
                                           wide_form=True,
                                           echo_function=lambda x: print(x.to_string()))

print(120 * "=")
print("Query representation")
print(120 * "-")

print("Representation by terms:")
lsaObj.represent_by_terms(
    ["This notebook is for differential equations solving.", "Anomalies of times series investigation"])

qmat = lsaObj.take_value()
qmat2 = qmat[:, [k for (k, v) in qmat.column_sums_dict().items() if v > 0]]
qmat2.print_matrix()
