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

mat = [[1, 0, 4, 16], [4, 0, 0, 10], [0, 9, 5, 5], [0, 0, 1, 0], [0, 0, 0, 5]]
smat = SSparseMatrix(mat)
smat.set_row_names(["A", "B", "C", "D", "E"])
smat.set_column_names(["a", "b", "c", "d"])


class DotProduct(unittest.TestCase):

    def test_dot_matrix(self):
        smat2 = smat.copy().dot(copy.deepcopy(smat).transpose())
        smat3 = smat.sparse_matrix().dot(smat.sparse_matrix().transpose())
        smat4 = SSparseMatrix(smat3)
        smat4.set_row_names(smat.row_names())
        smat4.set_column_names(smat.row_names())
        self.assertTrue(smat2.eq(smat4))

    def test_dot_list_1(self):
        vec2 = [1, 1, 3, 4]
        smat2 = smat.copy().dot(vec2)
        res2 = smat.sparse_matrix().dot(vec2)
        vec2 = [smat[i, 0] for i in range(smat2.rows_count())]
        self.assertTrue((res2 == vec2).all)

    def test_dot_ndarray_1(self):
        vec3 = numpy.array([1, 1, 3, 4])
        smat3 = smat.copy().dot(vec3)
        res3 = smat.sparse_matrix().dot(vec3)
        vec3 = [smat[i, 0] for i in range(smat3.rows_count())]
        self.assertTrue((res3 == vec3).all)


if __name__ == '__main__':
    unittest.main()
