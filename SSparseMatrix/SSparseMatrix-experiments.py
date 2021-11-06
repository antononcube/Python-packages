from src.SSparseMatrix import SSparseMatrix
from scipy import sparse
import copy


smat = SSparseMatrix([[1, 0, 16, 16], [4, 0, 0, 100], [0, 9, 25, 25]])
smat.set_row_names(["A1", "B2", "C3"])
smat.set_column_names(["a", "b", "c", "d"])

smat.print_matrix(boundary=False)

smat2 = smat.copy().dot(copy.deepcopy(smat).transpose())
smat2.print_matrix(boundary=True)

print(smat.row_sums())
print(smat.row_sums_dict())

print(smat.column_sums())
print(smat.column_sums_dict())

print(160 * "=")

print(smat.sparse_matrix()[0:2,:].todense())

print(smat[0, 3])
print(smat["A1", "c"])

print(160 * "-")
smat[0:2, :].print_matrix()
smat[:, ["a", "b", "c"]].print_matrix()
smat[["A1", "B2"], :].print_matrix()

print(160 * "-")
# It looks like there is a problem with scipy csr_matrix
#smat.sparse_matrix()[[0,1],[0,1,2]]
#smat[["A1", "B2"], ["a", "b", "c"]].print_matrix()
