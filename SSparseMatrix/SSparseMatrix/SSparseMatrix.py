import numpy
import scipy
from scipy import sparse


class SSparseMatrix:

    def __init__(self):
        self.id = "SSparseMatrix"
        self.sparseMatrix = None
        self.rowNames = None
        self.colNames = None
        self.dimensionNames = None

    def make_from_sparse_matrix(self, smat: sparse.csr_matrix):
        self.__init__()
        self.set_sparse_matrix(smat)
        return self

    # ------------------------------------------------------------------
    #  Getters
    # ------------------------------------------------------------------
    def sparse_matrix(self) -> scipy.sparse.csc.csc_matrix:
        return self.sparseMatrix

    def row_names(self):
        return self.rowNames

    def column_names(self):
        return self.colNames

    def dimension_names(self):
        return self.dimensionNames

    def rows_count(self):
        return self.sparse_matrix().shape[0]

    def columns_count(self):
        return self.sparse_matrix().shape[1]

    def shape(self):
        return self.sparse_matrix().shape

    # ------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------
    def set_sparse_matrix(self, arg):
        if scipy.sparse.issparse(arg):
            self.sparseMatrix = arg
        else:
            print("The first argument is expected to be sparse.csr_matrix.")
            return None
        return self

    def set_row_names(self, arg):
        if isinstance(arg, dict) and len(arg) == self.rows_count():
            self.rowNames = arg
        elif isinstance(arg, list) and len(arg) == self.rows_count():
            self.rowNames = dict(zip(arg, range(0, len(arg))))
        else:
            print(
                "The first argument is expected to be a string-to-index dictionary or a list of strings of length %d.",
                self.rows_count())
            return None
        return self

    def set_column_names(self, arg):
        if isinstance(arg, dict) and len(arg) == self.columns_count():
            self.colNames = arg
        elif isinstance(arg, list) and len(arg) == self.columns_count():
            self.colNames = dict(zip(arg, range(0, len(arg))))
        else:
            print(
                "The first argument is expected to be a string-to-index dictionary or a list of strings of length %d.",
                self.columns_count())
            return None
        return self

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
            print("The first argument is expected to be SSparseMatrix object or sparse.csr_matrix object.")
            return None
        return self

    # ------------------------------------------------------------------
    # Dot
    # ------------------------------------------------------------------
    def dot(self, other):
        # I am not sure should we check that : self.column_names() == other.row_names()
        # It might be too restrictive.
        if isinstance(other, SSparseMatrix):
            print(self.shape())
            print(other.shape())
            self.sparseMatrix = self.sparse_matrix().dot(other.sparse_matrix())
            # We keep the row names i.e. self.rowNames = self.row_names()
            self.colNames = other.column_names()
        elif scipy.sparse.issparse(other):
            self.sparseMatrix = self.sparse_matrix().dot(other)
            self.colNames = None
        else:
            print("The first argument is expected to be SSparseMatrix object or sparse.csr_matrix object.")
            return None
        return self

    # ------------------------------------------------------------------
    # Print outs
    # ------------------------------------------------------------------
    def print_matrix(self):
        table_data = numpy.asarray(self.sparse_matrix().todense())

        invRowNames = {v: k for k, v in self.row_names().items()}
        invColumnNames = {v: k for k, v in self.column_names().items()}

        col_names = [invColumnNames[x] for x in sorted(invColumnNames.keys())]
        row_names = [invRowNames[x] for x in sorted(invRowNames.keys())]

        fStr = (self.columns_count() + 1) * "{: >20} "
        print(fStr.format("", *col_names))

        for i in range(self.rows_count()):
            row = table_data[i]
            print(fStr.format(row_names[i], *row))
