# Follows the tests in
#   https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m

import unittest

from SSparseMatrix.SSparseMatrix import *
import numpy

mat = [[1, 0, 4, 16], [4, 0, 0, 10], [0, 9, 5, 5], [0, 0, 1, 0], [0, 0, 0, 5]]
smat = SSparseMatrix(mat)
smat.set_row_names(["A", "B", "C", "D", "E"])
smat.set_column_names(["a", "b", "c", "d"])


class DotProduct(unittest.TestCase):

    def test_dot_matrix_1(self):
        # Verify that matrix-matrix dot product is correct

        # Dot product with the transpose SSparseMatrix
        smat2 = smat.copy().dot(smat.copy().transpose())

        # Dot product with the transpose scipy.sparse.csr_matrx
        smat3 = smat.sparse_matrix().dot(smat.sparse_matrix().transpose())

        # Make the SSparseMatrix expected result
        smat4 = SSparseMatrix(smat3)
        smat4.set_row_names(smat.row_names())
        smat4.set_column_names(smat.row_names())

        # Verify equality
        self.assertTrue(smat2.eq(smat4))

    def test_dot_matrix_2(self):
        # Verify that column names are ignored in matrix-matrix dot product

        # Column names
        cns1 = ["X1", "X2", "X3", "X4"]

        # Copy SSparseMatrix object and assign the new column names
        smat2 = smat.copy()
        smat2.set_column_names(cns1)

        # Dot product the transpose
        smat3 = smat.dot(smat.transpose())

        # Dot product of smat2 with the transpose of smat
        smat4 = smat2.dot(smat.transpose())

        # Verify same results
        self.assertTrue(smat3.eq(smat4))

    def test_dot_matrix_3(self):
        # Verify that copying is not needed

        smat2 = smat.dot(smat.transpose())

        smat3 = smat.copy().dot(smat.copy().transpose())

        # Verify same results
        self.assertTrue(smat2.eq(smat3))

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
