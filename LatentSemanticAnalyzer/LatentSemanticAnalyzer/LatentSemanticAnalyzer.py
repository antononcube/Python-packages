from SparseMatrixRecommender import SparseMatrixRecommender
from SparseMatrixRecommender.CrossTabulate import cross_tabulate
from SparseMatrixRecommender.DocumentTermWeightFunctions import apply_term_weight_functions
from SSparseMatrix import SSparseMatrix
from SSparseMatrix import column_bind
from SSparseMatrix import is_sparse_matrix
import pandas
import scipy
import numpy
import warnings


# ======================================================================
# Utilities
# ======================================================================
def is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def is_str_dict(obj):
    return isinstance(obj, dict) and is_str_list(list(obj.keys())) and is_str_list(list(obj.values()))


# ======================================================================
# Class definition
# ======================================================================
class LatentSemanticAnalyzer:
    _docTermMat = None
    _wDocTermMat = None
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
    def set_document_term_matrix(self, arg):
        """Set document-term matrix."""
        if is_sparse_matrix(arg):
            self._docTermMat = arg
        else:
            raise TypeError("The first argument is expected to be a SSparseMatrix object.")
            return None
        return self

    def set_global_term_weights(self, arg):
        """Set global term weights value."""
        self._value = arg
        return self

    def set_value(self, arg):
        """Set pipeline value."""
        self._value = arg
        return self

    # ------------------------------------------------------------------
    # Make document-term matrix
    # ------------------------------------------------------------------
    def make_document_term_matrix(self,
                                  texts,
                                  stemming_rules=None,
                                  stop_words=None,
                                  split=[' ', ',', '.', ';', '!', '?']):

        if is_str_list(texts):
            aTexts = dict(zip(['id' + str(i) for i in range(len(texts))], texts))
        elif is_str_dict(texts):
            aTexts = texts
        else:
            raise TypeError("The argument 'texts' is expected to be a list of strings, or a dictionary of string.")

        return self

    # ------------------------------------------------------------------
    # Apply LSI functions
    # ------------------------------------------------------------------
    def apply_term_weight_functions(self,
                                    global_weight_func="IDF",
                                    local_weight_func="None",
                                    normalizer_func="Cosine"):
        """Apply LSI functions to the entries of the document-term matrix."""

        self._wDocTermMat = apply_term_weight_functions(doc_term_matrix=self._docTermMat,
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

        smat = self._docTermMat[:, ccols]

        # Compute matrix factors
        if method.lower() in {"SVD".lower(), "SingularValueDecomposition".lower()}:
            u, s, ct = scipy.sparse.linalg.svds(A=smat,
                                                k=number_of_topics,
                                                maxiter=max_steps)
        else:
            raise ValueError("The argument 'method' is expected to 'SVD'.")
            return None

        # Automatic topic names

        # Set factors
        self._W = SSparseMatrix(u, row_names=self.take_document_term_matrix().row_names())
        self._H = SSparseMatrix(ct.transpose(), column_names=self.take_document_term_matrix().column_names())

        return self
