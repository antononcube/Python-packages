from SparseMatrixRecommender import SparseMatrixRecommender
from SparseMatrixRecommender.DocumentTermWeightFunctions import apply_term_weight_functions
from LatentSemanticAnalyzer.DocumentTermMatrixConstruction import document_term_matrix
from SSparseMatrix import SSparseMatrix
from SSparseMatrix import is_sparse_matrix
import stop_words as stop_words_package
import pandas
import scipy
import scipy.sparse.linalg
import numpy


# ======================================================================
# Utilities
# ======================================================================
def _is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def _is_str_dict(obj):
    return isinstance(obj, dict) and _is_str_list(list(obj.keys())) and _is_str_list(list(obj.values()))


def _left_normalize_matrix_product(W, H):
    d = [scipy.sparse.linalg.norm(W[:, i].sparse_matrix()) for i in range(W.columns_count())]
    S = scipy.sparse.diags(diagonals=[d], offsets=[0])
    SI = scipy.sparse.diags(diagonals=[[1 / x if abs(x) > 0 else 0 for x in d]], offsets=[0])

    SI = SSparseMatrix(SI, row_names=H.row_names(), column_names=H.row_names())

    return {"W": W.dot(S), "H": SI.dot(H)}


def _right_normalize_matrix_product(W, H):
    d = [scipy.sparse.linalg.norm(H[:, i].sparse_matrix()) for i in range(H.rows_count())]
    S = scipy.sparse.diags(diagonals=[d], offsets=[0])
    SI = scipy.sparse.diags(diagonals=[[1 / x if abs(x) > 0 else 0 for x in d]], offsets=[0])

    S = SSparseMatrix(S, row_names=H.row_names(), column_names=H.row_names())

    return {"W": W.dot(SI), "H": S.dot(H)}


def _sort_dict(x):
    return dict([(k, v) for k, v in sorted(x.items(), key=lambda item: item[1])])


