# Follows the tests in
#   https://github.com/antononcube/MathematicaForPrediction/blob/master/SSparseMatrix.m

import unittest

from SSparseMatrix.SSparseMatrix import *

mat = [[1, 0, 0, 3], [4, 0, 0, 5], [0, 3, 0, 5], [0, 0, 1, 0], [0, 0, 0, 5]]
smat = SSparseMatrix(mat)
smat.set_row_names(["A", "B", "C", "D", "E"])
smat.set_column_names(["a", "b", "c", "d"])


class ColumnAndRowBinding(unittest.TestCase):

    def test_column_bind_1(self):
        # Verify column binding produces expected columns.

        # Create a new matrix with using a transposed smat
        mat2 = smat.sparse_matrix().transpose()
        smat2 = SSparseMatrix(mat2, row_names=list("ABCD"), column_names="c")

        # Column bind a slice of smat with the new matrix
        smat3 = smat[list("ABCD"), :].column_bind(smat2)

        # Verify column binding produced expected columns
        self.assertTrue(smat3.column_names() == (smat.column_names() + smat2.column_names()))

    def test_row_bind_1(self):
        # Verify row binding of two matrices with same row names produces expected columns.

        # Create a new matrix with using a transposed smat
        mat2 = smat.sparse_matrix().transpose()
        smat2 = SSparseMatrix(mat2, row_names=list("ABCD"), column_names="c")

        # Here we rename the column names of `smat` to be the same as `smat2`:
        smat3 = smat.copy()
        smat3.set_column_names(smat2.column_names()[0:4])
        smat3 = smat3.impose_column_names(smat2.column_names())

        # Row bind
        smat4 = smat2.row_bind(smat3)

        # Independent derivation of row names
        rows1 = [x + ".1" for x in smat2.row_names()]
        rows2 = [x + ".2" for x in smat3.row_names()]

        # Verify
        self.assertTrue(smat4.row_names() == (rows1 + rows2))


if __name__ == '__main__':
    unittest.main()
