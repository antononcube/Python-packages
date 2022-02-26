# Follows the tests in
#   https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m

import unittest

from SSparseMatrix.SSparseMatrix import *
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

    def test_multiply_scalar_1(self):
        rmat2 = SSparseMatrix(rmat.sparse_matrix().multiply(3.0))
        rmat2.set_column_names(rmat.column_names())
        rmat2.set_row_names(rmat.row_names())
        self.assertTrue(rmat.multiply(3.0).eq(rmat2))

    def test_unitize(self):
        rmat2 = rmat.unitize()
        self.assertTrue(min(rmat2.sparse_matrix().data) == 1 and max(rmat2.sparse_matrix().data) == 1)

    def test_clip(self):
        rmat2 = rmat.clip(v_min=2, v_max=3)
        self.assertTrue(min(rmat2.sparse_matrix().data) == 2.0 and
                        max(rmat2.sparse_matrix().data) == 3.0 and
                        rmat2.row_names() == rmat.row_names() and
                        rmat2.column_names() == rmat.column_names())

if __name__ == '__main__':
    unittest.main()
