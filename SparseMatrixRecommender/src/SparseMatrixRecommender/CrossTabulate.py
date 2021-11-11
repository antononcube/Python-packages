import pandas
import scipy
from SSparseMatrix.src.SSparseMatrix import SSparseMatrix


def cross_tabulate(data, index, columns, values=None, aggfunc=None):
    if isinstance(columns, str):
        if isinstance(data, pandas.core.frame.DataFrame) and isinstance(values, str):
            return _cross_tabulate_3(var1=data[index], var2=data[columns], values=data[values])
        elif isinstance(data, pandas.core.frame.DataFrame):
            return _cross_tabulate_2(var1=data[index], var2=data[columns])
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
