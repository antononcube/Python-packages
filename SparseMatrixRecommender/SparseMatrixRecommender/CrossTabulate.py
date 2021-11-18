import numpy
import pandas
import scipy
import bisect
from SSparseMatrix import SSparseMatrix


def cross_tabulate(data, index, columns, values=None, aggfunc=None, str_nan="None", num_nan=0):
    """Cross tabulate to a SSparseMatrix object.

    :type data: pandas.core.frame.DataFrame
    :param data: Data frame to be cross tabulated.

    :type index: str
    :param index: Column name for the rows of the result sparse matrix.

    :type columns: str|list
    :param columns: Column name(s) of the data frame for the columns of the result sparse matrix.

    :type values: str|None
    :param values: Column name of the data frame for the values in the result sparse matrix.

    :param aggfunc: Aggregation function for the values.

    :param str_nan: Value to replace NaNs in the categorical columns.
    :param num_nan: Value to replace NaNs in the numerical columns.
    :return: SSparseMatrix|dict
    """
    if isinstance(columns, str):
        if isinstance(data, pandas.core.frame.DataFrame) and isinstance(values, str):
            return _cross_tabulate_3(var1=data[index], var2=data[columns].fillna(str_nan),
                                     values=numpy.nan_to_num(x=data[values], nan=num_nan))
        elif isinstance(data, pandas.core.frame.DataFrame):
            return _cross_tabulate_2(var1=data[index], var2=data[columns].fillna(str_nan))
        else:
            raise TypeError(
                "The first argument is expected to be a data frame.")
            return None
    elif isinstance(columns, list):
        return dict(zip(columns, [cross_tabulate(data=data, index=index, columns=cn) for cn in columns]))
    else:
        raise TypeError(
            "The third argument, columns, is expected to be a string or a list of strings.")
        return None


def _cross_tabulate_2(var1, var2):
    if len(var1) != len(var2):
        raise IndexError("The lengths of var1 and var2 are expected to be the same.")
        return None
    return _cross_tabulate_3(var1=var1, var2=var2, values=[1 for x in range(len(var1))])


def _cross_tabulate_3(var1, var2, values):
    row_names = sorted(var1.unique())
    var1_cat = pandas.api.types.CategoricalDtype(row_names, ordered=True)

    col_names = sorted(var2.unique())
    var2_cat = pandas.api.types.CategoricalDtype(col_names, ordered=True)

    row_cat = var1.astype(var1_cat)
    row = var1.astype(var1_cat).cat.codes

    col = var2.astype(var2_cat).cat.codes
    sparse_matrix = scipy.sparse.csr_matrix((values, (row, col)),
                                            shape=(var1_cat.categories.size, var2_cat.categories.size))

    smat = SSparseMatrix(sparse_matrix)
    smat.set_row_names([str(x) for x in row_names])
    smat.set_column_names([str(x) for x in col_names])

    return smat


def categorize_to_intervals(vec, breaks=None, probs=None, interval_names=False):
    """Categorize to intervals.

    :type vec: list|numpy.ndarray
    :param vec: A numerical vector to be categorized.
    :param breaks: A numerical vector with breaks to be used. If None then numpy.quantile is used.
    :param probs: Probabilities to find quantiles with.
    :param interval_names: Should the intervals be represented with integers or with character names?
    :return resVec: List of integers or list of strings.
    """
    if not (isinstance(vec, list) or isinstance(numpy.ndarray)):
        raise TypeError("The first argument 'vec' is expected to be a list or numpy.ndarray.")
        return None

    mprobs = probs
    if isinstance(probs, type(None)):
        mprobs = [x * 0.1 for x in range(0, 11)]
    elif isinstance(probs, list) or isinstance(probs, numpy.ndarray):
        mprobs = sorted(list(set(probs)))
    else:
        raise TypeError("The third argument, 'probs', is expected to be a list, numpy.ndarray, or None.")
        return None

    if isinstance(breaks, type(None)):
        mbreaks = numpy.quantile(vec, mprobs)
        mbreaks = sorted(list(set(mbreaks)))
    elif isinstance(breaks, list) or isinstance(breaks, numpy.ndarray):
        mbreaks = sorted(list(set(breaks)))
    else:
        raise TypeError("The second argument, 'breaks', is expected to be a list, numpy.ndarray, or None.")
        return None

    resVec = [bisect.bisect_left(a=mbreaks, x=x) for x in vec]

    if interval_names:
        interval_names = [str(mbreaks[i]) + "≤v<" + str(mbreaks[i + 1]) for i in range(len(mbreaks) - 1)]
        resVec = [interval_names[i] if i < len(interval_names) else interval_names[-1] for i in resVec]

    return resVec


def numerical_column_to_s_sparse_matrix(data: pandas.core.frame.DataFrame, index: str, column: str):
    """Convert a numerical column of data frame into SSparseMatrix (with one column.)

    :param data: A data frame.
    :param index: The index/ID column of the data frame.
    :param column: The numerical column to be converted.
    :return: SSparseMatrix
    """
    data2 = pandas.DataFrame({"Index": data[index], "Variable": column, "Values": data[column]})
    return cross_tabulate(data=data2, index="Index", columns="Variable", values="Values")
