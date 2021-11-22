import SparseMatrixRecommender
from SparseMatrixRecommender.CrossTabulate import cross_tabulate
import pandas
import snowballstemmer
import re


# ======================================================================
# Utilities
# ======================================================================
def _is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def _is_str_dict(obj):
    return isinstance(obj, dict) and _is_str_list(list(obj.keys())) and _is_str_list(list(obj.values()))


# ======================================================================
# To bags of words
# ======================================================================
def to_bag_of_words(docs,
                    stop_words: list = [],
                    stemming_rules=None,
                    words_pattern="[\w']+|[.,!?;]",
                    min_length: int = 2):
    """To bag(s) of words.

    :type docs: str|list
    :param docs: A list of documents.

    :type stop_words: list
    :param stop_words: A list of stop words.

    :param stemming_rules: bool|dict
    :param stemming_rules: A dictionary of stemming rules or a Boolean. I

    :type words_pattern: str|None
    :param words_pattern: A regex pattern to extract the words with.

    :type min_length: int
    :param min_length: Minimum length of the words in the bags.

    :rtype docTerms: list
    :return docTerms: A list of bags of words.
    """
    if isinstance(docs, str):
        return to_bag_of_words([docs, ], words_pattern=words_pattern, min_length=min_length)

    mwords_pattern = words_pattern
    if words_pattern is None:
        mwords_pattern = "[\w']+|[.,!?;]"

    print(_is_str_list(docs))
    if _is_str_list(docs):
        docTerms = [re.findall(mwords_pattern, x, re.UNICODE) for x in docs]
    else:
        raise TypeError("The first argument, 'doc', is expected to be a list of strings.")

    if min_length > 0:
        docTerms = [[w for w in doc if len(w) >= min_length] for doc in docTerms]

    if _is_str_list(stop_words):
        stop_words_set = set(stop_words)
        docTerms = [[w for w in doc if w not in stop_words_set] for doc in docTerms]

    # Automatic stemming
    if isinstance(stemming_rules, bool) and stemming_rules:
        stObj = snowballstemmer.stemmer("english")
        docTerms = [stObj.stemWords(doc) for doc in docTerms]

    return docTerms


# ======================================================================
# Document term matrix
# ======================================================================
def document_term_matrix(docs):
    """Document term matrix.

    :type docs: dict|list
    :param docs: Documents

    :rtype smat: SSparseMatrix
    :return smat: Contingency matrix of document IDs vs terms.
    """
    if _is_str_list(docs):
        ids = ["id." + str(i) for i in range(len(docs))]
        return document_term_matrix(dict(zip(ids, docs)))
    elif not _is_str_dict(docs):
        raise TypeError("The first argument is expected to be list of strings or a dictionary of strings.")

    docTerms = to_bag_of_words(list(docs.values()))
    ids = list(docs.keys())
    dfDocTerms = [pandas.DataFrame({"ID": ids[i], "Word": docTerms[i]}) for i in range(len(docTerms))]
    dfDocTerms = pandas.concat(dfDocTerms)
    res = cross_tabulate(dfDocTerms, "ID", "Word")
    return res
