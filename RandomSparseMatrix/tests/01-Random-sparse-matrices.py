import random
import unittest

from RandomDataGenerators.RandomFunctions import *
from RandomSparseMatrix.RandomFunctions import *
from SSparseMatrix import *


class BasicFunctionalities(unittest.TestCase):

    def test_simple_1(self):
        smat = random_sparse_matrix()
        self.assertTrue(isinstance(smat, SSparseMatrix))

    def test_simple_2(self):
        smat = random_sparse_matrix(n_rows=12, columns_spec=5)
        self.assertTrue(isinstance(smat, SSparseMatrix))

    def test_simple_3(self):
        smat = random_sparse_matrix(n_rows=12)
        self.assertTrue(isinstance(smat, SSparseMatrix))

    def test_simple_4(self):
        smat = random_sparse_matrix(columns_spec=list("ABCDE"))
        self.assertTrue(isinstance(smat, SSparseMatrix))

    def test_n_vals_1(self):
        smat = random_sparse_matrix(n_rows=12,
                                    columns_spec=5,
                                    min_number_of_values=30,
                                    max_number_of_values=None)
        self.assertTrue(isinstance(smat, SSparseMatrix))

    def test_n_vals_2(self):
        random.seed(332)
        my_min = 30
        smats = [random_sparse_matrix(n_rows=12,
                                      columns_spec=5,
                                      min_number_of_values=my_min,
                                      max_number_of_values=None) for i in range(12)]

        nnzs = [x.nnz >= my_min for x in smats]

        self.assertTrue(all(nnzs))

    def test_generator_1(self):
        smat = random_sparse_matrix(n_rows=12,
                                    columns_spec=15,
                                    generators=lambda size: [random.random() for i in range(size)])
        self.assertTrue(isinstance(smat, SSparseMatrix))

    def test_row_names_generator_1(self):
        # If the row names generator produced number of row names that is smaller
        # than the specified number of rows, then ordinal suffixes are added to the row names.

        my_row_names = list("ABCD")
        m = 12

        with self.assertWarnsRegex(UserWarning,
                                   r"The specified number of rows is larger than the obtained row names.*"):
            smat = random_sparse_matrix(n_rows=m,
                                        columns_spec=15,
                                        row_names_generator=lambda size: [random.choice(my_row_names) for i in
                                                                          range(size)])

        self.assertTrue(isinstance(smat, SSparseMatrix) and smat.rows_count() == m)

    def test_row_names_generator_2(self):
        # If the row names generator produced number of row names that is smaller
        # than the automatically derived number of rows, then correct the number of rows.

        my_row_names = list("ABCD")

        smat = random_sparse_matrix(n_rows=None,
                                    columns_spec=15,
                                    row_names_generator=lambda size: [random.choice(my_row_names) for i in
                                                                      range(size)])

        self.assertTrue(isinstance(smat, SSparseMatrix) and smat.rows_count() <= len(my_row_names))


if __name__ == '__main__':
    unittest.main()
