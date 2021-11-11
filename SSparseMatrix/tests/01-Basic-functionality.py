# Follows the tests in
#   https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m

import unittest

from SSparseMatrix.src.SSparseMatrix import *
import scipy
import numpy


class BasicFunctionalities(unittest.TestCase):
    mat = [[1, 0, 0, 4, 0], [0, 2, 0, 0, 0], [0, 0, 0, 0, 2], [0, 0, 3, 0, 0]]
    mat2 = [[1, 0, 4], [0, 2, 0], [0, 0, 0], [0, 0, 3]]
    rmat = 0
    rmat2 = 0;

    def test_make_1(self):
        obj1 = SSparseMatrix()
        obj1.set_sparse_matrix(self.mat)
        obj2 = SSparseMatrix(self.mat)
        self.assertTrue(obj1.eq(obj2))

    def test_make_2(self):
        obj1 = SSparseMatrix()
        obj1.set_sparse_matrix(self.mat)
        obj1.set_row_names(list("ABCD"))
        obj1.set_column_names(list("abcde"))
        obj2 = SSparseMatrix(self.mat, list("ABCD"), list("abcde"))
        self.assertTrue(obj1.eq(obj2))

    def test_make_3(self):
        obj1 = SSparseMatrix()
        obj1.set_sparse_matrix(self.mat)
        obj1.set_row_names(list("0123"))
        obj1.set_column_names(list("01234"))
        obj2 = SSparseMatrix(matrix=self.mat, row_names="", column_names="")
        self.assertTrue(obj1.eq(obj2))

    def test_make_4(self):
        obj1 = SSparseMatrix()
        obj1.set_sparse_matrix(self.mat)
        obj1.set_row_names(list("ABCD"))
        obj1.set_column_names(list("01234"))
        obj2 = SSparseMatrix(self.mat, row_names=list("ABCD"), column_names="")
        self.assertTrue(obj1.eq(obj2))

    def test_mat(self):
        self.mat = scipy.sparse.csr_matrix(self.mat)
        self.assertTrue(scipy.sparse.issparse(self.mat))

    def test_mat_2(self):
        self.mat2 = scipy.sparse.csr_matrix(self.mat2)
        self.assertTrue(scipy.sparse.issparse(self.mat2))

    def test_rmat(self):
        # Make rmat
        row = numpy.array([1, 1, 2, 3, 4])
        row = [x - 1 for x in row]

        col = numpy.array([1, 4, 2, 5, 3], )
        col = [x - 1 for x in col]

        data = numpy.array([1, 4, 2, 2, 3])

        self.rmat = scipy.sparse.coo_matrix((data, (row, col)), shape=(4, 5))
        self.rmat = SSparseMatrix(self.rmat)

        self.rmat.set_row_names(["A", "B", "C", "D"])
        self.rmat.set_column_names(["a", "b", "c", "d", "e"])

        self.assertTrue(is_sparse_matrix(self.rmat))

    def test_row_names_1(self):
        self.test_rmat() and self.assertTrue(self.rmat.row_names() == ["A", "B", "C", "D"])

    def test_column_names_1(self):
        self.test_rmat() and self.assertTrue(self.rmat.column_names() == ["a", "b", "c", "d", "e"])

    def test_set_column_names_1(self):
        self.test_rmat()
        self.rmat2 = self.rmat
        new_cols = [str(x) for x in range(self.rmat.columns_count())]
        self.rmat2.set_column_names(new_cols)
        self.assertTrue(sorted(self.rmat2.column_names()) == sorted(new_cols))

    def test_transpose_1(self):

        self.test_rmat()

        rmat2 = copy.deepcopy(self.rmat).transpose()

        self.assertTrue(
            sorted(rmat2.row_names()) == sorted(self.rmat.column_names()) and
            sorted(rmat2.column_names()) == sorted(self.rmat.row_names()) and
            rmat2.sparse_matrix().shape[0] == self.rmat.sparse_matrix().shape[1] and
            rmat2.sparse_matrix().shape[1] == self.rmat.sparse_matrix().shape[0]
        )


if __name__ == '__main__':
    unittest.main()
