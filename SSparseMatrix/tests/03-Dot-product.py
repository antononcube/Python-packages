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

smat = SSparseMatrix([[1, 0, 16, 16], [4, 0, 0, 100], [0, 9, 25, 25]])
smat.set_row_names(["A1", "B3", "C3"])
smat.set_column_names(["a", "b", "c", "d"])


class DotProduct(unittest.TestCase):

    def test_dot_matrix(self):
        smat2 = copy.deepcopy(smat).dot(copy.deepcopy(smat).transpose())
        smat3 = smat.sparse_matrix().dot(smat.sparse_matrix().transpose())
        smat4 = SSparseMatrix(smat3)
        smat4.set_row_names(smat.row_names())
        smat4.set_column_names(smat.row_names())
        self.assertTrue(smat2.eq(smat4))


if __name__ == '__main__':
    unittest.main()
