from SSparseMatrix.SSparseMatrix import *

# Create a sparse matrix with named rows and columns (a SSparseMatrix object)
mat = [[1, 0, 0, 3], [4, 0, 0, 5], [0, 3, 0, 5], [0, 0, 1, 0], [0, 0, 0, 5]]
smat = SSparseMatrix(mat)
smat.set_row_names(["A", "B", "C", "D", "E"])
smat.set_column_names(["a", "b", "c", "d"])

# smat2 = SSparseMatrix(mat, list("ABCDE"), list("abcd"))
# smat2.print_matrix()

# smat3 = SSparseMatrix(matrix=mat, row_names="", column_names=list("abcd"))
# smat3.print_matrix()

# Print the sparse matrix
smat.print_matrix()

# Here is the dense version of the sparse matrix
print(smat.sparse_matrix().todense())

# Multiply with the transpose and print
smat2 = smat.dot(smat.transpose())
smat2.print_matrix()

# Multiply with a list-vector
smat3 = smat.dot([1, 2, 1, 0])
smat3.print_matrix()

# Get single element
print(smat["A", "d"])
print(smat[0, 3])

# Get sub-matrix using row names
smat[["A", "D", "B"], :].print_matrix()

# Get sub-matrix using row indices
smat[[0, 3, 1], :].print_matrix()

# Get sub-matrix with columns names
smat[:, ['a', 'c']].print_matrix()

# Get sub-matrix with columns indices
smat[:, [0, 2]].print_matrix()

# Row sums
print(smat.row_sums())
print(smat.row_sums_dict())

# Column sums
print(smat.column_sums())
print(smat.column_sums_dict())
