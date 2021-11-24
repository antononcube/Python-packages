from SSparseMatrix import SSparseMatrix
from SSparseMatrix import is_s_sparse_matrix
import scipy
import numpy
import math


# ===========================================================
# Utility functions
# ===========================================================
def _normalize_sparse_by_max(smat, abs_max=False):
    nonzero_rows = smat.nonzero()[0]
    for idx in numpy.unique(nonzero_rows):
        data_idx = numpy.where(nonzero_rows == idx)[0]
        if abs_max:
            myMax = numpy.max(numpy.abs(smat.data[data_idx]))
        else:
            myMax = numpy.max(smat.data[data_idx])
        if myMax != 0:
            smat.data[data_idx] = 1. / myMax * smat.data[data_idx]
    return smat


# ===========================================================
# Global weights
# ===========================================================
def global_term_function_weights(doc_term_matrix, func="None"):
    """Find the global term function weights for a specified SSparseMatrix object and function name."""
    if not isinstance(doc_term_matrix, SSparseMatrix):
        raise TypeError("The argument docTermMat is expected to be a SSparseMatrix object.")
        return None

    if not isinstance(func, str):
        raise TypeError("The argument func is expected to be a string.")
        return None

    mat = doc_term_matrix.copy()

    if func.lower() == "IDF".lower():

        mat.unitize()
        globalWeights = mat.column_sums()
        globalWeights = [math.log(mat.rows_count() / (1.0 + x), 2) for x in globalWeights]

        return globalWeights

    elif func.lower() == "GFIDF".lower():

        freqSums = mat.column_sums()
        mat.unitize()
        globalWeights = mat.column_sums()
        globalWeights = [1 if x == 0 else x for x in globalWeights]
        globalWeights = [x[0] / x[1] for x in zip(freqSums, globalWeights)]

        return globalWeights

    elif func.lower() == "Normal".lower():

        globalWeights = [math.sqrt(x) for x in mat.multiply(mat).column_sums()]
        globalWeights = [1 if x == 0 else x for x in globalWeights]
        globalWeights = [1 / x for x in globalWeights]

        return globalWeights

    elif func.lower() == "Binary".lower() or func.lower() == "None".lower():

        globalWeights = [1 for x in range(mat.columns_count())]

        return globalWeights

    elif func.lower() == "ColumnStochastic".lower() or func.lower() == "Sum".lower():

        mat.unitize()
        globalWeights = mat.column_sums()
        globalWeights = [1 if x == 0 else x for x in globalWeights]
        globalWeights = [1 / x for x in globalWeights]

        return globalWeights

    elif func.lower() == "Entropy".lower():

        raise TypeError("Global weight function Entropy is not implemented.")
        return None

    else:
        raise TypeError("Unknown global weight function specification for the argument func.")
        return None

    # Should not be reached
    return globalWeights


def apply_term_weight_functions(doc_term_matrix,
                                global_weight_func="None",
                                local_weight_func="None",
                                normalizer_func="None"):
    """Apply specified LSI functions to the entries of SSparseMatrix object."""
    if not isinstance(doc_term_matrix, SSparseMatrix):
        raise TypeError("The argument docTermMat is expected to be a SSparseMatrix object.")
        return None

    if not isinstance(local_weight_func, str):
        raise TypeError("The argument local_weight_func is expected to be a string.")
        return None

    if not isinstance(normalizer_func, str):
        raise TypeError("The argument normalizer_func is expected to be a string.")
        return None

    # Global weights set-up.
    if isinstance(global_weight_func, str):
        globalWeights = global_term_function_weights(doc_term_matrix=doc_term_matrix, func=global_weight_func)
    elif isinstance(global_weight_func, list) and len(global_weight_func) == doc_term_matrix.columns_count():
        globalWeights = global_weight_func
    else:
        raise TypeError("""The argument global_weight_func is expected to be a string 
        or a numeric vector with length that equals docTermMat.columns_count()""")
        return None

    # Make local copy
    mat = doc_term_matrix.copy()

    # Local weights application.
    if local_weight_func.lower() == "Log".lower() or local_weight_func.lower() == "Logarithmic".lower():

        smat = mat.sparse_matrix()
        smat.data = [x + 1 for x in smat.data]
        smat.data = numpy.log(smat.data)
        mat.set_sparse_matrix(smat)

    elif not (local_weight_func.lower() == "TermFrequency".lower() or local_weight_func.lower() == "None".lower()):
        # There is nothing to be done if local_weight_func is "None" or "TermFrequency".
        raise TypeError("Unknown local weight function specification for the argument local_weight_func.")
        return None

    # Multiply with the global weights
    diagMat = scipy.sparse.diags(diagonals=[globalWeights], offsets=[0])
    mat = mat.dot(diagMat)
    mat.set_column_names(doc_term_matrix.column_names())

    # Normalizing.
    if normalizer_func.lower() == "Cosine".lower():

        svec = numpy.sqrt(mat.multiply(mat).row_sums())
        svec = [1 if x == 0 else 1 / x for x in svec]
        diagMat = scipy.sparse.diags(diagonals=[svec], offsets=[0])
        diagMat = SSparseMatrix(diagMat, row_names=mat.row_names(), column_names=mat.row_names())
        mat = diagMat.dot(mat)

    elif normalizer_func.lower() == "Sum".lower() or normalizer_func.lower() == "RowStochastic".lower():

        svec = mat.row_sums()
        svec = [1 if x == 0 else 1 / x for x in svec]
        diagMat = scipy.sparse.diags(diagonals=[svec], offsets=[0])
        diagMat = SSparseMatrix(diagMat, row_names=mat.row_names(), column_names=mat.row_names())
        mat = diagMat.dot(mat)

    elif normalizer_func.lower() == "Max".lower() or normalizer_func.lower() == "Maximum".lower():

        smat = _normalize_sparse_by_max(mat.sparse_matrix(), abs_max=False)
        mat.set_sparse_matrix(smat)

    elif normalizer_func.lower() == "AbsMax".lower() or normalizer_func.lower() == "AbsMaximum".lower():

        smat = _normalize_sparse_by_max(mat.sparse_matrix(), abs_max=True)
        mat.set_sparse_matrix(smat)

    elif normalizer_func.lower() != "None".lower():
        # There is nothing to be done if normalizer_func is "None".
        raise TypeError("Unknown local weight function specification for the argument normalizer_func.")
        return None

    # Result
    return mat
