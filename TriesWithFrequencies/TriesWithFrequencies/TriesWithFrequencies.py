# This Python implementation follows mostly the Mathematica implementation:
#    https://github.com/antononcube/MathematicaForPrediction/blob/master/TriesWithFrequencies.m
# And to a lesser extent the Raku implementations:
#    https://github.com/antononcube/Raku-ML-TriesWithFrequencies ,
#    https://github.com/antononcube/Raku-ML-HashTriesWithFrequencies


import math
import warnings

# Constant naming directions here:
# https://peps.python.org/pep-0008/#constants
TRIE_ROOT = "TRIEROOT"
TRIE_VALUE = "TRIEVALUE"


# ===========================================================
# Predicates
# ===========================================================

def _is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def _is_list_of_str_lists(obj):
    return isinstance(obj, list) and all([_is_str_list(x) for x in obj])


# ===========================================================
# Utilities
# ===========================================================

def _reverse_sort_dict(x):
    return dict([(k, v) for k, v in sorted(x.items(), key=lambda item: -item[1])])


def _merge_with(x, y, merge_func):
    result = dict(x)
    for key in y:
        if key in result:
            result[key] = merge_func(result[key], y[key])
        else:
            result[key] = y[key]
    return result


def _deep_get(d, keys, partial=False):
    if not isinstance(d, dict):
        raise TypeError("The first argument is expected to be a dict.")
    if not _is_str_list(keys):
        raise TypeError("The second argument is expected to be a list of strings.")

    res = d
    if partial:
        for k in keys:
            r = res.get(k, None)
            if r is None:
                return res
            else:
                res = r

    else:
        for k in keys:
            res = res.get(k, {})

    return res


# ===========================================================
# Trie Predicates
# ===========================================================

def is_trie_body(tr):
    """
    Trie body check
    ---------------
    :param tr: An object to test.
    :return: bool
    """
    return isinstance(tr, dict) and (TRIE_VALUE in tr)


def is_trie(tr):
    """
    Trie check
    ----------
    :type tr: any
    :param tr: An object to test.
    :return: bool
    """
    return isinstance(tr, dict) and len(tr) == 1 and is_trie_body(list(tr.items())[0][1])


def is_trie_with_trie_root(tr):
    """
    Trie with a trie root check
    ---------------------------
    :param tr: An object to test.
    :return: bool
    """
    return is_trie(tr) and list(tr.keys())[0] == TRIE_ROOT


def is_trie_leaf(tr):
    """
    Trie leaf check
    ---------------
    :param tr: An object to test.
    :return: bool
    """
    warnings.warn("Not implemented.")
    return False


# ===========================================================
# Make
# ===========================================================

def trie_make(chars, value=1.0, bottom_value=1.0, verify_input=True):
    """
    Trie making
    -----------
    :param chars: A list of "characters" to make the trie with.
    :param value: Value
    :param bottom_value: Bottom value.
    :param verify_input: Should the input be verified or not?
    :return: Trie
    """
    if verify_input and not _is_str_list(chars):
        raise ValueError("The first argument is expected to be a list of strings.")

    if len(chars) == 0:
        return {}

    init = {chars[len(chars) - 1]: {TRIE_VALUE: bottom_value}}

    res = init
    for i in range(len(chars) - 2, -1, -1):
        res = {chars[i]: res | {TRIE_VALUE: value}}
    return res


# ===========================================================
# Merge
# ===========================================================

def trie_merge(first, second):
    """
    Trie merge
    ----------
    :type first: dict
    :param first: The first trie merge.

    :type second: dict
    :param second: The second trie to merge

    :return: Trie
    """
    result = first.copy()

    for k in list(second.keys()):

        if k not in first:
            result[k] = second[k].copy()
        else:
            if isinstance(first[k], dict):
                result[k] = trie_merge(first[k], second[k])
            elif isinstance(first[k], float | int):
                result[k] = first[k] + second[k]
            else:
                # This should not be happening.
                warnings.warn("Overwriting for key " + k)

    return result


# ===========================================================
# Insert
# ===========================================================

