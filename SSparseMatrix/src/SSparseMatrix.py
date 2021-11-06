import copy

import numpy
import scipy
from scipy import sparse
import copy

def is_sparse_matrix(obj):
    return isinstance(obj, SSparseMatrix) and scipy.sparse.issparse(obj.sparse_matrix())


def make_from_sparse_matrix(smat):
    obj = SSparseMatrix()
    return obj.set_sparse_matrix(smat)


class SSparseMatrix:

    def __init__(self, *args):
        self.id = "src"
        self.sparseMatrix = None
        self.rowNames = None
        self.colNames = None
        self.dimensionNames = None
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
        return list(self.dimensionNames.keys())

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
    def transpose(self):
        self.sparseMatrix = self.sparse_matrix().transpose()
        t = self.colNames
        self.colNames = self.rowNames
        self.rowNames = t
        return self

    # ------------------------------------------------------------------
    # Add
    # ------------------------------------------------------------------
    def add(self, other):
        if isinstance(other, SSparseMatrix) and \
                self.row_names() == other.row_names() and \
                self.column_names() == other.column_names():
            self.sparseMatrix = self.sparse_matrix() + other.sparse_matrix()
        elif scipy.sparse.issparse(other):
            self.sparseMatrix = self.sparse_matrix() + other
        else:
            raise TypeError("The first argument is expected to be SSparseMatrix object or sparse.csr_matrix object.")
            return None
        return self

    # ------------------------------------------------------------------
    # Multiply
    # ------------------------------------------------------------------
    def multiply(self, other):
        if isinstance(other, SSparseMatrix) and \
                self.row_names() == other.row_names() and \
                self.column_names() == other.column_names():
            self.sparseMatrix = self.sparse_matrix().multiply(other.sparse_matrix())
        elif scipy.sparse.issparse(other):
            self.sparseMatrix = self.sparse_matrix().multiply(other)
        else:
            raise TypeError("The first argument is expected to be SSparseMatrix object or sparse.csr_matrix object.")
            return None
        return self

    # ------------------------------------------------------------------
    # Dot
    # ------------------------------------------------------------------
    def dot(self, other):
        # I am not sure should we check that : self.column_names() == other.row_names()
        # It might be too restrictive.
        if isinstance(other, SSparseMatrix):
            self.sparseMatrix = self.sparse_matrix().dot(other.sparse_matrix())
            # We keep the row names i.e. self.rowNames = self.row_names_dict()
            self.colNames = other.column_names_dict()
        elif scipy.sparse.issparse(other):
            self.sparseMatrix = self.sparse_matrix().dot(other)
            self.colNames = None
        else:
            raise TypeError("The first argument is expected to be src object or sparse.csr_matrix object.")
            return None
        return self

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
    # Print outs
    # ------------------------------------------------------------------
    def print_matrix(self, boundary=True):
        table_data = numpy.asarray(self.sparse_matrix().todense())

        invRowNames = {v: k for k, v in self.row_names_dict().items()}
        invColumnNames = {v: k for k, v in self.column_names_dict().items()}

        col_names = [invColumnNames[x] for x in sorted(invColumnNames.keys())]
        row_names = [invRowNames[x] for x in sorted(invRowNames.keys())]

        fStr = "{: >20} |" + self.columns_count() * "{: >20} "

        if boundary:
            print(len(fStr.format("", *col_names)) * "=")

        print(fStr.format("", *col_names))
        print(len(fStr.format("", *col_names)) * "-")

        for i in range(self.rows_count()):
            row = table_data[i]
            print(fStr.format(row_names[i], *row))

        if boundary:
            print(len(fStr.format("", *col_names)) * "=")
