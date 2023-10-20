import math
import pickle
import warnings
from typing import Union, Optional

import nimfa
import numpy
import pandas
import scipy
import scipy.sparse.linalg
import stop_words as stop_words_package
from LatentSemanticAnalyzer.DocumentTermMatrixConstruction import document_term_matrix
from SSparseMatrix import SSparseMatrix
from SSparseMatrix import is_s_sparse_matrix
from SparseMatrixRecommender import SparseMatrixRecommender
from SparseMatrixRecommender.DocumentTermWeightFunctions import apply_term_weight_functions
from SparseMatrixRecommender.DocumentTermWeightFunctions import global_term_function_weights


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
    SI = scipy.sparse.diags(diagonals=[[1 / x if abs(x) > 0 else 1 for x in d]], offsets=[0])

    S = SSparseMatrix(S, row_names=H.row_names(), column_names=H.row_names())

    return {"W": W.dot(SI).set_column_names(W.column_names()), "H": S.dot(H)}


def _right_normalize_matrix_product(W, H):
    d = [scipy.sparse.linalg.norm(H[i, :].sparse_matrix()) for i in range(H.rows_count())]
    S = scipy.sparse.diags(diagonals=[d], offsets=[0])
    SI = scipy.sparse.diags(diagonals=[[1 / x if abs(x) > 0 else 1 for x in d]], offsets=[0])

    SI = SSparseMatrix(SI, row_names=H.row_names(), column_names=H.row_names())

    return {"W": W.dot(S).set_column_names(W.column_names()), "H": SI.dot(H)}


def _sort_dict(x):
    return dict([(k, v) for k, v in sorted(x.items(), key=lambda item: item[1])])


def _reverse_sort_dict(x):
    return dict([(k, v) for k, v in sorted(x.items(), key=lambda item: -item[1])])


