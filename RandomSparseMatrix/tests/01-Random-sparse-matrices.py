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

    def test_simple_4(self):
        random.seed(332)
        my_min = 30
        smats = [random_sparse_matrix(n_rows=12,
                                      columns_spec=5,
                                      min_number_of_values=my_min,
                                      max_number_of_values=None) for i in range(12)]

        nnzs = [x.nnz >= my_min for x in smats]

        self.assertTrue(all(nnzs))


if __name__ == '__main__':
    unittest.main()
