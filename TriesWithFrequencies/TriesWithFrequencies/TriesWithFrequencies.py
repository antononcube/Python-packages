import math
import warnings

trie_root = "TRIEROOT"
trie_value = "TRIEVALUE"


# ===========================================================
# Predicates
# ===========================================================

def _is_str_list(obj):
    return isinstance(obj, list) and all([isinstance(x, str) for x in obj])


def _is_list_of_str_lists(obj):
    return isinstance(obj, list) and all([_is_str_list(x) for x in obj])


# ===========================================================
# Trie Predicates
# ===========================================================

def is_trie_body(tr):
    """
    Trie body check
    ---------------
    :param tr: A trie
    :return: bool
    """
    return isinstance(tr, dict) and trie_value in tr


def is_trie(tr):
    """
    Trie check
    ----------
    :param tr: A trie
    :return: bool
    """
    return isinstance(tr, dict) and len(tr) == 1 and is_trie_body(tr)


def is_trie_with_trie_root(tr):
    """
    Trie with a trie root check
    ---------------------------
    :param tr: A trie
    :return: bool
    """
    return is_trie_body(tr) and list(tr.keys())[0] == trie_root


def is_trie_leaf(tr):
    """
    Trie leaf check
    ---------------
    :param tr: A trie
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
        ValueError("The first argument is expected to be a list of strings.")

    if len(chars) == 0:
        return {}

    init = {chars[len(chars) - 1]: {trie_value: bottom_value}}

    res = init
    for i in range(len(chars) - 2, -1, -1):
        res = {chars[i]: res | {trie_value: value}}
    return res


# ===========================================================
# Merge
# ===========================================================

def trie_merge(first, second):
    """
    Trie merge
    ----------
    :param first: The first trie merge.

    :param second: The second trie to merge

    :return: Trie
    """
    result = first

    for k in list(second.keys()):

        if k not in first:
            result[k] = second[k]
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
        ValueError("The second argument is expected to be a list of strings.")

    res0 = trie_make(word, value=value, bottom_value=bottom_value, verify_input=False)

    res = {trie_root: res0 | {trie_value: list(res0.items())[0][1][trie_value]}}

    return trie_merge(tr, res)


# ===========================================================
# Create
# ===========================================================

def trie_create1(words, verify_input=True):
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
        ValueError("The first argument is expected to be a list of lists of strings.")

    if len(words) == 0:
        return {}

    res0 = trie_make(words[0], verify_input=verify_input)

    res = {trie_root: res0 | {trie_value: list(res0.items())[0][1][trie_value]}}

    for w in words[1:]:
        res = trie_insert(res, w, verify_input=verify_input)

    return res


def trie_create(words, bisection_threshold=15, verify_input=True):
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
        ValueError("The first argument is expected to be a list of lists of strings.")

    if len(words) <= bisection_threshold:
        return trie_create1(words, verify_input=False)

    return trie_merge(
        trie_create(words[0:math.ceil(len(words) / 2)], bisection_threshold=bisection_threshold, verify_input=False),
        trie_create(words[math.ceil(len(words) / 2):], bisection_threshold=bisection_threshold, verify_input=False))


# ===========================================================
# Create by split
# ===========================================================

def trie_create_by_split(words, bisection_threshold=15):
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
        ValueError("The first argument is expected to be a list of strings.")

    return trie_create([list(x) for x in words], bisection_threshold=bisection_threshold)


# ===========================================================
# Node probabilities
# ===========================================================

def trie_node_probabilities():
    pass


# ===========================================================
# Node counts
# ===========================================================

def trie_node_counts(tr):
    """
    Trie node counts
    ----------------
    :param tr: A trie to find the node counts for.
    :return: Dictionary with counts statistics.
    """
    if not is_trie(tr):
        ValueError("The first argument is expected to be a trie.")

    res = _trie_node_counts_rec(tr, 0)

    return {"total": res["total"], "internal": res["internal"], "leaves": res["total"] - res["internal"]}


def _trie_node_counts_rec(tr, level):
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
            ValueError("Not a trie node at level", level)

    return res


# ===========================================================
# Tree Form
# ===========================================================

def trie_form(tr):
    """
    Trie form
    ---------
    :param tr: A trie to put in tree form
    :return: Nil
    """
    if len(tr) == 0:
        print("<empty>")
        return
    k = list(tr.keys())[0]
    _visit(k, tr[k], ["",""])


def _visit(k, body, indent, mid=["├─", "│ "], end=["└─", "  "]):
    children = list(body.keys())
    print(indent[0] + k, "=>", body[trie_value])

    if len(children) == 1:
        return

    for i in range(len(children)):
        c = children[i]
        if c != trie_value:
            if i < len(children) - 2:
                indent2 = [indent[1] + x for x in mid]
                _visit(c, body[c], indent2)
            else:
                indent2 = [indent[1] + x for x in end]
                _visit(c, body[c], indent2)
    return