def trie_insert(tr, word, value=1.0, bottom_value=1.0, verify_input=True):
    """
    Trie create
    -----------
    :type tr: dict
    :param tr: A trie to insert into.

    :type word: list
    :param word: A list of strings.

    :type value: float
    :param value: Value.

    :type bottom_value: float
    :param bottom_value: Bottom value.

    :type verify_input: bool
    :param verify_input: Should the input be verified or not?

    :return: Trie
    """
    if verify_input and not _is_str_list(word):
        raise ValueError("The second argument is expected to be a list of strings.")

    res0 = trie_make(word, value=value, bottom_value=bottom_value, verify_input=False)

    res = {TRIE_ROOT: res0 | {TRIE_VALUE: list(res0.items())[0][1][TRIE_VALUE]}}

    return trie_merge(tr, res)


# ===========================================================
# Create
# ===========================================================

def trie_create1(words: list, verify_input: bool = True):
    """
    Trie create sequentially
    -----------
    :type words: list
    :param words: A list of strings

    :type verify_input: bool
    :param verify_input: Should the input be verified or not?

    :return: Trie
    """
    if verify_input and not _is_list_of_str_lists(words):
        raise ValueError("The first argument is expected to be a list of lists of strings.")

    if len(words) == 0:
        return {}

    res0 = trie_make(words[0], verify_input=verify_input)

    res = {TRIE_ROOT: res0 | {TRIE_VALUE: list(res0.items())[0][1][TRIE_VALUE]}}

    for w in words[1:]:
        res = trie_insert(res, w, verify_input=verify_input)

    return res


def trie_create(words: list, bisection_threshold: int = 15, verify_input: bool = True):
    """
    Trie create
    -----------
    :type words: list
    :param words: A list of strings

    :type bisection_threshold: int
    :param bisection_threshold: Threshold above which recursive creation is used.

    :type verify_input: bool
    :param verify_input: Should the input be verified or not?

    :return: Trie
    """
    if verify_input and not _is_list_of_str_lists(words):
        raise ValueError("The first argument is expected to be a list of lists of strings.")

    if len(words) <= bisection_threshold:
        return trie_create1(words, verify_input=False)

    return trie_merge(
        trie_create(words[0:math.ceil(len(words) / 2)], bisection_threshold=bisection_threshold, verify_input=False),
        trie_create(words[math.ceil(len(words) / 2):], bisection_threshold=bisection_threshold, verify_input=False))


# ===========================================================
# Create by split
# ===========================================================

def trie_create_by_split(words: list, bisection_threshold: int = 15):
    """
    Trie create by split
    --------------------
    :type words: list
    :param words: A list of strings

    :type bisection_threshold: int
    :param bisection_threshold: Threshold above which recursive creation is used.

    :return: Trie
    """
    if not _is_str_list(words):
        raise ValueError("The first argument is expected to be a list of strings.")

    return trie_create([list(x) for x in words], bisection_threshold=bisection_threshold)


# ===========================================================
# Retrieve sub-trie
# ===========================================================

def trie_sub_trie(tr: dict, word: list):
    """
    Trie sub-trie
    -------------
    :type tr: dict
    :param tr: A trie.
    :param word: Word (a list of strings) to find search with.
    :return: A trie
    """
    if not (is_trie(tr) or is_trie_body(tr)):
        raise TypeError("The first argument is expected to be a trie or trie body.")

    if not _is_str_list(word):
        raise TypeError("The second argument is expected to be a list of strings.")

    wordLocal = word
    if is_trie_with_trie_root(tr) and word[0] != TRIE_ROOT:
        wordLocal.insert(0, TRIE_ROOT)

    res = _trie_sub_trie_path(tr, wordLocal)

    if len(res["path"]) == 0:
        return {}

    return {res["path"][-1]: res["trie"]}


def _trie_sub_trie_path(tr: dict, word: list):
    if not (is_trie(tr) or is_trie_body(tr)):
        raise TypeError("The first argument is expected to be a trie or trie body.")

    if not _is_str_list(word):
        raise TypeError("The second argument is expected to be a list of strings.")

    path = []
    trLocal = tr
    for k in word:
        if k in trLocal:
            path.append(k)
            trLocal = trLocal.get(k)
        else:
            break

    return {"trie": trLocal, "path": path}


def _trie_sub_trie_path_rec(tr: dict, word: list):
    if not (is_trie(tr) or is_trie_body(tr)):
        raise TypeError("The first argument is expected to be a trie or trie body.")

    if not _is_str_list(word):
        raise TypeError("The second argument is expected to be a list of strings.")

    if len(word) == 0:
        return []

    if word[0] in tr:
        return [word[0], ].append(_trie_sub_trie_path_rec(tr=tr[word[0]]), word=word[1:])

    return []


