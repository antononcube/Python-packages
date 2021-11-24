# Follows the tests in
#   https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m

import unittest

from SSparseMatrix.SSparseMatrix import *

mat = [[1, 0, 4, 16], [4, 0, 0, 10], [0, 9, 5, 5], [0, 0, 1, 0], [0, 0, 0, 5]]
smat = SSparseMatrix(mat)
smat.set_row_names(["A", "B", "C", "D", "E"])
smat.set_column_names(["a", "b", "c", "d"])


def is_s_sparse_matrix_dict(arg):
    return isinstance(arg, dict) and \
           all([x in {'rowIndexes', 'columnIndexes', 'values', 'shape', 'rowNames', 'columnNames'}
                for x in list(arg.keys())]
               )


class DotProduct(unittest.TestCase):

    def test_to_dict_1(self):
        # Verify to_dict() produces a dictionary representing SSparseMatrix object
        self.assertTrue(is_s_sparse_matrix_dict(smat.to_dict()))

    def test_to_dict_2(self):
        # Verify to_dict() produces a dictionary representing SSparseMatrix object

        # Dot product with the transpose SSparseMatrix
        smat2 = smat.copy().dot(smat.copy().transpose())

        # Verify is a dictionary representing SSparseMatrix object
        self.assertTrue(is_s_sparse_matrix_dict(smat2.to_dict()))

    def test_from_dict_1(self):
        # Verify from_dict() produces a SSparseMatrix object

        self.assertTrue(is_s_sparse_matrix(SSparseMatrix().from_dict(smat.to_dict())))

    def test_from_dict_2(self):
        # Verify from_dict() produces a SSparseMatrix object

        # Verify SSparseMatrix objects are equivalent
        self.assertTrue(smat.eq(SSparseMatrix().from_dict(smat.to_dict())))


if __name__ == '__main__':
    unittest.main()
