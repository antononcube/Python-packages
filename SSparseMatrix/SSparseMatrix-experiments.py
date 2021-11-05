from SSparseMatrix.SSparseMatrix import SSparseMatrix
from scipy import sparse
import copy

A = sparse.csr_matrix([[1, 2, 0], [0, 0, 3], [4, 0, 5], [4, 10, 5]])

smat = SSparseMatrix()

smat.set_sparse_matrix(A)

smat.set_row_names(["a", "b", "c", "d"])

smat.set_column_names(["A1", "B2", "C3"])

print(smat.sparse_matrix().todense())

smat.print_matrix()

print(60 * "-")

smat.transpose().print_matrix()

print(60 * "-")

smat.multiply(smat.sparse_matrix()).print_matrix()

print(60 * "-")

smat2 = copy.deepcopy(smat)
smat2.transpose()

smat.dot(smat2).print_matrix()