def _reverse_sort_dict(x):
    return dict([(k, v) for k, v in sorted(x.items(), key=lambda item: -item[1])])


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

    def set_weighted_document_term_matrix(self, arg):
        """Set weighted document-term matrix."""
        if is_sparse_matrix(arg):
            self._wDocTermMat = arg
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

        docs2 = {k: v.lower() for (k, v) in aTexts.items()}
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
        """Extract topics.

        :param number_of_topics: Number of topics to extract.
        :param min_number_of_documents_per_term: Minimum number of documents per term.
        :param method: Method for matrix factorization. (Only "SVD" currently implemented.)
        :param max_steps: Maximum number of steps for the matrix factorization algorith,
        :return self:
        """
        # Take terms present in large enough number of documents
        smat01 = self.take_document_term_matrix().unitize()
        cs = smat01.column_sums_dict()
        ccols = [key for (key, value) in cs.items() if value >= min_number_of_documents_per_term]

        smat = self.take_weighted_doc_term_mat()[:, ccols]

        # Compute matrix factors
        if method.lower() in {"SVD".lower(), "SingularValueDecomposition".lower()}:
            u, s, vt = scipy.sparse.linalg.svds(A=smat.sparse_matrix(),
                                                k=number_of_topics,
                                                maxiter=max_steps)
        else:
            raise ValueError("The argument 'method' is expected to 'SVD'.")
            return None

        # Scale V with S (in order to get H)
        svt = scipy.sparse.diags(diagonals=[s], offsets=[0]).dot(vt)

        # Automatic topic names
        topic_names = ["topic." + str(i) for i in range(u.shape[1])]

        # Set factors
        self._W = SSparseMatrix(u, row_names=smat.row_names(), column_names=topic_names)
        self._H = SSparseMatrix(svt, row_names=topic_names, column_names=smat.column_names())

        # Automatic topic names re-do
        topic_names = dict(
            [(k, k + "." + '-'.join(list(wterms.keys())[0:3]))
             for (k, wterms) in self._H.row_dictionaries(sort=True).items()])
        topic_names = [topic_names[t] for t in self._H.row_names()]

        self._H.set_row_names(topic_names)
        self._W.set_column_names(topic_names)

        return self

    # ------------------------------------------------------------------
    # Extract statistical thesaurus
    # ------------------------------------------------------------------
    def extract_statistical_thesaurus(self, words: list, n: int = 12, method: str = "euclidian"):
        """Extract statistical thesaurus.

        :param words: Words to find statistical thesaurus entries for.
        :param n: Number of nearest neighbors per word.
        :param method: Method for nearest neighbors finding.
        :param as_data_frame: Should the result be given as a data frame or not?
        :return self:
        """
        if not _is_str_list(words):
            raise TypeError("The first argument, 'words', is expected to be a list of strings.")

        factRes = _left_normalize_matrix_product(self.take_W(), self.take_H())

        my_words = [w for w in words if w in self._H.column_names_dict()]

        if len(my_words) == 0:
            raise ValueError("None of the given words are known.")

        my_words = sorted(my_words)

        # Using Cosine similarity is not a good idea
        if method.lower() == "cosine":
            smrObj = (SparseMatrixRecommender()
                      .create_from_matrices({"Words": factRes["H"].transpose()})
                      .apply_term_weight_functions(global_weight_func="None",
                                                   local_weight_func="None",
                                                   normalizer_func="Cosine"))

            res = dict([(w, smrObj.recommend(history=w, nrecs=n, remove_history=False).take_value()) for w in my_words])

        else:
            H = factRes["H"]
            res = {}
            for w in my_words:
                M = H[:, [w, ]].dot(numpy.ones([1, H.columns_count()]))
                M.set_column_names(H.column_names())
                M = M.add(H.multiply(-1))
                M = M.multiply(M)
                M = M.sparse_matrix().sqrt()
                M2 = SSparseMatrix(M, row_names=H.row_names(), column_names=H.column_names())
                dists = _sort_dict(M2.column_sums_dict())
                if len(dists) > n + 1:
                    dists = dict(list(dists.items())[0:n + 1])
                res = res | {w: dists}

        self.set_value(res)
        return self

    # ------------------------------------------------------------------
    # Get statistical thesaurus
    # ------------------------------------------------------------------
    def get_statistical_thesaurus(self, words,
                                  number_of_nearest_neighbors=12,
                                  method="cosine",
                                  as_data_frame=True,
                                  wide_form=False,
                                  echo=True,
                                  echo_function=print):
        """Get statistical thesaurus table.

        :param words: Words to find thesaurus entries for.
        :param number_of_nearest_neighbors: Number of nearest neighbors per specified word.
        :param method: Method for nearest neighbors finding.
        :param as_data_frame: Should the result be a data frame (or a dictionary)?
        :param wide_form: Should the thesaurus data frame (table) be in wide form or not?
        :param echo: Should the thesaurus data frame (table) be echoed or not?
        :param echo_function: Echo function.
        :return self:
        """

        my_words = words
        if words is None and _is_str_list(self.take_value()):
            my_words = self.take_value()

        self.extract_statistical_thesaurus(words=my_words,
                                           n=number_of_nearest_neighbors,
                                           method=method)

        if as_data_frame:
            if wide_form:
                dfRes = pandas.DataFrame({k: list(v.keys()) for (k, v) in self.take_value().items()})
                dfRes = dfRes.transpose()
            else:
                dfRes = [pandas.DataFrame({"SearchTerm": k, "Term": v.keys(), "Term.Distance": v.values()})
                         for (k, v) in self.take_value().items()]
                dfRes = pandas.concat(dfRes)

        self.set_value(dfRes)

        if echo:
            echo_function(dfRes)

        return self

    # ------------------------------------------------------------------
    # Echo statistical thesaurus
    # ------------------------------------------------------------------
    def echo_statistical_thesaurus(self,
                                   words=None,
                                   number_of_nearest_neighbors=12,
                                   method="cosine",
                                   as_data_frame=True,
                                   wide_form=False,
                                   echo_function=lambda x: print(x.to_string())):
        """Echo statistical thesaurus.

        :param words: Words to find thesaurus entries for.
        :param number_of_nearest_neighbors: Number of nearest neighbors per specified word.
        :param method: Method for nearest neighbors finding.
        :param as_data_frame: Should the result be a data frame (or a dictionary)?
        :param wide_form: Should the thesaurus data frame (table) be in wide form or not?
        :param echo_function: Echo function.
        :return self:
        """
        self.get_statistical_thesaurus(words=words,
                                       number_of_nearest_neighbors=number_of_nearest_neighbors,
                                       method=method,
                                       as_data_frame=as_data_frame,
                                       wide_form=wide_form,
                                       echo=True,
                                       echo_function=echo_function)
        return self
