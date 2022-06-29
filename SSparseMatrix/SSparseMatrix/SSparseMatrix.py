import itertools
import pickle

import numpy
import scipy
from scipy import sparse


# ======================================================================
# Utilities
# ======================================================================
def is_s_sparse_matrix(obj):
    return isinstance(obj, SSparseMatrix) and scipy.sparse.issparse(obj.sparse_matrix())


def make_s_sparse_matrix(matrix, rows="", columns=""):
    obj = SSparseMatrix()
    obj.set_sparse_matrix(matrix)

    if not isinstance(rows, type(None)):
        obj.set_row_names(rows)

    if not isinstance(columns, type(None)):
        obj.set_column_names(columns)

    return obj


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


def _is_num_like(x):
    return isinstance(x, int) or isinstance(x, float) or isinstance(x, complex)


def _reverse_sort_dict(x):
    return dict([(k, v) for k, v in sorted(x.items(), key=lambda item: -item[1])])


# ------------------------------------------------------------------
# Column binding
# ------------------------------------------------------------------
def column_bind(matrices):
    if isinstance(matrices, list):
        return column_bind(dict(zip([str(x) for x in range(len(matrices))], matrices)))
    elif isinstance(matrices, dict):
        res = None
        for k in matrices:
            if is_s_sparse_matrix(res) and is_s_sparse_matrix(matrices[k]):
                res = res.column_bind(matrices[k])
            else:
                res = matrices[k]
        return res
    else:
        raise TypeError("The first argument is expected to be a list or dictionary of SSparseMatrix objects.")