# ======================================================================
# Class definition
# ======================================================================
class LatentSemanticAnalyzer:
    _documents: Optional[dict] = None
    _docTermMat: Optional[SSparseMatrix] = None
    _wDocTermMat: Optional[SSparseMatrix] = None
    _terms = None,
    _stopWords = None,
    _stemmingRules = None,
    _W: Optional[SSparseMatrix] = None
    _H: Optional[SSparseMatrix] = None
    _globalWeights = None
    _localWeightFunction = None
    _normalizerFunction = None
    _method = None
    _stemRules = None
    _wordsPattern = None
    _value = None

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Creation of LatentSemanticAnalyzer object.

        The first (optional) argument is expected to be a data frame or SSparseMatrix object.
        """
        if len(args) == 1 and (_is_str_dict(args[0]) or _is_str_list(args[0])):
            self.set_documents(args[0])
        elif len(args) == 1 and is_s_sparse_matrix(args[0]):
            self.set_document_term_matrix(args[0])

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

    def take_words_pattern(self):
        """Take the words pattern."""
        return self._wordsPattern

    def take_W(self):
        """Take the left factor matrix."""
        return self._W

    def take_H(self):
        """Take the right factor matrix."""
        return self._H

    def take_global_term_weights(self):
        """Take the global term weights."""
        return self._globalWeights

    def take_local_weight_function(self):
        """Take the local weight function."""
        return self._localWeightFunction

    def take_normalizer_function(self):
        """Take the normalizer function."""
        return self._normalizerFunction

    def take_method(self):
        """Take the method."""
        return self._method

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
        if is_s_sparse_matrix(arg):
            self._docTermMat = arg
            self._terms = arg.column_names()
        else:
            raise TypeError("The first argument is expected to be a SSparseMatrix object.")
        return self

    def set_weighted_document_term_matrix(self, arg):
        """Set weighted document-term matrix."""
        if is_s_sparse_matrix(arg):
            self._wDocTermMat = arg
            self._terms = arg.column_names()
        else:
            raise TypeError("The first argument is expected to be a SSparseMatrix object.")
        return self

    def set_global_term_weights(self, arg):
        """Set global term weights value."""
        self._globalWeights = arg
        return self

    def set_local_weight_function(self, arg):
        """Set local term weight function."""
        self._localWeightFunction = arg
        return self

    def set_normalizer_function(self, arg):
        """Set normalizer function."""
        self._normalizerFunction = arg
        return self

    def set_W(self, arg):
        """Set the left matrix factor W."""
        self._W = arg
        return self

    def set_H(self, arg):
        """Set right matrix factor H."""
        self._H = arg
        return self

    def set_method(self, arg):
        """Set the method."""
        self._method = arg
        return self

    def set_terms(self, arg):
        """Set terms."""
        self._terms = arg
        return self

    def set_stop_words(self, arg):
        """Set stop words value."""
        self._stopWords = arg
        return self

    def set_stemming_rules(self, arg):
        """Set stemming rules."""
        self._stemmingRules = arg
        return self

    def set_words_pattern(self, arg):
        """Set words pattern."""
        self._wordsPattern = arg
        return self

    def set_value(self, arg):
        """Set pipeline value."""
        self._value = arg
        return self

    # ------------------------------------------------------------------
    # Copying
    # ------------------------------------------------------------------
    def copy(self):
        """Deep copy."""
        return pickle.loads(pickle.dumps(self, -1))

    def __copy__(self):
        """Deep copy."""
        return pickle.loads(pickle.dumps(self, -1))

    def __deepcopy__(self, memodict={}):
        """Deep copy."""
        return pickle.loads(pickle.dumps(self, -1))

    # ------------------------------------------------------------------
    # Make document-term matrix
    # ------------------------------------------------------------------
    def make_document_term_matrix(self,
                                  docs: Union[dict, list, None] = None,
                                  stop_words: Union[bool, list, tuple, None] = [],
                                  stemming_rules: Union[bool, dict, None] = None,
                                  words_pattern: str = r"[\w']+|[.,!?;]",
                                  min_length: int = 2):
        """Make document-term matrix.

        :type docs: dict|list|None
        :param docs: A collection of documents. If None then self.take_documents() is used.

        :type stop_words: bool|list|tuple|None
        :param stop_words: Stop words to remove from the documents.

        :type stemming_rules: bool|dict|None
        :param stemming_rules: A dictionary of stemming rules. Or a Boolean value should stemming be applied or not.

        :type words_pattern: str
        :param words_pattern: Regex pattern to extract words with.

        :type min_length: int
        :param min_length: Minimal string length of extracted words (that are used in the computations.)

        :rtype: LatentSemanticAnalyzer
        :return self:
        """

        # Note that self.set_documents(docs) checks the type of the argument docs.
        # Hence, we do not need a separate check and TypeError that test and clarifies
        # that self._documents is right or wrong.

        if docs is None:
            aTexts = self.take_documents()
            if aTexts is None:
                raise TypeError("Cannot find documents.")
        elif _is_str_list(docs):
            aTexts = dict(zip(['id' + str(i) for i in range(len(docs))], docs))
        elif _is_str_dict(docs):
            aTexts = docs
        else:
            raise TypeError(
                "The argument 'docs' is expected to be a list of strings, a dictionary of strings, or None.")

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
        self.set_words_pattern(words_pattern)

        return self

    # ------------------------------------------------------------------
    # Apply LSI functions
    # ------------------------------------------------------------------
    def apply_term_weight_functions(self,
                                    global_weight_func: str = "IDF",
                                    local_weight_func: str = "None",
                                    normalizer_func: str = "Cosine"):
        """Apply LSI functions to the entries of the document-term matrix.

        :param global_weight_func: Global term weight function.
        :param local_weight_func: Local term weight function.
        :param normalizer_func: Normalizer function.
        :return self:
        """

        if not is_s_sparse_matrix(self.take_doc_term_mat()):
            raise AttributeError("There is no document-term matrix")

        self._wDocTermMat = apply_term_weight_functions(doc_term_matrix=self.take_doc_term_mat(),
                                                        global_weight_func=global_weight_func,
                                                        local_weight_func=local_weight_func,
                                                        normalizer_func=normalizer_func)

        globalWeights = global_term_function_weights(doc_term_matrix=self.take_doc_term_mat())

        self.set_global_term_weights(globalWeights)
        self.set_local_weight_function(local_weight_func)
        self.set_normalizer_function(normalizer_func)

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

        if not is_s_sparse_matrix(self.take_weighted_doc_term_mat()):
            raise AttributeError("There is no weighted document-term matrix")

        # Take terms present in large enough number of documents
        smat01 = self.take_document_term_matrix().unitize()
        cs = smat01.column_sums_dict()
        ccols = [key for (key, value) in cs.items() if value >= min_number_of_documents_per_term]

        smat = self.take_weighted_doc_term_mat()[:, ccols]

        # Compute matrix factors
        if method.lower() in {"SVD".lower(), "SingularValueDecomposition".lower()}:

            W, s, vt = scipy.sparse.linalg.svds(A=smat.sparse_matrix(),
                                                k=number_of_topics,
                                                maxiter=max_steps)
            # Scale V with S (in order to get H)
            H = scipy.sparse.diags(diagonals=[s], offsets=[0]).dot(vt)
            self.set_method("SVD")

        elif method.lower() in set([x.lower() for x in ["NMF", "NNMF", "NonNegativeMatrixFactorization"]]):

            minSMat = min(smat.sparse_matrix().data)
            maxSMat = max(smat.sparse_matrix().data)

            if minSMat < 0:
                warnings.warn("The weighted document term matrix has negative elements. " +
                              "Continuing by clipping negative elements (in order to apply NNMF.)")
                smat = smat.clip(0, maxSMat)

            nmf = nimfa.Lsnmf(V=smat.sparse_matrix(),
                              seed='random_vcol',
                              rank=number_of_topics,
                              max_iter=max_steps)

            nmfRes = nmf()
            W = nmfRes.fit.W
            H = nmfRes.fit.H
            self.set_method("NNMF")

        else:
            raise ValueError("""The argument 'method' is expected to be one of 'SVD', 'SingularValueDecomposition', 
            'NonNegativeMatrixFactorization', or 'NNMF'.""")

        # Automatic topic names
        nd = math.ceil(math.log10(number_of_topics)) + 1
        topic_names = ["tpc." + str(i).zfill(nd) for i in range(W.shape[1])]

        # Set factors
        self._W = SSparseMatrix(W, row_names=smat.row_names(), column_names=topic_names)
        self._H = SSparseMatrix(H, row_names=topic_names, column_names=smat.column_names())

        # Automatic topic names re-do
        topic_names = dict(
            [(k, k + "." + '-'.join(list(wterms.keys())[0:3]))
             for (k, wterms) in self._H.row_dictionaries(sort=True).items()])
        topic_names = [topic_names[t] for t in self._H.row_names()]

        self._H.set_row_names(topic_names)
        self._W.set_column_names(topic_names)

        return self

    # ------------------------------------------------------------------
    # Normalized matrix product components
    # ------------------------------------------------------------------
    def normalize_matrix_product(self,
                                 normalize_left: bool = True,
                                 order_by_significance: bool = True):
        """Normalized matrix product components.

        :param normalize_left: Should the left component be normalized or not?
        :param order_by_significance: Should the basis vectors be ordered by their significance?
        :return self:
        """
        if not (is_s_sparse_matrix(self.take_W()) and is_s_sparse_matrix(self.take_H())):
            raise AttributeError("Cannot find matrix factors.")

        if normalize_left:
            nres = _left_normalize_matrix_product(self.take_W(), self.take_H())
        else:
            nres = _right_normalize_matrix_product(self.take_W(), self.take_H())

        if order_by_significance:
            if normalize_left:
                topicSFactors = nres["H"].multiply(nres["H"]).row_sums_dict()
            else:
                topicSFactors = nres["W"].multiply(nres["W"]).column_sums_dict()

            # Not really needed
            # topicSFactors = {k: math.sqrt(v) for (k, v) in topicSFactors.items()}

            topicSFactors = _reverse_sort_dict(topicSFactors)
            nres["W"] = nres["W"][:, list(topicSFactors.keys())]
            nres["H"] = nres["H"][list(topicSFactors.keys()), :]

        self._W = nres["W"]
        self._H = nres["H"]

        return self

    # ------------------------------------------------------------------
    # Get topics interpretation
    # ------------------------------------------------------------------
    def get_topics_interpretation(self,
                                  number_of_terms: int = 12,
                                  as_data_frame=False,
                                  wide_form=False,
                                  echo=True,
                                  echo_function=print):
        """Get topics interpretation.

        :param number_of_terms: Number of terms per topic.
        :param as_data_frame: Should the result be a data frame or not?
        :param wide_form: Should the topics data frame (table) be in wide form or not?
        :param echo: Should the result be echoed or not?
        :param echo_function: Echo function
        :return self:
        """
        if number_of_terms < 1:
            raise TypeError("The argument 'number_of_terms' is expected to be a positive integer.")

        if not (is_s_sparse_matrix(self.take_W()) and is_s_sparse_matrix(self.take_H())):
            raise AttributeError("Cannot find matrix factors.")

        topics = self.take_H().row_dictionaries(sort=True)
        topics = {k: dict(list(v.items())[0:number_of_terms]) for (k, v) in topics.items()}

        if as_data_frame:
            if wide_form:
                dfRes = pandas.DataFrame({k: list(v.keys()) for (k, v) in topics.items()})
                dfRes = dfRes.transpose()
            else:
                dfRes = [pandas.DataFrame({"Topic": k, "Term": v.keys(), "Score": v.values()})
                         for (k, v) in topics.items()]
                dfRes = pandas.concat(dfRes)
        else:
            dfRes = topics

        self.set_value(dfRes)

        if echo:
            if callable(echo_function):
                echo_function(dfRes)
            else:
                raise TypeError("The specified echo function is not a callable object.")

        return self

    # ------------------------------------------------------------------
    # Echo topics table
    # ------------------------------------------------------------------
    def echo_topics_table(self, *args, **kwargs):
        """Echo topics table. Synonym of echo_topics_interpretation.
        """
        return self.echo_topics_interpretation(*args, **kwargs)

    # ------------------------------------------------------------------
    # Echo topics interpretation
    # ------------------------------------------------------------------
    def echo_topics_interpretation(self,
                                   number_of_terms: int = 12,
                                   as_data_frame: bool = True,
                                   wide_form: bool = False,
                                   echo_function=lambda x: print(x.to_string())):
        """Echo topics table.

        :param number_of_terms: Number of terms per topic.
        :param as_data_frame: Should the result be a data frame or not?
        :param wide_form: Should the topics data frame (table) be in wide form or not?
        :param echo_function: Echo function
        :return self:
        """
        self.get_topics_interpretation(number_of_terms=number_of_terms,
                                       as_data_frame=as_data_frame,
                                       wide_form=wide_form,
                                       echo=True,
                                       echo_function=echo_function)
        return self

    # ------------------------------------------------------------------
    # Extract statistical thesaurus
    # ------------------------------------------------------------------
    def extract_statistical_thesaurus(self,
                                      terms: list,
                                      n: int = 12,
                                      method: str = "euclidean"):
        """Extract statistical thesaurus.

        :param terms: Words to find statistical thesaurus entries for.
        :param n: Number of nearest neighbors per word.
        :param method: Method for nearest neighbors finding.
        :return self:
        """
        if not (is_s_sparse_matrix(self.take_W()) and is_s_sparse_matrix(self.take_H())):
            raise AttributeError("Cannot find matrix factors.")

        if not _is_str_list(terms):
            raise TypeError("The first argument, 'words', is expected to be a list of strings.")

        factRes = _left_normalize_matrix_product(self.take_W(), self.take_H())

        my_words = [w for w in terms if w in self._H.column_names_dict()]

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
    def get_statistical_thesaurus(self,
                                  terms=None,
                                  number_of_nearest_neighbors: int = 12,
                                  method: str = "cosine",
                                  as_data_frame: bool = True,
                                  wide_form: bool = False,
                                  echo: bool = True,
                                  echo_function=print):
        """Get statistical thesaurus table.

        :param terms: Words to find thesaurus entries for.
        :param number_of_nearest_neighbors: Number of nearest neighbors per specified word.
        :param method: Method for nearest neighbors finding.
        :param as_data_frame: Should the result be a data frame (or a dictionary)?
        :param wide_form: Should the thesaurus data frame (table) be in wide form or not?
        :param echo: Should the thesaurus data frame (table) be echoed or not?
        :param echo_function: Echo function.
        :return self:
        """

        my_words = terms
        if terms is None and _is_str_list(self.take_value()):
            my_words = self.take_value()

        self.extract_statistical_thesaurus(terms=my_words,
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
            if callable(echo_function):
                echo_function(dfRes)
            else:
                raise TypeError("The specified echo function is not a callable object.")

        return self

    # ------------------------------------------------------------------
    # Echo statistical thesaurus
    # ------------------------------------------------------------------
    def echo_statistical_thesaurus(self,
                                   terms=None,
                                   number_of_nearest_neighbors: int = 12,
                                   method: str = "cosine",
                                   as_data_frame: bool = True,
                                   wide_form: bool = False,
                                   echo_function=lambda x: print(x.to_string())):
        """Echo statistical thesaurus.

        :param terms: Words to find thesaurus entries for.
        :param number_of_nearest_neighbors: Number of nearest neighbors per specified word.
        :param method: Method for nearest neighbors finding.
        :param as_data_frame: Should the result be a data frame (or a dictionary)?
        :param wide_form: Should the thesaurus data frame (table) be in wide form or not?
        :param echo_function: Echo function.
        :return self:
        """
        self.get_statistical_thesaurus(terms=terms,
                                       number_of_nearest_neighbors=number_of_nearest_neighbors,
                                       method=method,
                                       as_data_frame=as_data_frame,
                                       wide_form=wide_form,
                                       echo=True,
                                       echo_function=echo_function)
        return self

    # ------------------------------------------------------------------
    # Represent by terms
    # ------------------------------------------------------------------
    def represent_by_terms(self,
                           query,
                           apply_lsi_functions: bool = True):
        """Represent by terms.

        :param query: A vector of strings or a sparse matrix to be represented in the
        space of monad's (weighted) document-term matrix.
        :param apply_lsi_functions: Should the LSI weight term functions be applied to the result matrix or not?
        :return self:
        """
        if not (is_s_sparse_matrix(self.take_doc_term_mat()) or
                is_s_sparse_matrix(self.take_weighted_doc_term_mat())):
            raise AttributeError("Cannot document-term matrix.")

        if isinstance(query, str):

            return self.represent_by_terms(query=[query, ], apply_lsi_functions=apply_lsi_functions)

        elif _is_str_list(query):

            qmat = (LatentSemanticAnalyzer()
                    .make_document_term_matrix(docs=query,
                                               stemming_rules=self.take_stemming_rules(),
                                               stop_words=self.take_stop_words(),
                                               words_pattern=self.take_words_pattern())
                    .take_doc_term_mat())

            return self.represent_by_terms(query=qmat, apply_lsi_functions=apply_lsi_functions)

        elif is_s_sparse_matrix(query):

            if is_s_sparse_matrix(self.take_doc_term_mat()):
                qmat = query.impose_column_names(self.take_doc_term_mat().column_names())
            else:
                qmat = query.impose_column_names(self.take_weighted_doc_term_mat().column_names())

            if qmat.sparse_matrix().sum() == 0:
                raise ValueError("The obtained query matrix has not entries.")

            if apply_lsi_functions:

                if self.take_global_term_weights() is None or \
                        self.take_local_weight_function() is None or \
                        self.take_normalizer_function() is None:
                    raise AttributeError("""If the argument 'apply_lsi_functions' is True
                    then the monad context is expected to have the elements 
                    '_globalWeights', '_localWeightFunction', '_normalizerFunction'.""")

                qmat = apply_term_weight_functions(doc_term_matrix=qmat,
                                                   global_weight_func=self.take_global_term_weights(),
                                                   local_weight_func=self.take_local_weight_function(),
                                                   normalizer_func=self.take_normalizer_function())

            self.set_value(qmat)

        else:
            raise TypeError("Unknown type of the argument 'query'.")

        return self

    # ------------------------------------------------------------------
    # Represent by topics
    # ------------------------------------------------------------------
    def represent_by_topics(self,
                            query,
                            apply_lsi_functions: bool = True,
                            method: str = "algebraic"):
        """Represent by topics.

        :param query: A vector of strings or a sparse matrix to be represented in the space of monad's document-term matrix.
        :param apply_lsi_functions: Should the LSI weight term functions be applied to the result matrix or not?
        :param method: Method to find the topics representation with; one of 'algebraic' or 'recommendation'.
        :return self:
        """
        if not (is_s_sparse_matrix(self.take_W()) and is_s_sparse_matrix(self.take_H())):
            raise AttributeError("Cannot find matrix factors.")

        if method.lower() not in {"algebraic", "recommendation"}:
            raise TypeError("The argument method is expected to be NULL or one of 'algebraic' or 'recommendation'.")

        if isinstance(query, str):

            return self.represent_by_topics(query=[query, ], apply_lsi_functions=apply_lsi_functions, method=method)

        elif _is_str_list(query):

            qmat = self.represent_by_terms(query=query, apply_lsi_functions=apply_lsi_functions).take_value()

            return self.represent_by_topics(query=qmat, apply_lsi_functions=apply_lsi_functions, method=method)

        elif is_s_sparse_matrix(query):

            qmat = self.represent_by_terms(query=query, apply_lsi_functions=apply_lsi_functions).take_value()

            qmat = qmat.impose_column_names(self.take_H().column_names())

            self.normalize_matrix_product(normalize_left=False)

            if qmat.sparse_matrix().sum() == 0:
                raise ValueError("The obtained query matrix has not entries.")

            if method.lower() == "recommendation":

                # Same as SVD
                qmat = qmat.dot(self.take_H().transpose())

            elif isinstance(self.take_method(), str) and self.take_method().lower() == "nnmf":

                # invH = self.take_H()
                # invH = SSparseMatrix(scipy.sparse.linalg.inv(invH.sparse_matrix()),
                #                      row_names=self.take_H().column_names(),
                #                      column_names=self.take_H().row_names())
                # qmat = qmat.dot(invH)
                raise ValueError("Algebraic 'nnmf' is not implemented.")

            elif isinstance(self.take_method(), str) and self.take_method().lower() == "svd":

                qmat = qmat.dot(self.take_H().transpose())

            else:
                raise ValueError("Unknown value of self._method.")

            self.set_value(qmat)

        else:
            raise TypeError("Unknown type of the argument 'query'.")

        return self

    # ------------------------------------------------------------------
    # Echo document term matrix statistics
    # ------------------------------------------------------------------
    def echo_document_term_matrix_statistics(self,
                                             log_base: Union[float, int, None] = None):
        print("Document-term matrix:")
        print(repr(self.take_doc_term_mat()))

        # Number of terms per document
        x = self.take_doc_term_mat().unitize().row_sums()

        cor = ""
        if isinstance(log_base, (int, float)) and log_base > 0:
            x = [math.log(y, log_base) for y in x]
            cor = " (log " + str(log_base) + ")"

        print("Number of terms per document" + cor + ":")
        print("\tmin:    ", numpy.min(x))
        print("\tmean:   ", numpy.mean(x))
        print("\tmedian: ", numpy.median(x))
        print("\tmax:    ", numpy.max(x))
        print("\tstd:    ", numpy.std(x))

        x = self.take_doc_term_mat().unitize().column_sums()

        if isinstance(log_base, (int, float)) and log_base > 0:
            x = [math.log(y, log_base) for y in x]

        print("Number of documents per term" + cor + ":")
        print("\tmin:    ", numpy.min(x))
        print("\tmean:   ", numpy.mean(x))
        print("\tmedian: ", numpy.median(x))
        print("\tmax:    ", numpy.max(x))
        print("\tstd:    ", numpy.std(x))

        return self

    # ------------------------------------------------------------------
    # To dictionary form
    # ------------------------------------------------------------------
    def to_dict(self):
        """Convert to dictionary form.

        Returns dictionary representation of the LatentSemanticAnalyzer object with keys:
        ['matrices', 'W', 'H', 'stemmingRules', 'stopWords', ...].

        The value of the keys 'matrices' is a dictionary of dictionaries.

        (Ideally) this function facilitates rapid conversion and serialization.
        """
        dictDT = None
        if is_s_sparse_matrix(self.take_doc_term_mat()):
            dictDT = self.take_doc_term_mat().to_dict()

        dictWDT = None
        if is_s_sparse_matrix(self.take_weighted_doc_term_mat()):
            dictWDT = self.take_weighted_doc_term_mat().to_dict()

        res = {"matrices": {"docTermMat": dictDT, "wDocTermMat": dictWDT},
               "W": self.take_W(),
               "H": self.take_H(),
               "stemmingRules": self.take_stemming_rules(),
               "stopWords": self.take_stop_words(),
               "globalWeights": self.take_global_term_weights(),
               "localWeightFunction": self.take_local_weight_function(),
               "normalizerFunction": self.take_normalizer_function(),
               "method": self.take_method(),
               "value": self.take_value()}
        return res

    # ------------------------------------------------------------------
    # From dictionary form
    # ------------------------------------------------------------------
    def from_dict(self, arg):
        """Convert from dictionary form.

        Creates a LatentSemanticAnalyzer object from a dictionary representation with keys:
        ['matrices', 'W', 'H', 'stemmingRules', 'stopWords', ...].

        The value of the keys 'matrices' is expected to be a dictionary of dictionaries.

        (Ideally) this function facilitates rapid conversion and serialization.
        """
        if not (isinstance(arg, dict) and
                all([x in arg for x in ['matrices', 'W', 'H', 'stemmingRules', 'stopWords']])):
            raise TypeError("""The first argument is expected to be a dictionary with keys:
            'matrices', 'W', 'H', 'stemmingRules', 'stopWords'.""")

        if not (isinstance(arg["matrices"], dict) and
                "docTermMat" in arg["matrices"] and
                "wDocTermMat" in arg["matrices"] and
                all([isinstance(x, dict) or x is None for x in list(arg["matrices"].values())])):
            raise TypeError("""The value of 'matrices' is expected to be a dictionary of dictionaries or Nones
            and with keys docTermMat and wDocTermMat.""")

        if arg["matrices"]["docTermMat"] is None:
            self.set_document_term_matrix(None)
        else:
            self.set_document_term_matrix(SSparseMatrix().from_dict(arg["matrices"]["docTermMat"]))

        if arg["matrices"]["wDocTermMat"] is None:
            self.set_weighted_document_term_matrix(None)
        else:
            self.set_weighted_document_term_matrix(SSparseMatrix().from_dict(arg["matrices"]["wDocTermMat"]))

        self.set_stemming_rules(arg["stemmingRules"])
        self.set_W(arg["W"])
        self.set_H(arg["H"])
        self.set_stop_words(arg["stopWords"])
        self.set_global_term_weights(arg["globalWeights"])
        self.set_method(arg["method"])
        self.set_value(arg["value"])
        self.set_local_weight_function(arg["localWeightFunction"])
        self.set_normalizer_function(arg["normalizerFunction"])
        return self

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------
    def __str__(self):
        if is_s_sparse_matrix(self.take_doc_term_mat()):
            res = "LatentSemanticAnalyzer object with %d documents and %d terms." % self.take_doc_term_mat().shape()
        elif is_s_sparse_matrix(self.take_weighted_doc_term_mat()):
            res = "LatentSemanticAnalyzer object with %d documents and %d terms." % \
                  self.take_weighted_doc_term_mat().shape()
        else:
            res = "LatentSemanticAnalyzer object with no document-term matrix."
        return res

    def __repr__(self):
        """Representation of LatentSemanticAnalyzer object."""
        nTopics = self.take_H().rows_count() if is_s_sparse_matrix(self.take_H()) else 0
        if is_s_sparse_matrix(self.take_doc_term_mat()):
            tpls = (self.take_doc_term_mat().sparse_matrix().shape + (nTopics,))
            return "<LatentSemanticAnalyzer object with document-term matrix dimensions %dx%d\n" \
                   "\tand with %d extracted topics>" % tpls
        elif is_s_sparse_matrix(self.take_weighted_doc_term_mat()):
            tpls = (self.take_weighted_doc_term_mat().sparse_matrix().shape + (nTopics,))
            return "<LatentSemanticAnalyzer object with weighed document-term matrix dimensions %dx%d\n" \
                   "\tand with %d extracted topics>" % tpls
        else:
            return "LatentSemanticAnalyzer object with no document-term matrix."
