# Follows the tests in
#   https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m

import unittest

from SSparseMatrix.src.SSparseMatrix import *
import pandas
import scipy
import numpy
from scipy import sparse

from pandas.testing import assert_frame_equal
from scipy.sparse import lil_matrix
from scipy.sparse import *

rmat = SSparseMatrix([[1, 0, 0, 4, 0], [0, 2, 0, 0, 0], [0, 0, 0, 0, 2], [0, 0, 3, 0, 0]])
rmat.set_row_names(["A", "B", "C", "D"])
rmat.set_column_names(["a", "b", "c", "d", "e"])


class PointwiseOperations(unittest.TestCase):

    def test_add_1(self):
        rmat2 = SSparseMatrix(rmat.sparse_matrix() + rmat.sparse_matrix())
        rmat2.set_column_names(rmat.column_names())
        rmat2.set_row_names(rmat.row_names())
        self.assertTrue(rmat.add(rmat).eq(rmat2))

    def test_multiply_1(self):
        rmat2 = SSparseMatrix(rmat.sparse_matrix().multiply(rmat.sparse_matrix()))
        rmat2.set_column_names(rmat.column_names())
        rmat2.set_row_names(rmat.row_names())
        self.assertTrue(rmat.multiply(rmat).eq(rmat2))


if __name__ == '__main__':
    unittest.main()