# ===========================================================
# Shrinking
# ===========================================================

def _take_body_value(tr_body: dict):
    res = [v for (k, v) in tr_body.items() if k != TRIE_VALUE]
    return res[0][TRIE_VALUE]


def _shrink_q(val, ch_val, threshold):
    if threshold < 0 and val >= 1.0 and ch_val >= 1.0:
        return val == ch_val
    elif threshold < 0:
        return ch_val == 1.0
    else:
        return ch_val >= threshold

    return False


def _trie_shrink_rec(tr,
                     sep: str,
                     threshold: float,
                     internal_only: bool,
                     level: int):
    if is_trie(tr):

        return _trie_shrink_rec(list(tr.items())[0],
                                sep=sep,
                                threshold=threshold,
                                internal_only=internal_only,
                                level=level + 1)

    elif isinstance(tr, tuple) and len(tr) == 2 and is_trie_body(tr[1]):
        key = tr[0]
        vals = tr[1]
        valKeys = [k for (k, v) in vals.items() if k != TRIE_VALUE]

        if len(vals) == 1:
            return dict([tr])
        elif key != TRIE_ROOT and len(vals) == 2 and _shrink_q(vals[TRIE_VALUE], _take_body_value(vals), threshold):

            return _trie_shrink_rec((key + sep + valKeys[0], vals[valKeys[0]]),
                                    sep=sep,
                                    threshold=threshold,
                                    internal_only=internal_only,
                                    level=level + 1)
        else:
            res = {}
            for (k, v) in vals.items():
                if k != TRIE_VALUE:
                    res = res | _trie_shrink_rec((k, v),
                                                 sep=sep,
                                                 threshold=threshold,
                                                 internal_only=internal_only,
                                                 level=level + 1)

            return {key: ({TRIE_VALUE: vals[TRIE_VALUE]} | res)}
    else:
        raise ValueError(
            "Do not how to process the argument at level " + str(level) + " with type = " + str(type(tr)) + " .")

    return None


def trie_shrink(tr: dict,
                sep: str = "",
                threshold: float = -1.0,
                internal_only: bool = False):
    """
    Trie shrinking
    --------------
    Shrinks a trie by finding prefixes.
    :type tr: dict
    :param tr: A trie

    :type sep: str
    :param sep: A separator to be used when strings are joined.

    :type threshold: float
    :param threshold: Above what threshold to do the shrinking. If negative automatic shrinking test is applied.

    :type internal_only: bool
    :param internal_only:

    :return: Trie
    """

    if not is_trie(tr):
        raise TypeError("The first argument is expected to be a trie or trie body.")

    res = _trie_shrink_rec(tr, sep=sep, threshold=threshold, internal_only=internal_only, level=0)

    return res


# ===========================================================
# Node probabilities
# ===========================================================

def trie_node_probabilities(tr: dict):
    """
    Trie node probabilities
    -----------------------
    :type tr: dict
    :param tr: A trie the frequencies of which are converted into probabilities.
    :return: Trie
    """
    if not is_trie(tr):
        raise ValueError("The first argument is expected to be a trie.")

    return {list(tr.keys())[0]: _trie_node_probabilities_rec(list(tr.values())[0]) | {TRIE_VALUE: 1.0}}


# -----------------------------------------------------------
def _trie_node_probabilities_rec(trb):
    if not is_trie_body(trb):
        raise ValueError("The first argument is expected to be a trie body.")

    if len(trb) == 1:
        return trb
    else:
        if trb[TRIE_VALUE] == 0:
            tSum = _trie_value_total(trb)
        else:
            tSum = trb[TRIE_VALUE]

        res = {k: _trie_node_probabilities_rec(v) for (k, v) in trb.items() if k != TRIE_VALUE}

        res = {k: (v | {TRIE_VALUE: v[TRIE_VALUE] / tSum}) for (k, v) in res.items() if k != TRIE_VALUE}

        return res | {TRIE_VALUE: trb[TRIE_VALUE]}


# -----------------------------------------------------------
def _trie_value_total(trb):
    if not is_trie_body(trb):
        raise ValueError("The first argument is expected to be a trie body.")

    return sum([v[TRIE_VALUE] for (k, v) in trb.items() if k != TRIE_VALUE])


