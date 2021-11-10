import copy

import numpy
import scipy
from scipy import sparse
import copy
import math


# ======================================================================
# Utilities
# ======================================================================
def is_sparse_matrix(obj):
    return isinstance(obj, SSparseMatrix) and scipy.sparse.issparse(obj.sparse_matrix())


def make_from_sparse_matrix(smat):
    obj = SSparseMatrix()
    return obj.set_sparse_matrix(smat)


def is_int_like(x):
    return scipy.sparse.sputils.isintlike(x)


def is_str_like(x):
    """Is x appropriate as a key into a SSparseMatrix object? Returns True
    if it can be cast safely to a key.
    """
    if scipy.sparse.sputils.issequence(x):
        return False
    else:
        try:
            if str(x) == x:
                return True
            else:
                return False
        except TypeError:
            return False


# ======================================================================
# Class definition
# ======================================================================
class SSparseMatrix:

    def __init__(self, *args):
        self.id = "src"
        self.sparseMatrix = None
        self.rowNames = None
        self.colNames = None
        self.dimNames = None
        if len(args) == 1:
            self.set_sparse_matrix(args[0])
        elif len(args) > 1:
            raise TypeError("No arguments or a matrix argument is expected.")

    # ------------------------------------------------------------------
    #  Getters
    # ------------------------------------------------------------------
    def sparse_matrix(self) -> scipy.sparse.csc.csc_matrix:
        return self.sparseMatrix

    def row_names_dict(self):
        return self.rowNames

    def row_names(self):
        if isinstance(self.rowNames, dict):
            return list(self.rowNames.keys())
        else:
            return self.rowNames

    def column_names_dict(self):
        return self.colNames

    def column_names(self):
        if isinstance(self.colNames, dict):
            return list(self.colNames.keys())
        else:
            return self.colNames

    def dimension_names(self):
        return list(self.dimNames.keys())

    def rows_count(self):
        return self.sparse_matrix().shape[0]

    def nrows(self):
        return self.sparse_matrix().shape[0]

    def columns_count(self):
        return self.sparse_matrix().shape[1]

    def ncols(self):
        return self.sparse_matrix().shape[1]

    def shape(self):
        return self.sparse_matrix().shape

    def copy(self):
        return copy.deepcopy(self)

    # ------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------
    def set_sparse_matrix(self, arg):
        if scipy.sparse.issparse(arg):
            self.sparseMatrix = arg.tocsr()
            return self
        elif isinstance(arg, list):
            smat2 = scipy.sparse.csr_matrix(arg)
            if scipy.sparse.issparse(smat2):
                self.sparseMatrix = smat2
        else:
            raise TypeError("The first argument is expected to a matrix is or can be coerced to csr sparse matrix.")
            return None
        return self

    def set_row_names(self, *args):
        if len(args) == 0:
            self.set_row_names([str(x) for x in range(0, self.rows_count())])
        elif isinstance(args[0], dict) and len(args[0]) == self.rows_count():
            self.rowNames = args[0]
        elif isinstance(args[0], list) and len(args[0]) == self.rows_count():
            self.rowNames = dict(zip(args[0], range(0, len(args[0]))))
        else:
            raise TypeError(
                "The first argument is expected to be a string-to-index dictionary or a list of strings of length %s." %
                self.rows_count())
            return None
        return self

    def set_column_names(self, *args):
        if len(args) == 0:
            return self.set_column_names([str(x) for x in range(0, self.columns_count())])
        elif isinstance(args[0], dict) and len(args[0]) == self.columns_count():
            self.colNames = args[0]
        elif isinstance(args[0], list) and len(args[0]) == self.columns_count():
            self.colNames = dict(zip(args[0], range(0, len(args[0]))))
        else:
            raise TypeError(
                "The first argument is expected to be a string-to-index dictionary or a list of strings of length %s." %
                self.columns_count())
            return None
        return self

    # ------------------------------------------------------------------
    # Access
    # ------------------------------------------------------------------
    def is_key_like(self, x):
        """Is x appropriate as a key into a SSparseMatrix object? Returns True
        if it can be cast safely to a key.
        """
        return is_str_like(x) and (x in self.row_names() or x in self.column_names())

    def is_row_key_like(self, x):
        """Is x appropriate as a row key into a SSparseMatrix object? Returns True
        if it can be cast safely to a key.
        """
        return is_str_like(x) and x in self.row_names()

    def is_column_key_like(self, x):
        """Is x appropriate as a column key into a SSparseMatrix object? Returns True
        if it can be cast safely to a column key.
        """
        return is_str_like(x) and x in self.column_names()

    # ------------------------------------------------------------------
    # Access
    # ------------------------------------------------------------------
    def _get_single_element(self, row, col):
        if is_int_like(row) and is_int_like(col):
            return self.sparse_matrix()[row, col]
        elif row in self.row_names() and col in self.column_names():
            return self.sparse_matrix()[self.row_names_dict()[row], self.column_names_dict()[col]]

    def _get_submatrix(self, row_slice_arg, col_slice_arg):
        row_slice = row_slice_arg
        col_slice = col_slice_arg

        if isinstance(row_slice, list) and is_str_like(row_slice[0]):
            row_slice = [self.row_names_dict()[x] for x in row_slice]

        if isinstance(col_slice, list) and is_str_like(col_slice[0]):
            col_slice = [self.column_names_dict()[x] for x in col_slice]

        res = SSparseMatrix(self.sparse_matrix()[row_slice, col_slice])

        if isinstance(row_slice, list):
            res.set_row_names([self.row_names()[x] for x in row_slice])
        else:
            res.set_row_names(self.row_names()[row_slice])

        if isinstance(col_slice, list):
            res.set_column_names([self.column_names()[x] for x in col_slice])
        else:
            res.set_column_names(self.column_names()[col_slice])
        return res

    def __getitem__(self, key):
        if isinstance(key, tuple):
            row = key[0]
            col = key[1]

            if is_int_like(row) and is_int_like(col) or \
                    is_str_like(row) and is_str_like(col):
                return self._get_single_element(row, col)
            elif isinstance(row, slice) or isinstance(col, slice) or \
                    isinstance(row, list) or isinstance(col, list):
                return self._get_submatrix(row, col)

        elif is_int_like(key):
            return self[key, :]
        else:
            raise IndexError("invalid index")

    # ------------------------------------------------------------------
    # Slicing
    # ------------------------------------------------------------------

    # def _get_slice(self, i, start, stop, stride, shape):

    # ------------------------------------------------------------------
    # Predicates
    # ------------------------------------------------------------------
    def eq(self, other):
        if is_sparse_matrix(other):

            res = self.sparse_matrix() != other.sparse_matrix()

            if isinstance(res, bool) and not res:
                return False
            elif not isinstance(res, bool):
                res = res.nnz == 0

            return res and \
                   self.row_names() == other.row_names() and \
                   self.column_names() == other.column_names()
        else:
            return False

    # ------------------------------------------------------------------
    # Transpose
    # ------------------------------------------------------------------
    def transpose(self, inplace=False):
        obj = self if inplace else self.copy()
        obj.sparseMatrix = obj.sparse_matrix().transpose()
        t = obj.colNames
        obj.colNames = obj.rowNames
        obj.rowNames = t
        return obj

    # ------------------------------------------------------------------
    # Add
    # ------------------------------------------------------------------
    def add(self, other, inplace=False):
        obj = self if inplace else self.copy()
        if isinstance(other, SSparseMatrix) and \
                obj.row_names() == other.row_names() and \
                obj.column_names() == other.column_names():
            obj.sparseMatrix = obj.sparse_matrix() + other.sparse_matrix()
        elif scipy.sparse.issparse(other):
            obj.sparseMatrix = obj.sparse_matrix() + other
        else:
            raise TypeError("The first argument is expected to be SSparseMatrix object or sparse.csr_matrix object.")
            return None
        return obj

    # ------------------------------------------------------------------
    # Multiply
    # ------------------------------------------------------------------
    def multiply(self, other, inplace=False):
        obj = self if inplace else self.copy()
        if isinstance(other, SSparseMatrix) and \
                obj.row_names() == other.row_names() and \
                obj.column_names() == other.column_names():
            obj.sparseMatrix = obj.sparse_matrix().multiply(other.sparse_matrix())
        elif scipy.sparse.issparse(other):
            obj.sparseMatrix = obj.sparse_matrix().multiply(other)
        else:
            raise TypeError("The first argument is expected to be SSparseMatrix object or sparse.csr_matrix object.")
            return None
        return obj

    # ------------------------------------------------------------------
    # Dot
    # ------------------------------------------------------------------
    def dot(self, other, inplace=False):
        # I am not sure should we check that : self.column_names() == other.row_names()
        # It might be too restrictive.
        obj = self if inplace else self.copy()
        if is_sparse_matrix(other):
            obj.sparseMatrix = obj.sparse_matrix().dot(other.sparse_matrix())
            obj.sparseMatrix.eliminate_zeros()
            # We keep the row names i.e. self.rowNames = self.row_names_dict()
            obj.colNames = other.column_names_dict()
        elif scipy.sparse.issparse(other):
            obj.sparseMatrix = obj.sparse_matrix().dot(other)
            obj.sparseMatrix.eliminate_zeros()
            obj.set_column_names()
        elif isinstance(other, list) or isinstance(other, numpy.ndarray):
            vec = obj.sparse_matrix().dot(other)
            rowInds = [x for x in range(obj.rows_count())]
            colInds = [0 for x in range(obj.rows_count())]
            res = scipy.sparse.coo_matrix((vec, (rowInds, colInds)), shape=(obj.rows_count(), 1))
            res.eliminate_zeros()
            obj.set_sparse_matrix(res)
            obj.set_column_names()
        else:
            raise TypeError("The first argument is expected to be SSparseMatrix object or sparse.csr_matrix object.")
            return None
        return obj

    # ------------------------------------------------------------------
    # Summation
    # ------------------------------------------------------------------
    def row_sums(self):
        return self.sparse_matrix().sum(axis=1).flatten().tolist()[0]

    def row_sums_dict(self):
        return dict(zip(self.row_names(), self.row_sums()))

    def column_sums(self):
        return self.sparse_matrix().sum(axis=0).flatten().tolist()[0]

    def column_sums_dict(self):
        return dict(zip(self.column_names(), self.column_sums()))

    # ------------------------------------------------------------------
    # Impose row names
    # ------------------------------------------------------------------
    def impose_row_names(self, names):
        obj = self.copy()

        if not isinstance(names, list):
            raise TypeError("The first argument is expected to be a list of strings.")
            return None

        missingRows = list(set(names) - set(obj.row_names()))
        nMissingRows = len(missingRows)

        if nMissingRows > 0:
            # Rows are missing in the matrix
            complMat = scipy.sparse.coo_matrix((numpy.array([0]), (numpy.array([0]), numpy.array([0]))),
                                               shape=(nMissingRows, obj.columns_count()))

            complMat = SSparseMatrix(complMat)
            complMat.set_row_names(missingRows)
            complMat.set_column_names(obj.column_names())

            obj = obj.row_bind(complMat)

        return obj[names, :]

    # ------------------------------------------------------------------
    # Impose column names
    # ------------------------------------------------------------------
    def impose_column_names(self, names):
        if isinstance(names, list):
            return self.transpose().impose_row_names(names).transpose(inplace=True)
        else:
            raise TypeError("The first argument is expected to be a list of strings.")
            return None

    # ------------------------------------------------------------------
    # Row binding
    # ------------------------------------------------------------------
    def row_bind(self, other):
        if is_sparse_matrix(other):

            if not (sorted(self.column_names()) == sorted(other.column_names())):
                raise TypeError("The column names of the two SSparseMatrix objects are expected to be the same.")
                return None

            if self.column_names() == other.column_names():
                res = SSparseMatrix(scipy.sparse.vstack([self.sparse_matrix(), other.sparse_matrix()]))
            else:
                mat = scipy.sparse.vstack([self.sparse_matrix(), other[:, self.column_names()].sparse_matrix()])
                res = SSparseMatrix(mat)

            # Set the column names
            res.set_column_names(self.column_names())

            # Special handling of duplication of row names in the result.
            rn_dict = self.row_names_dict() | other.row_names_dict()
            if len(rn_dict) == (self.rows_count() + other.rows_count()):
                res.set_row_names(self.row_names() + other.row_names())
            else:
                res.set_row_names([x + ".1" for x in self.row_names()] + [x + ".2" for x in other.row_names()])

            return res

        else:
            raise TypeError("The first argument is expected to be a SSparseMatrix object.")
            return None

    # ------------------------------------------------------------------
    # Column binding
    # ------------------------------------------------------------------
    # Although there is an "easy" implementation using transposed matrices
    # it is considered potentially too slow.
    def column_bind(self, other):
        if is_sparse_matrix(other):

            if not (sorted(self.row_names()) == sorted(other.row_names())):
                raise TypeError("The row names of the two SSparseMatrix objects are expected to be the same.")
                return None

            if self.row_names() == other.row_names():
                res = SSparseMatrix(scipy.sparse.hstack([self.sparse_matrix(), other.sparse_matrix()]))
            else:
                mat = scipy.sparse.hstack([self.sparse_matrix(), other[self.row_names(),:].sparse_matrix()])
                res = SSparseMatrix(mat)

            # Set the row names
            res.set_row_names(self.row_names())

            # Special handling of duplication of row names in the result.
            cn_dict = self.column_names_dict() | other.column_names_dict()
            if len(cn_dict) == (self.columns_count() + other.columns_count()):
                res.set_column_names(self.column_names() + other.column_names())
            else:
                res.set_column_names([x + ".1" for x in self.column_names()] + [x + ".2" for x in other.column_names()])

            return res

        else:
            raise TypeError("The first argument is expected to be a SSparseMatrix object.")
            return None

    # ------------------------------------------------------------------
    # Print outs
    # ------------------------------------------------------------------
    def print_matrix(self, boundary=True, ndigits=-1):
        table_data = numpy.asarray(self.sparse_matrix().todense())

        invRowNames = {v: k for k, v in self.row_names_dict().items()}
        invColumnNames = {v: k for k, v in self.column_names_dict().items()}

        col_names = [invColumnNames[x] for x in sorted(invColumnNames.keys())]
        row_names = [invRowNames[x] for x in sorted(invRowNames.keys())]

        if not isinstance(ndigits, int):
            raise TypeError("The argument ndigits is expected to be an integer.")
            return None

        if ndigits < 1:
            # Not good enough for automatic determination
            # nds = math.ceil(math.log(self.sparse_matrix().max(), 10)) + 1
            nds = 8
        else:
            nds = ndigits

        fColSpec = "{: >" + str(max([len(x) for x in self.row_names()])) + "}"
        fSpec = "{: >" + str(nds) + "}"
        fStr = fColSpec + " |" + self.columns_count() * fSpec

        if boundary:
            print(len(fStr.format("", *col_names)) * "=")

        print(fStr.format("", *col_names))
        print(len(fStr.format("", *col_names)) * "-")

        for i in range(self.rows_count()):
            row = table_data[i]
            print(fStr.format(row_names[i], *row))

        if boundary:
            print(len(fStr.format("", *col_names)) * "=")

    # def __str__(self, *args):
    #     # This has to be modified
    #     # self.print_matrix(*args)
    #     return "__str__ not implemented"