# ======================================================================
# Class definition
# ======================================================================
class SSparseMatrix:
    _sparseMatrix = None
    _rowNames = None
    _colNames = None
    _dimNames = None

    # The following two fields are conceptually redundant
    # Introduced for optimization purposes -- for example .row_names was too slow
    # just using the dictionary _row_names.
    _rowNamesList = None
    _colNamesList = None

    def __init__(self, *args, **kwargs):
        """Creation of a SSparseMatrix object.
           The first argument is expected to be scipy sparse object.
           The second argument and third argument, if provided,
           are expected to be row names and column names respectively.
           Alternatively, the corresponding named arguments
           "row_names" and "column_names" can be used.
        """
        self._sparseMatrix = None
        self._rowNames = None
        self._colNames = None
        self._dimNames = None

        self._rowNamesList = None
        self._colNamesList = None

        if len(args) == 1:
            self.set_sparse_matrix(args[0])
        elif len(args) == 3:
            self.set_sparse_matrix(args[0])
            self.set_row_names(args[1])
            self.set_column_names(args[2])
        elif len(args) > 1:
            raise TypeError("""No arguments, a matrix argument, or a matrix argument 
            and row and column names are expected.""")

        if len(args) == 0 and "matrix" in kwargs:
            self.set_sparse_matrix(kwargs.get("matrix"))

        if len(args) < 3 and "row_names" in kwargs:
            self.set_row_names(kwargs.get("row_names"))

        if len(args) < 3 and "column_names" in kwargs:
            self.set_column_names(kwargs.get("column_names"))

    # ------------------------------------------------------------------
    #  Getters
    # ------------------------------------------------------------------
    def sparse_matrix(self) -> scipy.sparse.csc.csc_matrix:
        """Sparse matrix."""
        return self._sparseMatrix

    def row_names_dict(self):
        """Row names to indices dictionary."""
        return self._rowNames

    def row_names(self):
        """Row names."""
        if isinstance(self._rowNamesList, list):
            return self._rowNamesList
        elif isinstance(self._rowNames, dict):
            self._rowNamesList = list(self._rowNames.keys())
            return self._rowNamesList
        else:
            self._rowNamesList = self._rowNames
            return self._rowNamesList

    def column_names_dict(self):
        """Column names to indices dictionary."""
        return self._colNames

    def column_names(self):
        """Column names."""
        if isinstance(self._colNamesList, list):
            return self._colNamesList
        elif isinstance(self._colNames, dict):
            self._colNamesList = list(self._colNames.keys())
            return self._colNamesList
        else:
            self._colNamesList = self._colNames
            return self._colNames

    def dimension_names(self):
        """Dimension names."""
        return list(self._dimNames.keys())

    def rows_count(self):
        """Number of rows."""
        return self.sparse_matrix().shape[0]

    def nrow(self):
        """Number of rows."""
        return self.sparse_matrix().shape[0]

    def columns_count(self):
        """Number of columns."""
        return self.sparse_matrix().shape[1]

    def ncol(self):
        """Number of columns."""
        return self.sparse_matrix().shape[1]

    def shape(self):
        """Shape."""
        return self.sparse_matrix().shape

    def dim(self):
        """Dimensions. (Synonym of shape.)"""
        return self.sparse_matrix().shape

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
    # Setters
    # ------------------------------------------------------------------
    def set_sparse_matrix(self, arg, as_is=False):
        """Set sparse matrix object. (In place operation.)"""
        if scipy.sparse.issparse(arg):
            if as_is:
                self._sparseMatrix = arg
            else:
                self._sparseMatrix = arg.tocsr()
            return self
        elif isinstance(arg, list) or isinstance(arg, numpy.ndarray):
            smat2 = scipy.sparse.csr_matrix(arg)
            if scipy.sparse.issparse(smat2):
                self._sparseMatrix = smat2
        else:
            raise TypeError("The first argument is expected to a matrix is or can be coerced to csr sparse matrix.")

        return self

    def set_row_names(self, *args):
        """Set row names. (In place operation.)"""
        self._rowNamesList = None
        if len(args) == 0:
            return self.set_row_names([str(x) for x in range(0, self.rows_count())])
        elif isinstance(args[0], str):
            return self.set_row_names([args[0] + str(x) for x in range(0, self.rows_count())])
        elif isinstance(args[0], dict) and len(args[0]) == self.rows_count():
            self._rowNames = args[0]
        elif isinstance(args[0], list) and len(args[0]) == self.rows_count():
            self._rowNames = dict(zip(args[0], range(0, len(args[0]))))
        else:
            raise TypeError(
                """The first argument is expected to be a string-to-index dictionary of length %s, 
                a list of strings of length %s, or a string.""" %
                (self.rows_count(), self.rows_count()))

        return self

    def set_column_names(self, *args):
        """Set column names. (In place operation.)"""
        self._colNamesList = None
        if len(args) == 0:
            return self.set_column_names([str(x) for x in range(0, self.columns_count())])
        elif isinstance(args[0], str):
            return self.set_column_names([args[0] + str(x) for x in range(0, self.columns_count())])
        elif isinstance(args[0], dict) and len(args[0]) == self.columns_count():
            self._colNames = args[0]
        elif isinstance(args[0], list) and len(args[0]) == self.columns_count():
            self._colNames = dict(zip(args[0], range(0, len(args[0]))))
        else:
            raise TypeError(
                """The first argument is expected to be a string-to-index dictionary of length %s,
                a list of strings of length %s, or a string.""" %
                (self.columns_count(), self.columns_count()))

        return self

    def set_dimension_names(self, *args):
        """Set dimension names. (In place operation.)"""
        if len(args) == 0:
            self.set_dimension_names([str(x) for x in (0, 1)])
        elif isinstance(args[0], dict) and len(args[0]) == 2:
            self._dimNames = args[0]
        elif isinstance(args[0], list) and len(args[0]) == 2:
            self._dimNames = dict(zip(args[0], range(0, len(args[0]))))
        else:
            raise TypeError(
                "The first argument is expected to be a string-to-index dictionary or a list of strings of length 2.")

        return self

    # ------------------------------------------------------------------
    # Predicates
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
        """Equivalence with another SSparseMatrix object.

        :type other: SSparseMatrix
        :param other: Another object
        :rtype: bool
        :return res: Equivalent or not?
        """
        if is_s_sparse_matrix(other):

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
    def transpose(self, copy=True):
        """Transpose."""
        obj = self.copy() if copy else self
        obj._sparseMatrix = obj.sparse_matrix().transpose()
        t = obj.column_names()
        obj.set_column_names(obj.row_names())
        obj.set_row_names(t)
        return obj

    # ------------------------------------------------------------------
    # Conjugate transpose
    # ------------------------------------------------------------------
    def conjugate(self, copy=True):
        """Conjugate elementwise."""
        obj = self.copy() if copy else self
        obj._sparseMatrix = obj.sparse_matrix().conj()
        return obj

    def conjugate_transpose(self, copy=True):
        """Conjugate transpose."""
        obj = self.copy() if copy else self
        obj.conjugate(copy=False)
        obj.transpose(copy=False)
        return obj

    # ------------------------------------------------------------------
    # Add
    # ------------------------------------------------------------------
    def add(self, other, copy=True):
        """Element-wise addition with another SSparseMatrix object,
         or a scipy sparse matrix, or a scalar."""
        obj = self.copy() if copy else self
        if isinstance(other, SSparseMatrix) and \
                obj.row_names() == other.row_names() and \
                obj.column_names() == other.column_names():
            obj._sparseMatrix = obj.sparse_matrix() + other.sparse_matrix()
        elif scipy.sparse.issparse(other):
            obj._sparseMatrix = obj.sparse_matrix() + other
        else:
            raise TypeError("The first argument is expected to be SSparseMatrix object or sparse.csr_matrix object.")

        return obj

    # ------------------------------------------------------------------
    # Multiply
    # ------------------------------------------------------------------
    def multiply(self, other, copy=True):
        """Element-wise multiplication with another SSparseMatrix object,
         or a scipy sparse matrix, or a scalar."""
        obj = self.copy() if copy else self
        if isinstance(other, SSparseMatrix) and \
                obj.row_names() == other.row_names() and \
                obj.column_names() == other.column_names():
            obj._sparseMatrix = obj.sparse_matrix().multiply(other.sparse_matrix())
        elif scipy.sparse.issparse(other) or _is_num_like(other):
            obj._sparseMatrix = obj.sparse_matrix().multiply(other)
        else:
            raise TypeError("The first argument is expected to be SSparseMatrix object or sparse.csr_matrix object.")

        return obj

    # ------------------------------------------------------------------
    # Unitize
    # ------------------------------------------------------------------
    def unitize(self):
        """Make all non-zero elements 1. (In place operation.)"""
        self.set_sparse_matrix(self.sparse_matrix().astype(bool).astype(float))
        return self

    # ------------------------------------------------------------------
    # Clip
    # ------------------------------------------------------------------
    def clip(self, v_min, v_max, copy=True):
        """Clip the values in a SSparseMatrix object."""
        smat = self.sparse_matrix()

        smat.data *= smat.data >= v_min
        smat.data *= smat.data <= v_max
        smat.eliminate_zeros()

        if copy:
            return SSparseMatrix(smat, row_names=self.row_names(), column_names=self.column_names())
        else:
            return self.set_sparse_matrix(smat)

    # ------------------------------------------------------------------
    # Dot
    # ------------------------------------------------------------------
    def dot(self, other, copy=True):
        """Dot product with another object that is a SSparseMatrix object, or scipy sparse matrix,
        or a list, or a numpy array."""
        # I am not sure should we check that : self.column_names() == other.row_names()
        # It might be too restrictive.
        # obj = self.copy() if copy else self
        obj = SSparseMatrix() if copy else self
        if is_s_sparse_matrix(other):
            obj._sparseMatrix = self.sparse_matrix().dot(other.sparse_matrix())
            obj._sparseMatrix.eliminate_zeros()
            # We keep the row names i.e. self.rowNames = self.row_names_dict()
            obj.set_column_names(other.column_names_dict())
            obj.set_row_names(self.row_names_dict())
        elif scipy.sparse.issparse(other):
            obj._sparseMatrix = self.sparse_matrix().dot(other)
            obj._sparseMatrix.eliminate_zeros()
            obj.set_column_names()
            obj.set_row_names(self.row_names_dict())
        elif isinstance(other, list):
            vec = self.sparse_matrix().dot(other)
            rowInds = [x for x in range(self.rows_count())]
            colInds = [0 for x in range(self.rows_count())]
            res = scipy.sparse.coo_matrix((vec, (rowInds, colInds)), shape=(self.rows_count(), 1))
            res.eliminate_zeros()
            obj.set_sparse_matrix(res)
            obj.set_column_names()
            obj.set_row_names(self.row_names_dict())
        elif isinstance(other, numpy.ndarray):
            if len(other.shape) == 1:
                vec = scipy.sparse.csr_matrix([other, ]).transpose()
            else:
                vec = scipy.sparse.csr_matrix(other)
            obj = self.dot(vec)
        else:
            raise TypeError("The first argument is expected to be SSparseMatrix object or sparse.csr_matrix object.")

        return obj

    # ------------------------------------------------------------------
    # Maximums
    # ------------------------------------------------------------------
    def row_maximums(self):
        """Give the row maximums"""
        return self.sparse_matrix().max(axis=1).todense().flatten().tolist()[0]

    def row_maximums_dict(self):
        """Give a dictionary of the row-names to row-maximums."""
        return dict(zip(self.row_names(), self.row_maximums()))

    def column_maximums(self):
        """Give the column maximums."""
        return self.sparse_matrix().max(axis=0).todense().flatten().tolist()[0]

    def column_maximums_dict(self):
        """Give a dictionary of the column-names to column-maximums."""
        return dict(zip(self.column_names(), self.column_maximums()))

    # ------------------------------------------------------------------
    # Minimums
    # ------------------------------------------------------------------
    def row_minimums(self):
        """Give the row minimums"""
        return self.sparse_matrix().min(axis=1).todense().flatten().tolist()[0]

    def row_minimums_dict(self):
        """Give a dictionary of the row-names to row-minimums."""
        return dict(zip(self.row_names(), self.row_minimums()))

    def column_minimums(self):
        """Give the column minimums."""
        return self.sparse_matrix().min(axis=0).todense().flatten().tolist()[0]

    def column_minimums_dict(self):
        """Give a dictionary of the column-names to column-mins."""
        return dict(zip(self.column_names(), self.column_minimums()))

    # ------------------------------------------------------------------
    # Summation
    # ------------------------------------------------------------------
    def row_sums(self):
        """Give the row sums"""
        return self.sparse_matrix().sum(axis=1).flatten().tolist()[0]

    def row_sums_dict(self):
        """Give a dictionary of the row-names to row-sums."""
        return dict(zip(self.row_names(), self.row_sums()))

    def column_sums(self):
        """Give the column sums."""
        return self.sparse_matrix().sum(axis=0).flatten().tolist()[0]

    def column_sums_dict(self):
        """Give a dictionary of the column-names to column-sums."""
        return dict(zip(self.column_names(), self.column_sums()))

    # ------------------------------------------------------------------
    # Impose row names
    # ------------------------------------------------------------------
    def impose_row_names(self, names):
        """Impose row names. (New SSparseMatrix object is created.)"""
        obj = self.copy()

        if not isinstance(names, list):
            raise TypeError("The first argument is expected to be a list of strings.")

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
        """Impose column names. (New SSparseMatrix object is created.)"""
        if isinstance(names, list):
            return self.transpose().impose_row_names(names).transpose(copy=False)
        else:
            raise TypeError("The first argument is expected to be a list of strings.")

    # ------------------------------------------------------------------
    # Row binding
    # ------------------------------------------------------------------
    def row_bind(self, other):
        """Row binding with another SSparseMatrix object."""
        if is_s_sparse_matrix(other):

            if not (sorted(self.column_names()) == sorted(other.column_names())):
                raise TypeError("The column names of the two SSparseMatrix objects are expected to be the same.")

            if self.column_names() == other.column_names():
                res = SSparseMatrix(scipy.sparse.vstack([self.sparse_matrix(), other.sparse_matrix()]))
            else:
                mat = scipy.sparse.vstack([self.sparse_matrix(), other[:, self.column_names()].sparse_matrix()])
                res = SSparseMatrix(mat)

            # Set the column names
            res.set_column_names(self.column_names())

            # Special handling of duplication of row names in the result.
            # rn_dict = self.row_names_dict() | other.row_names_dict() # this is Version 3.9+ only
            rn_dict = {**self.row_names_dict(), **other.row_names_dict()}
            if len(rn_dict) == (self.rows_count() + other.rows_count()):
                res.set_row_names(self.row_names() + other.row_names())
            else:
                res.set_row_names([x + ".1" for x in self.row_names()] + [x + ".2" for x in other.row_names()])

            return res

        else:
            raise TypeError("The first argument is expected to be a SSparseMatrix object.")

    # ------------------------------------------------------------------
    # Column binding
    # ------------------------------------------------------------------
    # Although there is an "easy" implementation using transposed matrices
    # it is considered potentially too slow.
    def column_bind(self, other):
        """Column binding with another SSparseMatrix object."""
        if is_s_sparse_matrix(other):

            if not (sorted(self.row_names()) == sorted(other.row_names())):
                raise TypeError("The row names of the two SSparseMatrix objects are expected to be the same.")

            if self.row_names() == other.row_names():
                res = SSparseMatrix(scipy.sparse.hstack([self.sparse_matrix(), other.sparse_matrix()]))
            else:
                mat = scipy.sparse.hstack([self.sparse_matrix(), other[self.row_names(), :].sparse_matrix()])
                res = SSparseMatrix(mat)

            # Set the row names
            res.set_row_names(self.row_names())

            # Special handling of duplication of row names in the result.
            # cn_dict = self.column_names_dict() | other.column_names_dict() # this is version 3.9+ only
            cn_dict = {**self.column_names_dict(), **other.column_names_dict()}
            if len(cn_dict) == (self.columns_count() + other.columns_count()):
                res.set_column_names(self.column_names() + other.column_names())
            else:
                res.set_column_names([x + ".1" for x in self.column_names()] + [x + ".2" for x in other.column_names()])

            return res

        else:
            raise TypeError("The first argument is expected to be a SSparseMatrix object.")

    # ------------------------------------------------------------------
    # Triplets
    # ------------------------------------------------------------------
    def triplets(self):
        """Give a list of triplets (row, column, value) of the SSparseMatrix object."""
        A = self.sparse_matrix().tocoo()
        return list(zip([self.row_names()[i] for i in A.row],
                        [self.column_names()[i] for i in A.col],
                        A.data))

    # ------------------------------------------------------------------
    # Row dictionaries
    # ------------------------------------------------------------------
    def row_dictionaries(self, sort=False):
        """Row dictionaries."""
        triplets = self.triplets()
        triplets.sort(key=lambda x: x[0])
        rowGroups = dict([(key, dict([(col, v) for (_, col, v) in value]))
                          for key, value in itertools.groupby(triplets, lambda x: x[0])])
        if sort:
            rowGroups = dict([(k, _reverse_sort_dict(v)) for (k, v) in rowGroups.items()])
        return rowGroups

    def rows_dict(self, sort=False):
        """Row dictionaries. (Synonym of row_dictionaries.)"""
        return self.row_dictionaries(sort=sort)

    # ------------------------------------------------------------------
    # Column dictionaries
    # ------------------------------------------------------------------
    def column_dictionaries(self, sort=False):
        """Column dictionaries."""
        # Could be done directly if some performance issues come up...
        return self.transpose().row_dictionaries(sort=sort)

    def cols_dict(self, sort=False):
        """Column dictionaries. (Synonym of column_dictionaries.)"""
        return self.column_dictionaries(sort=sort)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------
    def __str__(self):
        """String form of SSparseMatrix object that resembles that of scipy sparse matrices."""
        maxprint = self.sparse_matrix().getmaxprint()

        A = self.sparse_matrix().tocoo()
        A2 = ([self.row_names()[i] for i in A.row],
              [self.column_names()[i] for i in A.col],
              A.data)

        # Helper function to output "(i,j)  v"
        def to_str(row, col, data):
            triples = zip(list(zip(row, col)), data)
            return '\n'.join([('  %s\t%s' % t) for t in triples])

        if self.sparse_matrix().nnz > maxprint:
            half = maxprint // 2
            out = to_str(A2[0][:half], A2[1][:half], A2[2][:half])
            out += "\n  :\t:\n"
            half = maxprint - maxprint // 2
            out += to_str(A2[0][-half:], A2[1][-half:], A2[2][-half:])
        else:
            out = to_str(A2[0], A2[1], A2[2])

        return out

    def __repr__(self):
        """Representation of SSparseMatrix object."""
        tsize = self.sparse_matrix().shape[0] * self.sparse_matrix().shape[1]
        res = repr(self.sparse_matrix())
        res = res.replace("sparse matrix", "SSparseMatrix (sparse matrix with named rows and columns)")
        res = res.replace("format>", "format, and fill-in " + str(self.sparse_matrix().nnz / tsize) + ">")
        return res

    # ------------------------------------------------------------------
    # To dictionary form
    # ------------------------------------------------------------------
    def to_dict(self):
        """Convert to dictionary form.

        Returns dictionary representation of the SSparseMatrix object with keys
        ['rowIndexes', 'columnIndexes', 'values', 'shape', 'rowNames', 'columnNames'].

        The keys ['rowIndexes', 'columnIndexes', 'values'] correspond to the result of scipy.sparse.find.

        The row- and column indices are given separately from the row- and column names in order
        to facilitate rapid conversion and serialization.
        """
        res = scipy.sparse.find(self.sparse_matrix())
        res = dict(zip(['rowIndexes', 'columnIndexes', 'values'], res))
        # This is version 3.9+ only:
        # res = res | {"shape": self.shape(), "rowNames": self.row_names(), "columnNames": self.column_names()}
        res = {**res, "shape": self.shape(), "rowNames": self.row_names(), "columnNames": self.column_names()}
        return res

    # ------------------------------------------------------------------
    # From dictionary form
    # ------------------------------------------------------------------
    def from_dict(self, arg):
        """Convert from dictionary form.

        Creates the SSparseMatrix internals from dictionary representation (of a SSparseMatrix object) with keys
        ['rowIndexes', 'columnIndexes', 'values', 'shape', 'rowNames', 'columnNames'].

        The keys ['rowIndexes', 'columnIndexes', 'values'] correspond to the result of scipy.sparse.find.

        The row- and column indices are given separately from the row- and column names in order
        to facilitate rapid conversion and serialization.
        """
        if not (isinstance(arg, dict) and
                all([x in {'rowIndexes', 'columnIndexes', 'values', 'shape', 'rowNames', 'columnNames'}
                     for x in list(arg.keys())]
                    )):
            raise TypeError("""The first argument is expected to be a dictionary with keys:
            'rowIndexes', 'columnIndexes', 'values', 'shape', 'rowNames', 'columnNames'.""")
        smat = scipy.sparse.coo_matrix((arg["values"], (arg["rowIndexes"], arg["columnIndexes"])), arg["shape"])
        self.set_sparse_matrix(smat)
        self.set_row_names(arg["rowNames"])
        self.set_column_names(arg["columnNames"])
        return self

    # ------------------------------------------------------------------
    # Wolfram Language full form
    # ------------------------------------------------------------------
    def to_wl_string(self):
        """Wolfram Language (WL) full form representation string of the SSparseMatrix object."""
        A = self.sparse_matrix().tocoo()
        triplets = list(zip([x + 1 for x in A.row], [x + 1 for x in A.col], A.data))

        out = ','.join([('{%s,%s}->%s' % t) for t in triplets])
        out = '{' + out + '}'

        rows_wl = str(self.row_names()).replace("'", "\"").replace("[", "{").replace("]", "}")
        cols_wl = str(self.column_names()).replace("'", "\"").replace("[", "{").replace("]", "}")

        return "Association[\"SparseMatrix\"->SparseArray[" + out + ",{" + str(self.rows_count()) + ', ' + \
               str(self.columns_count()) + "}]," + "\"RowNames\"->" + rows_wl + ",\"ColumnNames\"->" + cols_wl + "]"

    # ------------------------------------------------------------------
    # Convert to Wolfram Language (deferred)
    # ------------------------------------------------------------------
    def to_wl(self):
        """Convert to Wolfram Language form (deferred.)

        See the GitHub repository
        `Wolfram Client for Python: <https://github.com/wolframResearch/WolframClientForPython>`_.

        See the WL package
        `SSparseMatrix.m <https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m>`_.

        The actual definition (most likely) uses the dictionary representation, self.to_dict().
        (The function SSparseMatrix`ToSSparseMatrix knows how to make SSparseMatrix objects from that representation.)

        Here is a definition with the declaration of the package wolframclient:

        ..code:: python
            from wolframclient.language import wl

            def to_wl(self):
                return wl.SSparseMatrix.ToSSparseMatrix(self.to_dict())
        """
        pass

    # ------------------------------------------------------------------
    # Print outs
    # ------------------------------------------------------------------
    def print_matrix(self, boundary=True, dotted_implicit=True, n_digits=-1):
        """Pretty printing of the SSparseMatrix object."""
        table_data = numpy.asarray(self.sparse_matrix().todense())

        invRowNames = {v: k for k, v in self.row_names_dict().items()}
        invColumnNames = {v: k for k, v in self.column_names_dict().items()}

        col_names = [invColumnNames[x] for x in sorted(invColumnNames.keys())]
        row_names = [invRowNames[x] for x in sorted(invRowNames.keys())]

        if not isinstance(n_digits, int):
            raise TypeError("The argument n_digits is expected to be an integer.")

        if n_digits < 1:
            # Not good enough for automatic determination
            # nds = math.ceil(math.log(self.sparse_matrix().max(), 10)) + 1
            nds = 8
        else:
            nds = n_digits

        nds = max(nds, max([len(cn) for cn in self.column_names()]) + 1)

        fColSpec = "{: >" + str(max([len(x) for x in self.row_names()])) + "}"
        fSpec = "{: >" + str(nds) + "}"
        fStr = fColSpec + " |" + self.columns_count() * fSpec

        if boundary:
            print(len(fStr.format("", *col_names)) * "=")

        print(fStr.format("", *col_names))
        print(len(fStr.format("", *col_names)) * "-")

        indices_set = set(zip(*self.sparse_matrix().nonzero()))

        for i in range(self.rows_count()):
            if dotted_implicit:
                row = [str(x) for x in table_data[i]]
                for j in range(len(row)):
                    if not (i, j) in indices_set:
                        row[j] = "."
            else:
                row = table_data[i]
            print(fStr.format(row_names[i], *row))

        if boundary:
            print(len(fStr.format("", *col_names)) * "=")

    # ------------------------------------------------------------------
    # Delegation methods
    # ------------------------------------------------------------------
    _delegated_queries = {"asformat", "asfptype", "astype", "check_format", "count_nonzero",
                          "data", "diagonal", "dtype", "format", "getcol", "getformat", "getH",
                          "getmaxprint", "getnnz", "getrow", "get_shape", "has_canonical_format",
                          "has_sorted_indices", "indices", "indptr", "maxprint", "ndim", "nnz",
                          "nonzero", "shape", "toarray", "tobsr", "tocoo", "tocsc", "tocsr",
                          "todense", "todia", "todok", "tolil"}

    _delegated_mat = {"arcsin", "arcsinh", "arctan", "arctanh", "argmax", "argmin",
                      "ceil", "deg2rad", "eliminate_zeros", "expm1", "floor",
                      "log1p", "power", "prune", "rad2deg", "rint",
                      "sign", "sin", "sinh", "sort_indices", "sorted_indices",
                      "sqrt", "tan", "tanh", "trunc"}

    # ------------------------------------------------------------------
    # Delegation
    # ------------------------------------------------------------------
    def __getattr__(self, method_name):
        if method_name in self._delegated_queries:

            res = getattr(self.sparse_matrix(), method_name)
            return res

        elif method_name in self._delegated_mat:

            def delegated_method(*args, **kwargs):
                resMat = getattr(self.sparse_matrix(), method_name)(*args, **kwargs)
                return SSparseMatrix(resMat, row_names=self.row_names(), column_names=self.column_names())

            return delegated_method

        else:
            return getattr(SSparseMatrix, method_name)
