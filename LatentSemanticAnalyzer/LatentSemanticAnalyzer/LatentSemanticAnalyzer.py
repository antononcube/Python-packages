from SparseMatrixRecommender import SparseMatrixRecommender
from SparseMatrixRecommender.CrossTabulate import cross_tabulate
from SparseMatrixRecommender.DocumentTermWeightFunctions import apply_term_weight_functions
from LatentSemanticAnalyzer.DocumentTermMatrixConstruction import document_term_matrix
from SSparseMatrix import SSparseMatrix
from SSparseMatrix import column_bind
from SSparseMatrix import is_sparse_matrix
import stop_words as stop_words_package
import pandas
import scipy
import scipy.sparse.linalg
import numpy
import warnings


# ======================================================================
# Utilities
# ======================================================================
def _is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def _is_str_dict(obj):
    return isinstance(obj, dict) and _is_str_list(list(obj.keys())) and _is_str_list(list(obj.values()))


# ======================================================================
# Class definition
# ======================================================================
class LatentSemanticAnalyzer:
    _documents = None
    _docTermMat = None
    _wDocTermMat = None
    _terms = None,
    _stopWords = None,
    _stemmingRules = None,
    _W = None
    _H = None
    _globalWeights = None
    _stemRules = None
    _value = None

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------
    def __init__(*args):
        if len(args) == 1 and isinstance(args[0], pandas.core.frame.DataFrame):
            _data = args[0]
        elif len(args) == 1 and is_sparse_matrix(args[0]):
            _docTermMat = args[0]

    # ------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------
    def take_documents(self):
        """Take the documents."""
        return self._documents

    def take_document_term_matrix(self):
        """Take the document-term matrix."""
        return self._docTermMat

    def take_weighted_document_term_matrix(self):
        """Take the weighted document-term matrix."""
        return self._wDocTermMat

    def take_doc_term_mat(self):
        """Take the document-term matrix."""
        return self._docTermMat

    def take_weighted_doc_term_mat(self):
        """Take the document-term matrix."""
        return self._wDocTermMat

    def take_terms(self):
        """Take the terms."""
        return self._terms

    def take_stop_words(self):
        """Take the stop words."""
        return self._stopWords

    def take_stemming_rules(self):
        """Take the stemming rules."""
        return self._stemmingRules

    def take_W(self):
        """Take the left factor matrix."""
        return self._W

    def take_H(self):
        """Take the right factor matrix."""
        return self._H

    def take_global_term_weights(self):
        """Take the global term weights."""
        return self._data

    def take_value(self):
        """Take the pipeline value."""
        return self._value

    # ------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------
    def set_documents(self, arg):
        """Set documents."""
        if _is_str_list(arg) or _is_str_dict(arg):
            self._documents = arg
        else:
            raise TypeError("The first argument is expected to be a list of strings or a dictionary of strings.")
        return self

    def set_document_term_matrix(self, arg):
        """Set document-term matrix."""
        if is_sparse_matrix(arg):
            self._docTermMat = arg
            self._terms = arg.column_names()
        else:
            raise TypeError("The first argument is expected to be a SSparseMatrix object.")
            return None
        return self

    def set_global_term_weights(self, arg):
        """Set global term weights value."""
        self._globalWeights = arg
        return self

    def set_terms(self, arg):
        """Set terms."""
        self._terms = arg
        return self

    def set_stop_words(self, arg):
        """Set stop words value."""
        self._stopWords = arg
        return self

    def set_stop_words(self, arg):
        """Set stop words value."""
        self._stopWords = arg
        return self

    def set_stemming_rules(self, arg):
        """Set stemming rules."""
        self._stemmingRules = arg
        return self

    def set_value(self, arg):
        """Set pipeline value."""
        self._value = arg
        return self

    # ------------------------------------------------------------------
    # Make document-term matrix
    # ------------------------------------------------------------------
    def make_document_term_matrix(self,
                                  docs,
                                  stop_words: list = [],
                                  stemming_rules=None,
                                  words_pattern="[\w']+|[.,!?;]",
                                  min_length: int = 2):

        if _is_str_list(docs):
            aTexts = dict(zip(['id' + str(i) for i in range(len(docs))], docs))
        elif _is_str_dict(docs):
            aTexts = docs
        else:
            raise TypeError("The argument 'docs' is expected to be a list of strings, or a dictionary of string.")

        mstop_words = stop_words
        if isinstance(stop_words, bool) and stop_words:
            mstop_words = stop_words_package.get_stop_words('english')

        docs2 = [x.lower() for x in docs]
        docTermMat = document_term_matrix(docs=docs2,
                                          stop_words=mstop_words,
                                          stemming_rules=stemming_rules,
                                          words_pattern=words_pattern,
                                          min_length=min_length)

        self.set_documents(docs2)
        self.set_document_term_matrix(docTermMat)
        self.set_terms(docTermMat.column_names())
        self.set_stop_words(stop_words)
        self.set_stemming_rules(stemming_rules)

        return self

    # ------------------------------------------------------------------
    # Apply LSI functions
    # ------------------------------------------------------------------
    def apply_term_weight_functions(self,
                                    global_weight_func="IDF",
                                    local_weight_func="None",
                                    normalizer_func="Cosine"):
        """Apply LSI functions to the entries of the document-term matrix."""

        self._wDocTermMat = apply_term_weight_functions(doc_term_matrix=self.take_doc_term_mat(),
                                                        global_weight_func=global_weight_func,
                                                        local_weight_func=local_weight_func,
                                                        normalizer_func=normalizer_func)

        return self

    # ------------------------------------------------------------------
    # Extract topics
    # ------------------------------------------------------------------
    def extract_topics(self,
                       number_of_topics: int = 12,
                       min_number_of_documents_per_term: int = 12,
                       method: str = "SVD",
                       max_steps: int = 100):

        # Take terms present in large enough number of documents
        smat01 = self.take_document_term_matrix().unitize()
        cs = smat01.column_sums_dict()
        ccols = [key for (key, value) in cs.items() if value > min_number_of_documents_per_term]

        smat = self.take_weighted_doc_term_mat()[:, ccols]

        # Compute matrix factors
        if method.lower() in {"SVD".lower(), "SingularValueDecomposition".lower()}:
            u, s, ct = scipy.sparse.linalg.svds(A=smat.sparse_matrix(),
                                                k=number_of_topics,
                                                maxiter=max_steps)
        else:
            raise ValueError("The argument 'method' is expected to 'SVD'.")
            return None

        # Automatic topic names
        topic_names = ["topic." + str(i) for i in range(u.shape[1])]

        # Set factors
        self._W = SSparseMatrix(u, row_names=smat.row_names(), column_names=topic_names)
        self._H = SSparseMatrix(ct, row_names=topic_names, column_names=smat.column_names())

        # Automatic topic names re-do
        topic_names = dict(
            [(k, k + "." + '-'.join(list(wterms.keys())[0:3]))
             for (k, wterms) in self._H.row_dictionaries(sort=True).items()])
        topic_names = [topic_names[t] for t in self._H.row_names()]

        self._H.set_row_names(topic_names)
        self._W.set_column_names(topic_names)

        return self