# ===========================================================
# Leaf probabilities
# ===========================================================
def trie_leaf_probabilities(tr: dict):
    """
    Trie leaf probabilities
    -----------------------
    :type tr: dict
    :param tr: Trie
    :return: dict
    """
    if not is_trie(tr):
        raise ValueError("The first argument is expected to be a trie.")

    t = list(tr.items())[0]
    res = _trie_leaf_probabilities_rec(t[0], t[1])

    if len(res) == 1:
        return dict(res)
    else:
        res2 = {}
        for p in res:
            res2 = _merge_with(res2, dict([p]), lambda x, y: x + y)
        return res2


def _trie_leaf_probabilities_rec(k, trb):
    if not is_trie_body(trb):
        raise ValueError("The first argument is expected to be a trie body.")

    if len(trb) == 1:
        return [(k, trb[TRIE_VALUE])]
    else:
        tSum = _trie_value_total(trb)

        res = [_trie_leaf_probabilities_rec(k, v) for (k, v) in trb.items() if k != TRIE_VALUE]

        res2 = []
        for e in res:
            res2 = res2 + e

        if tSum < 1:
            res2 = res2 + [(k, 1 - tSum)]

        res = [(p[0], p[1] * trb[TRIE_VALUE]) for p in res2]

        return res


# ===========================================================
# Classify
# ===========================================================

def trie_classify(tr, record, prop="Decision", default=None, verify_key_existence: bool = True):
    """
    Trie classify
    -------------
    :type tr: dict
    :param tr: A trie to be used as classifier.

    :param record: A record or a list of records to classify.

    :param prop: Property to be returned.

    :param default: Default value.

    :type verify_key_existence: bool
    :param verify_key_existence: Should the record-as-key existence be verified or not?

    :return: A decision label or a dictionary with labels to probabilities.
    """
    if not is_trie(tr):
        raise ValueError("The first argument is expected to be a trie.")

    propLocal = prop
    if prop is None:
        prop = "Probabilities"

    if _is_list_of_str_lists(record):
        return [trie_classify(tr, x,
                              prop=propLocal,
                              default=default,
                              verify_key_existence=verify_key_existence) for x in record]

    # Probabilities
    res = trie_sub_trie(tr, record)

    if len(res) == 0:
        res = {default: 0}
    else:
        res = _reverse_sort_dict(trie_leaf_probabilities(res))

    if prop.lower() == "decision":
        return list(res.keys())[0]
    else:
        return res
    return res


# ===========================================================
# Node counts
# ===========================================================

def trie_node_counts(tr: dict):
    """
    Trie node counts
    ----------------
    :param tr: A trie to find the node counts for.
    :return: Dictionary with counts statistics.
    """
    if not is_trie(tr):
        raise ValueError("The first argument is expected to be a trie.")

    res = _trie_node_counts_rec(tr, 0)

    return {"total": res["total"], "internal": res["internal"], "leaves": res["total"] - res["internal"]}


def _trie_node_counts_rec(tr, level: int):
    res = {"internal": 0, "total": 0}
    for (k, v) in tr.items():
        if isinstance(v, float | int):
            res["total"] = res["total"] + 1
        elif isinstance(v, dict):
            if len(v) > 1:
                res["internal"] = res["internal"] + 1
            for (k1, v1) in v.items():
                res2 = _trie_node_counts_rec({k1: v1}, level + 1)
                res["internal"] = res["internal"] + res2["internal"]
                res["total"] = res["total"] + res2["total"]
        else:
            raise ValueError("Not a trie node at level", level)

    return res


# ===========================================================
# Tree Form
# ===========================================================

def trie_form(tr: dict):
    """
    Trie form
    ---------
    :type tr: dict
    :param tr: A trie to put in tree form
    :return: Nil
    """
    if len(tr) == 0:
        print("<empty>")
        return
    k = list(tr.keys())[0]
    _visit(k, tr[k], ["", ""])


def _visit(k, body, indent, mid=["├─", "│ "], end=["└─", "  "]):
    children = list(body.keys())
    print(indent[0] + k, "=>", body[TRIE_VALUE])

    if len(children) == 1:
        return

    for i in range(len(children)):
        c = children[i]
        if c != TRIE_VALUE:
            if i < len(children) - 2:
                indent2 = [indent[1] + x for x in mid]
                _visit(c, body[c], indent2)
            else:
                indent2 = [indent[1] + x for x in end]
                _visit(c, body[c], indent2)
    return
